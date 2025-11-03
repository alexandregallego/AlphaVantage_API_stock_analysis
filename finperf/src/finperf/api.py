from .company import Company
import requests #type: ignore

class CompanyApi:
    def __init__(self, url: str, apiKey: str, company: Company):
        self.url = url
        self.apiKey = apiKey
        self.company = company

    def get(self):
        response = requests.get(self.url)
        return response.json()

class BalanceSheetApi(CompanyApi):

    def __init__(self, apiKey: str, company: Company, url: str = 'ttps://www.alphavantage.co/query?function=BALANCE_SHEET&symbol='):
        super().__init__(
            url=url + f'{company.ticker}' + f'&apikey={apiKey}',
            apiKey=apiKey,
            company=company
        )