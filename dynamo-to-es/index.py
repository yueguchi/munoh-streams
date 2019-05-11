import boto3
import requests
import logging
import json
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from requests_aws4auth import AWS4Auth

region = 'ap-northeast-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-munoh-search-bz33yvrlve67kvwg5plleuzwli.ap-northeast-1.es.amazonaws.com' # the Amazon ES domain, with https://
index = 'words'
type = 'word'
url = host + '/' + index + '/' + type + '/'

headers = { "Content-Type": "application/json" }

def handler(event, context):
    count = 0
    for record in event['Records']:
        logger.info('record: {}'.format(record))
        # Get the primary key for use as the Elasticsearch ID
        id = record['dynamodb']['Keys']['id']['S']

        if record['eventName'] == 'REMOVE':
            r = requests.delete(url + id, auth=awsauth)
        else:
            # wordは終端EOFのときはnullが入るので空文字いれとく
            word1_dict = record['dynamodb']['NewImage']['word1']
            word1 = record['dynamodb']['NewImage']['word1']['S'] if 'S' in word1_dict else ''
            word2_dict = record['dynamodb']['NewImage']['word2']
            word2 = record['dynamodb']['NewImage']['word2']['S'] if 'S' in word2_dict else ''
            word3_dict = record['dynamodb']['NewImage']['word3']
            word3 = record['dynamodb']['NewImage']['word3']['S'] if 'S' in word3_dict else ''
            created_at = record['dynamodb']['NewImage']['created_at']['N']
            updated_at = record['dynamodb']['NewImage']['updated_at']['N']
            jsonStr = '''
{{
    "id": "{_id}",
    "word1": "{_word1}",
    "word2": "{_word2}",
    "word3": "{_word3}",
    "created_at": "{_created_at}",
    "updated_at": "{_updated_at}"
}}
'''.format(_id = id, _word1 = word1, _word2 = word2, _word3 = word3, _created_at = created_at, _updated_at = updated_at)
            document = json.loads(jsonStr)
            logger.info('got NewImage {}'.format(document))
            logger.info('endpoint: %s' % url + id)
            r = requests.put(url + id, auth=awsauth, json=document, headers=headers)
            logger.info('result {}'.format(r))
            logger.info("detail: " + r.text)
        count += 1
    return str(count) + ' records processed.'
