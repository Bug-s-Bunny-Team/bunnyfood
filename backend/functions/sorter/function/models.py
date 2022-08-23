from common.models import LambdaEvent


# TODO: define the event
class SortEvent(LambdaEvent):
    posts: list
