from abc import ABC, abstractmethod

from common.models import LambdaEvent


class BaseService(ABC):
    @abstractmethod
    def process_event(self, event: LambdaEvent) -> dict:
        pass
