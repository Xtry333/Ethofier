import xml.etree.ElementTree as et
import pymongo
import requests
import settings as s
import bot
from flask import Flask
from flask import request
from threading import Thread
from datetime import datetime
from datetime import timedelta
import scheduler


app = Flask('app')
mongo_client = pymongo.MongoClient(s.ATLAS_CONNECTION_STRING)
db = mongo_client['Ethofier']


def request_subscription(channel, sub_mode=True):
    subscribe_url = 'https://pubsubhubbub.appspot.com/subscribe'
    callback_url = s.HOST_URL + 'notification'
    data = {
        'hub.callback': callback_url,
        'hub.topic': s.CHANNEL_URL % channel,
        'hub.lease_seconds': 60 * 60 * 24 * 5,
        'hub.mode': 'subscribe' if sub_mode else 'unsubscribe'
    }
    bot.log_message('Renewing subscription of channel %s.' % channel)
    requests.post(subscribe_url, data=data)


def renew_subscriptions():
    subs = db.Subscriptions.find()
    for sub in subs:
        if (sub['valid'] - timedelta(days=1) < datetime.now()):
            request_subscription(sub['channel_id'])


def app_run():
    # bot.log_message("Keep-Alive Module Running.")
    app.run(host='0.0.0.0', port=8080)


@app.route('/')
def index_route():
    return 'I\'m alive!'


def keep_alive_start():
    t = Thread(target=app_run)
    t.start()


@app.route('/notification', methods=['GET'])
def subscribe_confirmation():

    mode = request.args.get('hub.mode')
    challenge = request.args.get('hub.challenge')
    topic = request.args.get('hub.topic')

    if (mode == 'subscribe'):
        channel_id = topic.split('=')[-1]
        lease_seconds = request.args.get('hub.lease_seconds', default='0')
        valid = datetime.now() + timedelta(seconds=int(lease_seconds))
        if (challenge):
            current_sub = db.Subscriptions.find_one({'channel_id': channel_id})
            subscription = {
                'channel_id': channel_id,
                'topic': topic,
                'added': datetime.now(),
                'valid': valid
            }
            if (not current_sub):
                db.Subscriptions.insert_one(subscription)
            else:
                db.Subscriptions.update_one({
                    '_id': current_sub['_id']
                }, {'$set': {
                    'valid': valid
                }})
            bot.log_message('Confirmation received:\n' + str(request.args))
            return challenge
    else:
        bot.log_message('Unsubscribe event:\n' + topic)
    return 'No hub.challenge in get request'


@app.route('/notification', methods=['POST'])
def notification():
    root = et.fromstring(request.data)
    video_id = root.find('./atom:entry/yt:videoId', s.NAMESPACES).text
    video_link = root.find('./atom:entry/atom:link', s.NAMESPACES).get('href')
    video_title = root.find('./atom:entry/atom:title', s.NAMESPACES).text

    bot.log_message('POST Notification of %s.' % video_id)

    try: 
        if (not db.Notifications.find_one({'video_id': video_id, notification: None })):
            db.Notifications.insert_one({'video_id': video_id, 'video_title': video_title, 'video_link': video_link})
            bot.send_notification(video_id, video_title, video_link)
            db.Notifications.update_one({'video_id': video_id}, {'notification': True})
            return 'Notification Received, sent to Telegram channel.'
        else:
            return 'Notification Received and ignored.'
    except:
        bot.send_simple_notification(video_id, video_title, video_link)

@app.route('/subscribe')
def subscribe():
    channel = request.args.get('channel_id')
    mode = request.args.get('sub', default='True')
    request_subscription(channel, mode == 'True')
    return 'Done.'


keep_alive_start()
scheduler.add_job(func=renew_subscriptions)
scheduler.start()
renew_subscriptions()
