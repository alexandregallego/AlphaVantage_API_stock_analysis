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
                (i['fiscalDateEnding'][:4], i['totalRevenue']))

        sales_growth_df = pd.DataFrame(total_revenue, columns=[
                                       'YEAR', 'TOTAL_REVENUE'])

        sales_growth_df['TOTAL_REVENUE'] = sales_growth_df.TOTAL_REVENUE.astype(
            float)

        sales_growth_df['SALES_GROWTH'] = sales_growth_df['TOTAL_REVENUE'].pct_change(
            periods=-1) * 100

        sales_growth_df = sales_growth_df.dropna()

        sales_growth_df['SALES_GROWTH'] = sales_growth_df['SALES_GROWTH'].apply(
            lambda x: str(round(float(x), 2)) + '%')

        sales_growth_dict = {}

        for i in range(0, len(sales_growth_df.SALES_GROWTH.values.tolist())):
            sales_growth_dict[f"SALES_GROWTH_{sales_growth_df.YEAR.values.tolist()[i]}"] = [
                sales_growth_df.SALES_GROWTH.values.tolist()[i]]

        self.sales_growth_df_v2 = pd.DataFrame(sales_growth_dict)
        self.sales_growth_df_v2['Company'] = self.symbol

        return self.sales_growth_df_v2

    def final_df(self):

        final_df = pd.merge(self.df, self.sales_growth_df_v2,
                            on='Company', how='left')

        return final_df


msft_analysis = CompanyAnalysis(symbol='MSFT', access_key='')
msft_analysis.per_ratio_calculation()
msft_analysis.income_statement_calculation()
print(msft_analysis.final_df())
