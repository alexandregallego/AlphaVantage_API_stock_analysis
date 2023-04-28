import requests
import pandas as pd


class CompanyAnalysis():
    def __init__(self, symbol: str = None, access_key: str = None):
        self.symbol = symbol
        self.access_key = access_key

    def per_ratio_calculation(self):
        """Function to extract the PER ratio of whatever company symbol specified."""

        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey={self.access_key}'
        response = requests.get(url)
        self.per_ratio = response.json()['PERatio']
        dictionary_init = {'Company': [
            self.symbol], 'PER ratio': [self.per_ratio]}
        self.df = pd.DataFrame(dictionary_init)

        return self.df

    def income_statement_calculation(self):
        """Function to calculate relevant metrics from the income statement of whatever company symbol specified."""

        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.symbol}&apikey={self.access_key}'
        response = requests.get(url)
        income_statement_data = response.json()
        total_revenue = []
        for i in income_statement_data['annualReports']:
            total_revenue.append(
                (i['fiscalDateEnding'][:4], i['totalRevenue'], i['netIncome']))

        income_statement_df = pd.DataFrame(total_revenue, columns=[
            'YEAR', 'TOTAL_REVENUE', 'NET_INCOME'])

        income_statement_df['TOTAL_REVENUE'] = income_statement_df.TOTAL_REVENUE.astype(
            float)

        income_statement_df['SALES_GROWTH'] = income_statement_df['TOTAL_REVENUE'].pct_change(
            periods=-1)

        income_statement_df['NET_INCOME'] = income_statement_df.NET_INCOME.astype(
            float)

        income_statement_df['NET_INCOME_GROWTH'] = income_statement_df['NET_INCOME'].pct_change(
            periods=-1)

        income_statement_df = income_statement_df.dropna()

        income_statement_df[['SALES_GROWTH', 'NET_INCOME_GROWTH']] = income_statement_df[[
            'SALES_GROWTH', 'NET_INCOME_GROWTH']].applymap('{:.2%}'.format)

        income_statement_dict = {}

        for i in range(0, len(income_statement_df.SALES_GROWTH.values.tolist())):
            income_statement_dict[f"SALES_GROWTH_{income_statement_df.YEAR.values.tolist()[i]}"] = [
                income_statement_df.SALES_GROWTH.values.tolist()[i]]

        for i in range(0, len(income_statement_df.NET_INCOME_GROWTH.values.tolist())):
            income_statement_dict[f"NET_INCOME_GROWTH_{income_statement_df.YEAR.values.tolist()[i]}"] = [
                income_statement_df.NET_INCOME_GROWTH.values.tolist()[i]]

        self.income_statement_df_v2 = pd.DataFrame(income_statement_dict)
        self.income_statement_df_v2['Company'] = self.symbol

        return self.income_statement_df_v2

    def final_df(self):

        final_df = pd.merge(self.df, self.income_statement_df_v2,
                            on='Company', how='left')

        return final_df


msft_analysis = CompanyAnalysis(symbol='MSFT', access_key='QV6GB9465BJSYTEE')
msft_analysis.per_ratio_calculation()
msft_analysis.income_statement_calculation()
print(msft_analysis.final_df())
