import os
from pathlib import Path
from typing import Optional

import requests

from db.models import Post
from common.utils import s3_key_exists, s3_upload_file


# TODO: add option to download file in memory and don't create a new file
def download_media(url: str, dest: Path):
    with requests.get(url, stream=True) as r:
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def download_and_save_post(post: Post, overwrite: bool = True) -> Optional[str]:
    post_key = f'media/instagram/{post.media_filename}'
    bucket_name = os.environ['ENV_BUCKET_NAME']

    if not overwrite and s3_key_exists(bucket_name, post_key):
        print('post already downloaded, skipping')
    else:
        print('downloading post media')
        dest = Path('/tmp') / post.media_filename
        download_media(post.media_url, dest)

        print(f'uploading to s3 with key "{post_key}"')
        s3_upload_file(bucket_name, post_key, dest)

        return post_key

    return None
