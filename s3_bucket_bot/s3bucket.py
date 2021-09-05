import os
import boto3
import logging
from botocore.exceptions import ClientError

AWS_SERVER_PUBLIC_KEY = os.getenv('AWS_SERVER_PUBLIC_KEY')
AWS_SERVER_SECRET_KEY = os.getenv('AWS_SERVER_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
BUCKET_NAME = None
if os.getenv('BUCKET_NAME', '').strip():
    BUCKET_NAME = os.getenv('BUCKET_NAME')
ENDPOINT_URL = None
if os.getenv('ENDPOINT_URL', '').strip():
    ENDPOINT_URL = os.getenv('ENDPOINT_URL')
EDGE_ENDPOINT_URL = None
if os.getenv('EDGE_ENDPOINT_URL', '').strip():
    EDGE_ENDPOINT_URL = os.getenv('EDGE_ENDPOINT_URL')
CUSTOM_ENDPOINT_URL = None
if os.getenv('CUSTOM_ENDPOINT_URL', '').strip():
    CUSTOM_ENDPOINT_URL = os.getenv('CUSTOM_ENDPOINT_URL')


def get_s3_client():
    session = boto3.session.Session()
    return session.client('s3',
                          region_name=AWS_REGION,
                          endpoint_url=ENDPOINT_URL,
                          aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
                          aws_secret_access_key=AWS_SERVER_SECRET_KEY)


def upload_file(file_name, object_name=None, mime_type=None, acl=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :param mime_type: File mime type
    :param acl: ACL specifying access rules for the objects (e.g. private or public-read). Defaults to private
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        extra_args = {}
        if acl is not None and acl == 'public-read':
            extra_args['ACL'] = acl
        if mime_type is not None:
            extra_args['ContentType'] = mime_type

        s3_client = get_s3_client()
        # Upload the file
        s3_client.upload_file(file_name,
                              BUCKET_NAME,
                              object_name,
                              ExtraArgs=extra_args)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_file_name(file_name):
    """ Get an object URL """
    if CUSTOM_ENDPOINT_URL is not None:
        return f'{CUSTOM_ENDPOINT_URL}/{file_name}'

    endpoint_url = 's3.amazonaws.com'
    if ENDPOINT_URL is not None:
        endpoint_url = ENDPOINT_URL.lstrip('https://')

    return f'https://{BUCKET_NAME}.{endpoint_url}/{file_name}'


def delete_file(file_name):
    s3_client = get_s3_client()
    # Delete the file
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_name)


def make_public(file_name):
    s3_client = get_s3_client()
    # Make the file public
    s3_client.put_object_acl(ACL='public-read', Bucket=BUCKET_NAME, Key=file_name)


def make_private(file_name):
    s3_client = get_s3_client()
    # Make the file public
    s3_client.put_object_acl(ACL='private', Bucket=BUCKET_NAME, Key=file_name)


def file_exist(file_name):
    try:
        s3_client = get_s3_client()
        s3_client.head_object(Bucket=BUCKET_NAME, Key=file_name)
    except ClientError as e:
        logging.error(e)
        if e.response['ResponseMetadata']['HTTPStatusCode'] != 404:
            raise e
        return False
    return True
