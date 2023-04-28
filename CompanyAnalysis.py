import requests
import pandas as pd
import csv


class CompanyAnalysis():
    def __init__(self, symbol: str = None, access_key: str = None):
        self.__symbol = symbol
        self.__access_key = access_key

    def trading_stocks_list(self):
        url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={self.__access_key}"
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            df = pd.DataFrame(my_list, columns=[
                              'TICKER', 'NAME', 'INDEX', 'TYPE_OF_ASSET', 'DATE', 'UNDEFINED', 'STATUS'])
            df.to_csv('STOCKS.csv')

    def per_ratio_calculation(self):
        """Function to extract the PER ratio of whatever company symbol specified."""

        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.__symbol}&apikey={self.__access_key}'
        response = requests.get(url)
        self.__per_ratio = response.json()['PERatio']
        dictionary_init = {'Company': [
            self.__symbol], 'PER ratio': [self.__per_ratio]}
        self.__df = pd.DataFrame(dictionary_init)

        return self.__df

    def income_statement_growth_calculation(self):
        """Function to calculate relevant growth metrics from the income statement of whatever company symbol specified."""

        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.__symbol}&apikey={self.__access_key}'
        response = requests.get(url)
        income_statement_data = response.json()
        total_revenue = []
        for i in income_statement_data['annualReports']:
            total_revenue.append(
                (i['fiscalDateEnding'][:4], i['totalRevenue'], i['netIncome']))

        income_statement_growth_df = pd.DataFrame(total_revenue, columns=[
            'YEAR', 'TOTAL_REVENUE', 'NET_INCOME'])

        income_statement_growth_df['TOTAL_REVENUE'] = income_statement_growth_df.TOTAL_REVENUE.astype(
            float)

        income_statement_growth_df['SALES_GROWTH'] = income_statement_growth_df['TOTAL_REVENUE'].pct_change(
            periods=-1)

        income_statement_growth_df['NET_INCOME'] = income_statement_growth_df.NET_INCOME.astype(
            float)

        income_statement_growth_df['NET_INCOME_GROWTH'] = income_statement_growth_df['NET_INCOME'].pct_change(
            periods=-1)

        income_statement_growth_df = income_statement_growth_df.dropna()

        income_statement_growth_df[['SALES_GROWTH', 'NET_INCOME_GROWTH']] = income_statement_growth_df[[
            'SALES_GROWTH', 'NET_INCOME_GROWTH']].applymap('{:.2%}'.format)

        income_statement_growth_dict = {}

        for i in range(0, len(income_statement_growth_df.SALES_GROWTH.values.tolist())):
            income_statement_growth_dict[f"SALES_GROWTH_{income_statement_growth_df.YEAR.values.tolist()[i]}"] = [
                income_statement_growth_df.SALES_GROWTH.values.tolist()[i]]

        for i in range(0, len(income_statement_growth_df.NET_INCOME_GROWTH.values.tolist())):
            income_statement_growth_dict[f"NET_INCOME_GROWTH_{income_statement_growth_df.YEAR.values.tolist()[i]}"] = [
                income_statement_growth_df.NET_INCOME_GROWTH.values.tolist()[i]]

        self.__income_statement_growth_df_v2 = pd.DataFrame(
            income_statement_growth_dict)
        self.__income_statement_growth_df_v2['Company'] = self.__symbol

        return self.__income_statement_growth_df_v2

    def income_statement_calculation(self):
        """Function to calculate relevant metrics from the income statement of whatever company symbol specified."""

        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.__symbol}&apikey={self.__access_key}'
        response = requests.get(url)
        income_statement_data = response.json()
        total_revenue = []
        for i in income_statement_data['annualReports']:
            total_revenue.append(
                (i['fiscalDateEnding'][:4], i['totalRevenue'], i['netIncome']))

        income_statement_df = pd.DataFrame(total_revenue, columns=[
            'YEAR', 'TOTAL_REVENUE', 'NET_INCOME'])

        income_statement_df[['TOTAL_REVENUE', 'NET_INCOME']] = income_statement_df[['TOTAL_REVENUE', 'NET_INCOME']].astype(
            float)

        income_statement_df['MARGIN'] = income_statement_df['NET_INCOME'] / \
            income_statement_df['TOTAL_REVENUE']

        income_statement_df['MARGIN'] = income_statement_df['MARGIN'].apply(
            '{:.2%}'.format)

        income_statement_dict = {}

        for i in range(0, len(income_statement_df.MARGIN.values.tolist())):
            income_statement_dict[f"MARGIN_{income_statement_df.YEAR.values.tolist()[i]}"] = [
                income_statement_df.MARGIN.values.tolist()[i]]

        self.__income_statement_df_v2 = pd.DataFrame(income_statement_dict)
        self.__income_statement_df_v2['Company'] = self.__symbol

        return self.__income_statement_df_v2

    def balance_sheet_calculation(self):
        """Function to calculate relevant metrics from the income statement of whatever company symbol specified."""

        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.__symbol}&apikey={self.__access_key}'
        response = requests.get(url)
        balance_sheet_data = response.json()

        working_capital = []
        for i in balance_sheet_data['annualReports']:
            working_capital.append(
                (i['fiscalDateEnding'][:4], i['totalCurrentAssets'], i['totalCurrentLiabilities']))

        balance_sheet_df = pd.DataFrame(working_capital, columns=[
            'YEAR', 'CURRENT_ASSETS', 'CURRENT_LIABILITIES'])

        balance_sheet_df[['CURRENT_ASSETS', 'CURRENT_LIABILITIES']] = balance_sheet_df[['CURRENT_ASSETS', 'CURRENT_LIABILITIES']].astype(
            float)

        balance_sheet_df['WORKING_CAPITAL'] = balance_sheet_df['CURRENT_ASSETS'] / \
            balance_sheet_df['CURRENT_LIABILITIES']

        balance_sheet_df['WORKING_CAPITAL'] = balance_sheet_df['WORKING_CAPITAL'].apply(
            '{:.2f}'.format)

        balance_sheet_dict = {}

        for i in range(0, len(balance_sheet_df.WORKING_CAPITAL.values.tolist())):
            balance_sheet_dict[f"WORKING_CAPITAL_{balance_sheet_df.YEAR.values.tolist()[i]}"] = [
                balance_sheet_df.WORKING_CAPITAL.values.tolist()[i]]

        self.__balance_sheet_df_v2 = pd.DataFrame(balance_sheet_dict)
        self.__balance_sheet_df_v2['Company'] = self.__symbol

        return self.__balance_sheet_df_v2

    def final_df(self):

        self.final_df = pd.merge(self.__df, self.__balance_sheet_df_v2,
                                 on='Company', how='left')

        self.final_df = pd.merge(
            self.final_df, self.__income_statement_growth_df_v2, on='Company', how='left')

        self.final_df = pd.merge(
            self.final_df, self.__income_statement_df_v2, on='Company', how='left')

        return self.final_df
