import boto3
import botocore
import logging
import os
import time
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timezone
from decimal import Decimal
import json

from config import (
    ID_COLUMN,
    CREATED_TIME_COLUMN,
    FROM_COLUMN, 
    TO_COLUMN,
    MESSAGE_COLUMN,
    SENDER_ID_COLUMN,
    RECIPIENT_ID_COLUMN,
    INSERTION_TS_COLUMN,
    EXPIRATION_TS_COLUMN,
    TABLE_NAME_DEFAULT,
    TABLE_TTL_DEFAULT,
    ISO_FORMAT
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# dynamo db config and initialization
dynamodb = boto3.resource('dynamodb')

table_name = os.environ.get('TABLENAME_OVERRIDE', TABLE_NAME_DEFAULT)
logger.info("table_name %s", table_name)

try:
    TABLE_TTL = int(os.environ.get('TABLE_TTL', TABLE_TTL_DEFAULT))
except:
    TABLE_TTL = TABLE_TTL_DEFAULT
logger.info("TABLE_TTL %d", TABLE_TTL)

try:
    table = dynamodb.Table(table_name)
except Exception as e:
    logger.error(
            'Error in connecting to dynamob table {}, Skipping execution.'.format(table_name),
            exc_info=e)
    exit(1)

def _query(message_id):
    # DB query
    response = table.query(
            KeyConditionExpression=Key(ID_COLUMN).eq(message_id)
        )

    if len(response['Items']) >0 :
        return response['Items']
    else:
        return None

def _insert(item):
    # Add timestamps
    item[INSERTION_TS_COLUMN]= datetime.fromtimestamp(datetime.timestamp(datetime.now()), tz=timezone.utc).strftime(ISO_FORMAT)
    item[EXPIRATION_TS_COLUMN]=  str(int(time.time() + TABLE_TTL))
    
    item = json.loads(json.dumps(item), parse_float=Decimal)

    # DB insertion
    table.put_item(
            Item=item
        )
    logger.debug('PutItem succeeded %s', str(item))
