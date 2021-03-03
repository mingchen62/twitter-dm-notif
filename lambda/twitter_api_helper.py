import tweepy
from collections import defaultdict
from datetime import datetime
import pytz
import logging

from config import (
    ISO_FORMAT, 
    twitter_keys, 
    ID_COLUMN,
    CREATED_TIME_COLUMN,
    FROM_COLUMN, 
    TO_COLUMN,
    MESSAGE_COLUMN,
    SENDER_ID_COLUMN,
    RECIPIENT_ID_COLUMN,
    STATUS_NEW_COLUMN,
    HEADERS,
    TZ
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    auth = tweepy.OAuthHandler(twitter_keys['consumer-key'], twitter_keys['consumer-secret'])
    auth.set_access_token(twitter_keys['access-token'], twitter_keys['access-token-secret'])
    api = tweepy.API(auth)
    # If the authentication was successful, the name of the account will be print out
    logger.info("twitter authentication succ "+api.me().name)
except Exception as e:
    logger.error("twitter authentication error", exc_info=e)
    exit(-1)

def lookup_user(user_id):
    res = []
    try:
        users_data = api.lookup_users(user_ids=[user_id])
        for user_data in users_data:
            res.append(user_data._json['screen_name'])
        return res
    except Exception as e:
        logger.error("lookup user error", exc_info=e)
        return [""]
        
def retrieve_dm():
    res = defaultdict(list)
    
    for  direct_message in api.list_direct_messages():

        try:
            msg_data = {}
            msg_data[ID_COLUMN] = direct_message._json['id']

            dt = datetime.fromtimestamp(int(direct_message._json['created_timestamp'])/1000, TZ)
            msg_data[CREATED_TIME_COLUMN] = dt.strftime(ISO_FORMAT)

            msg_data[SENDER_ID_COLUMN] = direct_message._json['message_create']['sender_id']
            msg_data[RECIPIENT_ID_COLUMN] = direct_message._json['message_create']['target']['recipient_id']
            msg_data[FROM_COLUMN] = lookup_user(msg_data['sender_id'])[0]
            msg_data[TO_COLUMN] = lookup_user(msg_data['recipient_id'])[0]
            msg_data[MESSAGE_COLUMN] = direct_message._json['message_create']['message_data']['text']
            msg_data[STATUS_NEW_COLUMN] = 'Y'
            for k in HEADERS:
                res[k].append(msg_data[k])
        except Exception as e:
            logger.error("retrieve_dm error", exc_info=e)
            continue
    #print(res)
    return  res