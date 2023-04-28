from CompanyAnalysis import CompanyAnalysis
import pandas as pd
import time

list_of_companies = ['MSFT', 'AAPL', 'NVDA', 'AMD']

company_analysis_df = pd.DataFrame()
for i in list_of_companies:
    company_analysis = CompanyAnalysis(symbol=i, access_key='')
    company_analysis.per_ratio_calculation()
    company_analysis.income_statement_calculation()
    company_analysis.income_statement_growth_calculation()
    company_analysis.balance_sheet_calculation()
    company_analysis.final_df()
    if company_analysis_df.shape[0] < 1:
        company_analysis_df = pd.concat(
            [company_analysis_df, company_analysis.final_df], axis=0)
    else:
        company_analysis_df = pd.concat(
            [company_analysis_df, company_analysis.final_df])
    print(company_analysis_df)
    del company_analysis
    time.sleep(65)

company_analysis_df.to_csv('Company_analysis.csv')
