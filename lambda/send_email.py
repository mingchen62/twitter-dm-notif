import boto3
from botocore.exceptions import ClientError
import logging

from config import SENDER, RECIPIENT, CHARSET

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Create a new SES resource
client = boto3.client('ses')

class HTML:

    def __init__(self, Header, tableStyles = {}, trStyles = {}, thStyles = {}):
        self.tableStyles = HTML._styleConverter(tableStyles)
        trStyles = HTML._styleConverter(trStyles)
        thStyles = HTML._styleConverter(thStyles)
        self.rows = []
        self.Header= f'<tr {trStyles} >'
        for th in Header:
            self.Header += f'\n<th {thStyles} >{th}</th>'
        self.Header += '\n</tr>'

    @staticmethod
    def _styleConverter(styleDict : dict):
        if styleDict == {}:
            return ''
        styles = ''
        for [style, value] in styleDict.items():
            styles +=f'{style}: {value};'
        return f'style="{styles}"'

    def addRow(self, row, trStyles = {}, tdStyles = {}):
        trStyles = HTML._styleConverter(trStyles)
        tdStyles = HTML._styleConverter(tdStyles)
        temp_row = f'\n<tr {trStyles} >'
        for td in row:
            temp_row += f'\n<td {tdStyles} >{td}</td>'
        temp_row += '\n</tr>'
        self.rows.append(temp_row)


    def __str__(self):


        return \
f'''
<table {self.tableStyles} >
{self.Header}
{''.join(self.rows)}
</table>
'''

def dictionaryToHTMLTable(dict : dict):
    html = HTML(Header = dict.keys(),
                tableStyles={'margin': '3px'},
                trStyles={'background-color': '#7cc3a97d'},
                thStyles={ 'color': 'white'})
    for i, row in enumerate(zip(*dict.values())):
        # last column is status. if status new, use a different color.
        if row[-1] == 'N':
            BGC = 'aliceblue'
        else:
            BGC = '#c2d4e4'
        html.addRow(row, trStyles={'background-color' : BGC}, tdStyles={'padding': '1rem'})
    return html

def send_email_via_ses(body_html, body_text, subject):
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER,

        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        logger.error(e.response['Error']['Message'], exc_info=e)
    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])