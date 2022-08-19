import json

from db.utils import init_db
from entity.post import Post
from functions.sorter.function.sorting_service import SorterService


def lambda_handler(event, post: Post):
    try:
        init_db('user', 'password', '172.18.0.10', 'poc_test')
        sorterEvent = SorterService
        sorterEvent.sort(post)
        return 'Success'
    except Exception as e:
        print('Error processing Event {}'.format(json.dumps(event, indent=2)))
        raise e


lambda_handler(
    {},
    None
)
