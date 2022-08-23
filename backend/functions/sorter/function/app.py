from functions.sorter.function.sorting_service import SorterService

from functions.sorter.function.models import SortEvent


def lambda_handler(event, context):
    event = SortEvent(**event)
    service = SorterService()
    return service.process_event(event)
