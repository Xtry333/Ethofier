import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
NOTIFICATIONS_CHAT_ID = os.environ.get("CHAT_ID")
DEBUG_CHAT_ID = os.environ.get("DEBUG_CHAT_ID")
HOST_URL = os.environ.get("HOST_URL")
ATLAS_CONNECTION_STRING = os.environ.get("ATLAS_CONNECTION_STRING")
THUMBNAIL_URL = 'https://img.youtube.com/vi/%s/0.jpg'
CHANNEL_URL = 'https://www.youtube.com/xml/feeds/videos.xml?channel_id=%s'
DATETIME_FORMAT = '%Y/%m/%d, %H:%M:%S'

NAMESPACES = {
    'atom': 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015'
}