from CompanyAnalysis import CompanyAnalysis
import pandas as pd
import time
import os

new_folder_path_2 = 'ANALYSIS_RESULTS/'
list_of_companies = ['MSFT', 'AAPL']

company_analysis_df = pd.DataFrame()
for i in list_of_companies:
    company_analysis = CompanyAnalysis(symbol=i, access_key='')
    company_analysis.income_statement_load()
    company_analysis.balance_sheet_load()
    roe_df = company_analysis.return_on_equity_calculation()
    working_capital_df = company_analysis.working_capital_calculation()
    roa_df = company_analysis.return_on_assets_calculation()
    sales_growth_df = company_analysis.sales_growth()
    per_ratio_df = company_analysis.per_ratio_calculation()
    net_income_df = company_analysis.net_income_growth()
    margin_df = company_analysis.margin_calculation()
    cash_df = company_analysis.cash_growth()
    final_df = pd.concat([per_ratio_df, working_capital_df, sales_growth_df,
                          net_income_df, roe_df, roa_df, margin_df, cash_df], axis=1)
    if company_analysis_df.shape[0] < 1:
        company_analysis_df = pd.concat(
            [company_analysis_df, final_df], axis=0)
    else:
        company_analysis_df = pd.concat(
            [company_analysis_df, final_df])
    company_analysis.sales_growth_graph()
    company_analysis.net_income_graph()
    company_analysis.working_capital_graph()
    company_analysis.return_on_equity_graph()
    company_analysis.return_on_assets_graph()
    company_analysis.margin_graph()
    company_analysis.cash_graph()
    time.sleep(65)

first_column = ['Company', 'PER ratio']
other_columns = sorted(
    list(company_analysis_df.columns.difference(first_column)))
df_to_load = company_analysis_df.reindex(first_column + other_columns, axis=1).sort_values(
    by=['MARGIN_2022', 'MARGIN_2021', 'ROE_2022', 'ROE_2021'], ascending=False)
if not os.path.exists(new_folder_path_2):
    os.makedirs(new_folder_path_2)
    df_to_load.to_csv(f'{new_folder_path_2}COMPANY_ANALYSIS.csv')
    print(f'Created new folder: {new_folder_path_2}')
else:
    print(f'Folder {new_folder_path_2} already exists')
