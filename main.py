from CompanyAnalysis import CompanyAnalysis
import pandas as pd
import time
import os

new_folder_path_2 = 'ANALYSIS_RESULTS/'
list_of_companies = ['MSFT', 'AAPL']

company_analysis_df = pd.DataFrame()
for i in list_of_companies:
    company_analysis = CompanyAnalysis(symbol=i, access_key='QV6GB9465BJSYTEE')
    company_analysis.income_statement_load()
    company_analysis.balance_sheet_load()
    roe_df = company_analysis.return_on_equity_calculation()
    working_capital_df = company_analysis.working_capital_calculation()
    roa_df = company_analysis.return_on_assets_calculation()
    sales_growth_df = company_analysis.sales_growth()
    per_ratio_df = company_analysis.per_ratio_calculation()
    net_income_df = company_analysis.net_income_growth()
    margin_df = company_analysis.margin_calculation()
    final_df = pd.concat([per_ratio_df, working_capital_df, sales_growth_df,
                         net_income_df, roe_df, roa_df, margin_df], axis=1)
    # if company_analysis_df.shape[0] < 1:
    company_analysis_df = pd.concat(
        [company_analysis_df, final_df], axis=0)
    # else:
    #    company_analysis_df = pd.concat(
    #        [company_analysis_df, final_df])
    company_analysis.sales_growth_graph()
    company_analysis.net_income_graph()
    company_analysis.working_capital_graph()
    company_analysis.return_on_equity_graph()
    company_analysis.return_on_assets_graph()
    company_analysis.margin_graph()
    time.sleep(65)

if not os.path.exists(new_folder_path_2):
    os.makedirs(new_folder_path_2)
    company_analysis_df.to_csv(f'{new_folder_path_2}COMPANY_ANALYSIS.csv')
    print(f'Created new folder: {new_folder_path_2}')
else:
    print(f'Folder {new_folder_path_2} already exists')
