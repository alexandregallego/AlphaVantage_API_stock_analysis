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
            total_revenue.append(
                (i['fiscalDateEnding'][:4], i['totalRevenue']))

        sales_growth_df = pd.DataFrame(total_revenue, columns=[
                                       'YEAR', 'TOTAL_REVENUE'])

        sales_growth_df['TOTAL_REVENUE'] = sales_growth_df.TOTAL_REVENUE.astype(
            float)

        sales_growth_df['SALES_GROWTH'] = sales_growth_df['TOTAL_REVENUE'].pct_change(
            periods=-1) * 100

        sales_growth_df['SALES_GROWTH'] = sales_growth_df['SALES_GROWTH'].apply(
            lambda x: str(round(float(x), 2)) + '%')

        return sales_growth_df


msft_analysis = CompanyAnalysis(symbol='MSFT', access_key='QV6GB9465BJSYTEE')
print(msft_analysis.per_ratio_calculation())
print(msft_analysis.income_statement_calculation())
