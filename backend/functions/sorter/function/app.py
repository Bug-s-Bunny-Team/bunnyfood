import json

from db.utils import init_db
from entity.post import Post
from functions.sorter.function.sorting_service import SorterService


def lambda_handler(event, context):
    try:
        init_db()
        sorterEvent = SorterService
        sorterEvent.sort(event)
        return 'Success'
    except Exception as e:
        print('Error processing Event {}'.format(json.dumps(event, indent=2)))
        raise e
