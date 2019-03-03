from __future__ import print_function

import json
import logging
import urllib
import os
import boto3

log = logging.getLogger()
log.setLevel(logging.DEBUG)

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    log.debug("Received context {}".format(context))

    # Get the object from the event and log it 
    snsevent = json.loads(event['Records'][0]['Sns']['Message'])
    sourcebucket = snsevent['Records'][0]['s3']['bucket']['name']
    eventtime = snsevent['Records'][0]['eventTime']

    log.debug(eventtime) # Eventtime might be used to create a partition, depending on source data.  

    targetbucket = "knox-data-lake"
    feedname = sourcebucket.split('knox-data-')[-1]
    log.debug(feedname)
    
    sourcekey = urllib.unquote_plus(snsevent['Records'][0]['s3']['object']['key']).decode('utf8')
    try:
        keyname = sourcekey.split('/')[-2]
    except:
        #set to empty string if index out of range
        keyname = ""
        
    filename = sourcekey.split('/')[-1]

    targetkey = "{feedname}/{sourcekey}".format(feedname=feedname,sourcekey=sourcekey)
    
    copy_source = {
        'Bucket': sourcebucket,
        'Key': sourcekey
    }

    s3.meta.client.copy_object(CopySource=copy_source, Bucket=targetbucket, Key=targetkey)
    return {}
