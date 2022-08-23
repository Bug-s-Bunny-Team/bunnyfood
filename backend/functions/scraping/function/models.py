from common.models import LambdaEvent


class ScrapingEvent(LambdaEvent):
    username: str
    posts_limit: int = 6
