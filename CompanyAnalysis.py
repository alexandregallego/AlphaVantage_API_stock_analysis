import requests
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os


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
                                 i['totalCurrentLiabilities'], i['totalShareholderEquity'], i['totalAssets'], i['cashAndShortTermInvestments']))

        self.__balance_sheet_df = pd.DataFrame(balance_sheet, columns=[
                                               'YEAR', 'CURRENT_ASSETS', 'CURRENT_LIABILITIES', 'SHAREHOLDER_EQUITY', 'TOTAL_ASSETS', 'CASH'])

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

    def bar_graph(column1, column2):
        def bar_graph_decorator(func):
            def wrapper(self, *args, **kwargs):
                df = func(self, *args, **kwargs)
                x = np.array(list(reversed(df[column1].tolist())))
                if column2 not in ['ROE', 'ROA', 'MARGIN']:
                    y = np.array(
                        list(reversed(df[column2].tolist()))).astype(float)
                else:
                    y = np.array([i.split('%')[0]
                                 for i in list(reversed(df[column2].tolist()))]).astype(float)
                    print(y)
                idx = np.argsort(x)
                x_sorted = x[idx]
                y_sorted = y[idx]
                plt.bar(x_sorted, y_sorted)
                plt.ylim(ymin=0)
                plt.xlabel(column1)
                plt.ylabel(column2)
                plt.title(self.__symbol + '' + column2)
                new_folder_path = f'GRAPHS/{self.__symbol}'
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                    print(f'Created new folder: {new_folder_path}')
                else:
                    print(f'Folder {new_folder_path} already exists')
                plt.savefig(
                    f'GRAPHS/{self.__symbol}/{self.__symbol}_{column2}.png')
                plt.close()
            return wrapper
        return bar_graph_decorator

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
        self.__net_income_df = self.__income_statement_df.copy()

        return self.__net_income_df

    @format_floats('TOTAL_REVENUE', 'SALES_GROWTH')
    def sales_growth(self):
        """Function that will return sales growth for whatever company specified over the period from which
        data is available.
        """

        self.__sales_df = self.__income_statement_df.copy()
        return self.__sales_df

    @format_floats('CASH', 'CASH_GROWTH')
    def cash_growth(self):
        """Function that will return sales growth for whatever company specified over the period from which
       data is available.
       """

        self.__cash_df = self.__balance_sheet_df.copy()
        return self.__cash_df

    @percentage_calc_fmt('NET_INCOME', 'TOTAL_REVENUE', 'MARGIN')
    def margin_calculation(self):
        """
        Function that will return the margin for whatever company specified over the period from which
        data is available
        """

        self.__margin_df = self.__income_statement_df.copy()
        return self.__margin_df

    @percentage_calc_fmt('CURRENT_ASSETS', 'CURRENT_LIABILITIES', 'WORKING_CAPITAL')
    def working_capital_calculation(self):
        """
        Function that will return the margin for whatever company specified over the period from which
        data is available
        """

        self.__working_capital_df = self.__balance_sheet_df.copy()
        return self.__working_capital_df

    @percentage_calc_fmt('NET_INCOME', 'SHAREHOLDER_EQUITY', 'ROE')
    def return_on_equity_calculation(self):
        """
        Function that will return the return on equity for whatever company specified over the period from which
        data is available
        """

        df_income_statement = self.__income_statement_df.copy()
        df_balance_sheet = self.__balance_sheet_df.copy()
        self.__return_on_equity_df = pd.merge(
            df_balance_sheet, df_income_statement, on='YEAR', how='inner')

        return self.__return_on_equity_df

    @percentage_calc_fmt('NET_INCOME', 'TOTAL_ASSETS', 'ROA')
    def return_on_assets_calculation(self):
        """
        Function that will return the return on equity for whatever company specified over the period from which
        data is available
        """

        df_income_statement = self.__income_statement_df.copy()
        df_balance_sheet = self.__balance_sheet_df.copy()
        self.__return_on_assets_df = pd.merge(
            df_balance_sheet, df_income_statement, on='YEAR', how='inner')

        return self.__return_on_assets_df

    @bar_graph('YEAR', 'TOTAL_REVENUE')
    def sales_growth_graph(self):
        sales_growth_graph_df = self.__income_statement_df.copy()
        return sales_growth_graph_df

    @bar_graph('YEAR', 'NET_INCOME')
    def net_income_graph(self):
        net_income_growth_graph = self.__income_statement_df.copy()
        return net_income_growth_graph

    @bar_graph('YEAR', 'WORKING_CAPITAL')
    def working_capital_graph(self):
        return self.__working_capital_df

    @bar_graph('YEAR', 'ROE')
    def return_on_equity_graph(self):
        return self.__return_on_equity_df

    @bar_graph('YEAR', 'ROA')
    def return_on_assets_graph(self):
        return self.__return_on_assets_df

    @bar_graph('YEAR', 'MARGIN')
    def margin_graph(self):
        return self.__margin_df

    @bar_graph('YEAR', 'CASH')
    def cash_graph(self):
        cash_graph = self.__balance_sheet_df.copy()
        return cash_graph
