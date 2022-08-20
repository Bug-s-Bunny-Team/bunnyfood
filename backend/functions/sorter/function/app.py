import json

from entity.post import Post
from functions.sorter.function.sorting_service import SorterService


def lambda_handler(event, post: Post):
    try:
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
