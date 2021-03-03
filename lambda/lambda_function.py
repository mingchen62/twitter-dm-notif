import json
import pprint
import logging

from send_email import send_email_via_ses, dictionaryToHTMLTable
from twitter_api_helper import retrieve_dm
from db_helper import _query, _insert
from config import ID_COLUMN, HEADERS, STATUS_NEW_COLUMN

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    all_dms  = retrieve_dm()
    # Check database
    num_new = 0
    for i, id in enumerate(all_dms[ID_COLUMN]):
      if _query(id):
        all_dms[STATUS_NEW_COLUMN][i]='N'
      else:
        num_new = num_new+1
        d ={}
        for k in HEADERS:
          d[k] = all_dms[k][i]
        _insert(d)
        
    if num_new == 0:
      logger.info("no new DM")
      return {
        'statusCode': 200,
        'body': json.dumps("no new DM")
      }
      
    html_table = dictionaryToHTMLTable(all_dms)
 
    body_text = pprint.pformat(all_dms)
    
    # The HTML body of the email.
    body_html = f"""<html>
    <head></head>
    <body>
      <h1>Aloha</h1>
      <p>
      {html_table}
      </p>
    </body>
    </html>
    """ 
    subject = f"{num_new} new direct messages received"
    logger.info(subject)
    
    send_email_via_ses(body_html, body_text, subject)
    
    return {
        'statusCode': 200,
        'body': json.dumps(subject)
    }
