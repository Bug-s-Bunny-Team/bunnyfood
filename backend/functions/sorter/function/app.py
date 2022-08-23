#
# from entity.post import Post
# from functions.sorter.function.sorting_service import SorterService
from common.utils import create_response


def lambda_handler(event, context):
    # try:
    #     sorterEvent = SorterService
    #     sorterEvent.sort(post)
    #     return 'Success'
    # except Exception as e:
    #     print('Error processing Event {}'.format(json.dumps(event, indent=2)))
    #     raise e

    return create_response('Hi from sorter', 200)
