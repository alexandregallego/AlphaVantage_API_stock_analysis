from CompanyAnalysis import CompanyAnalysis
import pandas as pd
import time

list_of_companies = ['MSFT']

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
    final_df = pd.concat([per_ratio_df, working_capital_df, sales_growth_df,
                         net_income_df, roe_df, roa_df, margin_df], axis=1)
    # if company_analysis_df.shape[0] < 1:
    company_analysis_df = pd.concat(
        [company_analysis_df, final_df], axis=0)
    # else:
    #    company_analysis_df = pd.concat(
    #        [company_analysis_df, final_df])
    company_analysis.sales_growth_graph()
    time.sleep(65)

company_analysis_df.to_csv('Company_analysis.csv')
