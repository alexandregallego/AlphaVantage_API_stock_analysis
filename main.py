from CompanyAnalysis import CompanyAnalysis
import pandas as pd
import time
import os

new_folder_path_2 = 'ANALYSIS_RESULTS/'
list_of_companies = ['MSFT']

company_analysis_df = pd.DataFrame()
for i in list_of_companies:
    company_analysis = CompanyAnalysis(symbol=i, access_key='QV6GB9465BJSYTEE')
    final_df = company_analysis.run()
    if company_analysis_df.shape[0] < 1:
        company_analysis_df = pd.concat(
            [company_analysis_df, final_df], axis=0)
    else:
        company_analysis_df = pd.concat(
            [company_analysis_df, final_df])
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
