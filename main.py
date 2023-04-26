import requests
import pandas as pd


class CompanyAnalysis():
    def __init__(self, symbol: str = None, access_key: str = None):
        self.symbol = symbol
        self.access_key = access_key

    def per_ratio_calculation(self):
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey={self.access_key}'
        response = requests.get(url)
        self.per_ratio = response.json()['PERatio']
        dictionary_init = {'Company': [
            self.symbol], 'PER ratio': [self.per_ratio]}
        self.df = pd.DataFrame(dictionary_init)

        return self.df

    def income_statement_calculation(self):
        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.symbol}&apikey={self.access_key}'
        response = requests.get(url)
        income_statement_data = response.json()
        total_revenue = []
        for i in income_statement_data['annualReports']:
            total_revenue.append((i['fiscalDateEnding'], i['totalRevenue']))

        return total_revenue


msft_analysis = CompanyAnalysis(symbol='MSFT', access_key='')
print(msft_analysis.per_ratio_calculation())
print(msft_analysis.income_statement_calculation())


# income_statement_data = response.json()
# df = pd.DataFrame(
#    income_statement_data['annualReports'][0].keys(), columns=['KEY_NAMES'])
# df.to_csv('Income_statement_keys.csv')

# print(income_statement_data['Symbol'],  income_statement_data['PERatio'])

# for i in income_statement_data['annualReports']:
#    print(i)
# else:
#   print('Error fetching income statement data')
