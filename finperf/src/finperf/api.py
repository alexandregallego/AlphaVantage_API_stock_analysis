from abc import ABC, abstractmethod
from .company import Company

class ApiInterface(ABC):
    @abstractmethod
    def get(self):
        pass

class BalanceSheetApi(ApiInterface):

    def __init__(self, url: str, apiKey: str, company: Company):
        self.url = url
        self._apiKey = apiKey
        self.company = company

    def get(self):
        return None