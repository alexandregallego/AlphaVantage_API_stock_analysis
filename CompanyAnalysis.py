import requests
import pandas as pd
import csv
import matplotlib.pyplot as plt


class CompanyAnalysis():
    def __init__(self, symbol: str = None, access_key: str = None):
        self.__symbol = symbol
        self.__access_key = access_key

    def trading_stocks_list(self):
        "Function to return active stocks in the last day."
        url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={self.__access_key}"
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            df = pd.DataFrame(my_list, columns=[
                              'TICKER', 'NAME', 'INDEX', 'TYPE_OF_ASSET', 'DATE', 'UNDEFINED', 'STATUS'])
            file_path = 'STOCKS_LIST/'
            df.to_csv(file_path + 'STOCKS.csv', index=False)

    def per_ratio_calculation(self):
        """Function to extract the PER ratio of whatever company symbol specified."""

        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.__symbol}&apikey={self.__access_key}'
        response = requests.get(url)
        self.__per_ratio = response.json()['PERatio']
        dictionary_init = {'Company': [
            self.__symbol], 'PER ratio': [self.__per_ratio]}
        self.__df = pd.DataFrame(dictionary_init)

        return self.__df

    def income_statement_load(self):
        """Function to load income statement data."""

        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.__symbol}&apikey={self.__access_key}'
        response = requests.get(url)
        income_statement_data = response.json()
        total_revenue = []
        for i in income_statement_data['annualReports']:
            total_revenue.append(
                (i['fiscalDateEnding'][:4], i['totalRevenue'], i['netIncome']))

        self.__income_statement_df = pd.DataFrame(total_revenue, columns=[
            'YEAR', 'TOTAL_REVENUE', 'NET_INCOME'])

        return self.__income_statement_df

    def balance_sheet_load(self):
        """Function to load balance sheet data."""

        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.__symbol}&apikey={self.__access_key}'
        response = requests.get(url)
        balance_sheet_data = response.json()

        balance_sheet = []
        for i in balance_sheet_data['annualReports']:
            balance_sheet.append((i['fiscalDateEnding'][:4], i['totalCurrentAssets'],
                                 i['totalCurrentLiabilities'], i['totalShareholderEquity'], i['totalAssets']))

        self.__balance_sheet_df = pd.DataFrame(balance_sheet, columns=[
                                               'YEAR', 'CURRENT_ASSETS', 'CURRENT_LIABILITIES', 'SHAREHOLDER_EQUITY', 'TOTAL_ASSETS'])

        return self.__balance_sheet_df

    def format_floats(column1, column2):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                df = func(self, *args, **kwargs)
                df[column1] = df[column1].astype(float)
                df[column2] = df[column1].pct_change(
                    periods=-1)
                df = df.dropna()
                df[column2] = df[column2].apply('{:.2%}'.format)
                dict = {}
                for i in range(0, len(df[column2].values.tolist())):
                    dict[f"{column2}_{df.YEAR.values.tolist()[i]}"] = [
                        df[column2].values.tolist()[i]]
                df_v2 = pd.DataFrame(dict)
                return df_v2
            return wrapper
        return decorator

    def percentage_calc_fmt(column1, column2, column3):
        def percentage_decorator(func):
            def wrapper(self, *args, **kwargs):
                df = func(self, *args, **kwargs)
                df[[column1, column2]] = df[[column1, column2]].astype(float)
                df[column3] = df[column1]/df[column2]
                if column3 != 'WORKING_CAPITAL':
                    df[column3] = df[column3].apply('{:.2%}'.format)
                else:
                    df[column3] = df[column3].apply('{:.2f}'.format)
                percentage_dict = {}
                for i in range(0, len(df[column3].values.tolist())):
                    percentage_dict[f"{column3}_{df.YEAR.values.tolist()[i]}"] = [
                        df[column3].values.tolist()[i]]
                df_v2 = pd.DataFrame(percentage_dict)
                return df_v2
            return wrapper
        return percentage_decorator

    @format_floats('NET_INCOME', 'NET_INCOME_GROWTH')
    def net_income_growth(self):
        """Function that will return net income growth for whatever company specified over the period from which
        data is available.
        """
        self.__net_income_df = self.__income_statement_df

        return self.__net_income_df

    @format_floats('TOTAL_REVENUE', 'SALES_GROWTH')
    def sales_growth(self):
        """Function that will return sales growth for whatever company specified over the period from which
        data is available.
        """

        self.__sales_df = self.__income_statement_df
        return self.__sales_df

    @percentage_calc_fmt('NET_INCOME', 'TOTAL_REVENUE', 'MARGIN')
    def margin_calculation(self):
        """
        Function that will return the margin for whatever company specified over the period from which
        data is available
        """

        self.__margin_df = self.__income_statement_df
        return self.__margin_df

    @percentage_calc_fmt('CURRENT_ASSETS', 'CURRENT_LIABILITIES', 'WORKING_CAPITAL')
    def working_capital_calculation(self):
        """
        Function that will return the margin for whatever company specified over the period from which
        data is available
        """

        self.__working_capital_df = self.__balance_sheet_df
        return self.__working_capital_df

    @percentage_calc_fmt('NET_INCOME', 'SHAREHOLDER_EQUITY', 'ROE')
    def return_on_equity_calculation(self):
        """
        Function that will return the return on equity for whatever company specified over the period from which
        data is available
        """

        df_income_statement = self.__income_statement_df
        df_balance_sheet = self.__balance_sheet_df
        self.__return_on_equity_df = pd.merge(
            df_balance_sheet, df_income_statement, on='YEAR', how='inner')

        return self.__return_on_equity_df

    @percentage_calc_fmt('NET_INCOME', 'TOTAL_ASSETS', 'ROA')
    def return_on_assets_calculation(self):
        """
        Function that will return the return on equity for whatever company specified over the period from which
        data is available
        """

        df_income_statement = self.__income_statement_df
        df_balance_sheet = self.__balance_sheet_df
        self.__return_on_assets_df = pd.merge(
            df_balance_sheet, df_income_statement, on='YEAR', how='inner')

        return self.__return_on_assets_df

    def sales_growth_graph(self):
        plt.bar(list(reversed(self.__income_statement_df['YEAR'].tolist())),
                list(reversed(self.__income_statement_df['TOTAL_REVENUE'].tolist())))
        plt.xlabel('YEAR')
        plt.ylabel('SALES')
        plt.title(self.__symbol + ' sales growth')
        plt.savefig(self.__symbol + '_sales_growth.png')
