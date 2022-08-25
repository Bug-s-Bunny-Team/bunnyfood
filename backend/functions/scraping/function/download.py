import os
from pathlib import Path
from typing import Optional

import requests

from db.models import Post
from common.utils import s3_key_exists, s3_upload_file


class Downloader:
    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name

    @staticmethod
    def download_media(url: str, dest: Path):
        with requests.get(url, stream=True) as r:
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def download_and_save_post(
        self, post: Post, overwrite: bool = True
    ) -> Optional[str]:
        post_key = f'media/{post.media_filename}'

        if not overwrite and s3_key_exists(self._bucket_name, post_key):
            print('post already downloaded, skipping')
        else:
            print('downloading post media')
            dest = Path('/tmp') / post.media_filename
            self.download_media(post.media_url, dest)

            print(f'uploading to s3 with key "{post_key}"')
            s3_upload_file(self._bucket_name, post_key, dest)

            return post_key

        return None
