import json
import re
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from common.constants import INSTA_SHORTCODE_REGEX


def create_response(data, code: int) -> dict:
    return {'statusCode': code, 'body': json.dumps(data)}


def create_error_response(message: str, code: int = 400) -> dict:
    return create_response({'error': message}, code)


def s3_key_exists(bucket_name: str, key: str) -> bool:
    try:
        s3 = boto3.client('s3')
        s3.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError:
        return False


def s3_upload_file(bucket_name: str, key: str, src: Path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(str(src), key)


def key_present_in_dict(dict, key):
    if key in dict.keys():
        return True
    else:
        return False


def extract_insta_shortcode(url: str) -> Optional[str]:
    groups = re.compile(INSTA_SHORTCODE_REGEX).match(url)
    if groups:
        shortcode = groups.group(6)
        if shortcode:
            return shortcode
    return None
