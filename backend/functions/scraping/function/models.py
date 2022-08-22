from common.models import LambdaEvent


class ScrapingEvent(LambdaEvent):
    username: str
