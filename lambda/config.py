import os
import logging
import boto3
import pytz

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Twitter Authentication configuration
# == OAuth Authentication ==
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
# The consumer keys can be found on  application's Details
# https://dev.twitter.com/apps (under "OAuth settings")
# We will store those secrets in AWS SSM and then retrieve
# Please refer to readme for retrieving it from twitter developer portal and installed keys in AWS SSM
# The access tokens of applications's Details
# page located at https://dev.twitter.com/apps (located under "Your access token")
ssm = boto3.client('ssm')
key_prefix = "/third-party/twitter"
key_names = ['consumer-key', 'consumer-secret', 'access-token', 'access-token-secret']
twitter_keys = {}
def get_twitter_keys():
     
    global twitter_keys
    if len(twitter_keys) == 0:
        for key_name in key_names:

            logger.info(f".....{key_prefix}/{key_name}")
            try:
                res = ssm.get_parameter(Name=f"{key_prefix}/{key_name}", WithDecryption=True)
                twitter_keys[key_name] = res['Parameter']['Value']
                logging.info('.....' + res['Parameter']['Value'])
            except ssm.exceptions.ParameterNotFound:
                logging.error(f'ParameterNotFound {key_prefix}/{key_name}')
                twitter_keys = {}
# fetch keys once
get_twitter_keys()

# DynamoDB Configuration
TABLE_NAME_DEFAULT = "Twitter-DM"
# 1 years of data retention in seconds
TABLE_TTL_DEFAULT = 3600*24*365*1
ISO_FORMAT = '%Y-%m-%d %H:%M:%S %Z'
TZ = pytz.timezone('America/New_York')
# DM fields 
ID_COLUMN = 'id'
CREATED_TIME_COLUMN = 'created_time'
FROM_COLUMN = 'From'
TO_COLUMN = 'To'
MESSAGE_COLUMN = 'Message'
SENDER_ID_COLUMN = 'sender_id'
RECIPIENT_ID_COLUMN = 'recipient_id'
INSERTION_TS_COLUMN = "insertion_ts"
EXPIRATION_TS_COLUMN = 'expiration_time'
STATUS_NEW_COLUMN = 'New?'
HEADERS = [ID_COLUMN, CREATED_TIME_COLUMN, FROM_COLUMN, TO_COLUMN, MESSAGE_COLUMN, STATUS_NEW_COLUMN]

# Email Configuration
# Make sure email addresses used below are certified in AWS SES
# Email address config is from environment variables, passed from cloudformation parameters
SENDER = os.environ.get('SEND_EMAIL_ADDRESS','')
if len(SENDER)==0:
    logger.error("Error in configuration, SEND_EMAIL_ADDRESS")
    exit(-1)
logger.info(f"Config {SENDER}")
RECIPIENT = os.environ.get('RECEPIENT_EMAIL_ADDRESS','')
if len(RECIPIENT)==0:
    logger.error("Error in configuration, RECEPIENT_EMAIL_ADDRESS")
    exit(-1)
logger.info(f"Config {RECIPIENT}")   
# The character encoding for the email.
CHARSET = "UTF-8"