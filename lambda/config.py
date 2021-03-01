# DynamoDB
TABLE_NAME_DEFAULT = "Twitter-DM"
# 1 years of data retention in seconds
TABLE_TTL_DEFAULT = 3600*24*365*1

ISO_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
# The consumer keys can be found on  application's Details
#  https://dev.twitter.com/apps (under "OAuth settings")
consumer_key = "xyz"
consumer_secret = "xyz"
# The access tokens of applications's Details
# page located at https://dev.twitter.com/apps (located under "Your access token")
access_token = "xyz"
access_token_secret = "xyz"

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

# Email config
# Make sure email addresses used below are certified in AWS SES
SENDER = "Mike somebody <xyz@gmail.com>"
RECIPIENT = "zyx@gmail.com"
# The character encoding for the email.
CHARSET = "UTF-8"