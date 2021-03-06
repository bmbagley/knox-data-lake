import boto3
import io
from io import StringIO
import censusdata
import pandas as pd


session = boto3.Session(profile_name='knoxhack')  # set keys in ~/.aws/credentials under profile
s3 = session.client('s3')
s3r = session.resource('s3')

knoxdata_bucket_name = 'knox-data-temp-bucket'
knox_census_bucket = 'knox-data-census'
pilot_filename = 'PILOT_summary.xlsx'
facad_filename = 'facade_grant_recipients.xls'


def read_xl_s3(bucket_name, file_name):
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = obj['Body'].read()
    return pd.read_excel(io.BytesIO(data), encoding='utf-8')


def write_csv_s3(df, bucket_name, file_name):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, index_label=False)
    s3_rsrc = session.resource('s3')
    s3_rsrc.Object(bucket_name, file_name).put(Body=csv_buffer.getvalue())


# Import Pilot & Facad data
# pilot_df = read_xl_s3(knoxdata_bucket_name, pilot_filename)
# facad_df = read_xl_s3(knoxdata_bucket_name, facad_filename)

# Import 1 year estimates by tract
# searching for single years
# censusdata.search('acs1', 2017, 'group', 'B25003')  # Tenure
# censusdata.printtable(censusdata.censustable('acs5', 2017, 'B25003'))

# censusdata.search('acs5', 2017, 'group', 'C17002')  # RATIO OF INCOME TO POVERTY LEVEL IN THE PAST 12 MONTHS
# censusdata.geographies(censusdata.censusgeo([('state', '47'), ('county', '093'), ('tract', '*')]), 'acs5', 2017)

for i in list(range(2010, 2018)):
    c_ratio = censusdata.download('acs5', i,
                                 censusdata.censusgeo([('state', '47'), ('county', '093'), ('tract', '*')]),
                        ['C17002_001E', 'C17002_002E', 'C17002_003E',
                         'C17002_004E', 'C17002_005E', 'C17002_006E',
                         'C17002_007E', 'C17002_008E'])
    c_ratio['census_tract'] = [(str(c_ratio.index[i]).split(',')[0].split(' ')[-1]) for i in list(range(len(c_ratio.index)))]

    c_ratio['percent_under_1'] = ((c_ratio.C17002_002E + c_ratio.C17002_003E)/c_ratio.C17002_001E)*100
    c_ratio['percent_over_1'] = ((c_ratio.C17002_004E + c_ratio.C17002_005E + c_ratio.C17002_006E + c_ratio.C17002_007E + c_ratio.C17002_008E)/c_ratio.C17002_001E)*100

    poverty_ratio = c_ratio[['census_tract', 'percent_under_1', 'percent_over_1']]
    # print(poverty_ratio.describe())
    write_filename_summary = '{}/{}/acs5_ratio_of_income_to_poverty_level_past_12_months_summary_{}.csv'.format(
        'acs5',
        'ratio_of_income_to_poverty_level_past_12_months', i)
    write_filename_raw = '{}/{}/acs5_ratio_of_income_to_poverty_level_past_12_months_raw_{}.csv'.format(
        'acs5',
        'ratio_of_income_to_poverty_level_past_12_months', i)
    # print(c_ratio.head())
    print(poverty_ratio.head())
    # print(write_filename_summary)
    # print(write_filename_raw)
    write_csv_s3(poverty_ratio, knox_census_bucket, write_filename_summary)
    write_csv_s3(c_ratio, knox_census_bucket, write_filename_raw)

# Tenure
for i in list(range(2010, 2018)):
    temp = censusdata.censustable('acs5', i, 'B25003')
    temp_vars = [i for i in temp]
    temp_names = [k['label'].replace('!!', '_').replace(' ', '_').replace(':', '').lower() for i, k in temp.items()]
    c_ratio = censusdata.download('acs5', i,
                                  censusdata.censusgeo([('state', '47'), ('county', '093'), ('tract', '*')]),
                                  temp_vars)
    tenure = c_ratio.copy()
    tenure.columns = temp_names
    tenure = tenure.drop(columns=[col for col in tenure.columns.tolist() if 'error' in col])
    for calc in tenure.columns.tolist()[1:]:
        bina = (tenure[calc] / tenure[tenure.columns.tolist()[0]])*100
        tenure[calc + '_percentage'] = round(bina, 2)

    tenure['census_tract'] = [(str(tenure.index[i]).split(',')[0].split(' ')[-1]) for i in list(range(len(tenure.index)))]
    acs_name = 'tenure'
    write_filename_summary = '{}/{}/acs5_{}_summary_{}.csv'.format(
        'acs5',
        acs_name, acs_name, i)
    write_filename_raw = '{}/{}/acs5_{}_raw_{}.csv'.format(
        'acs5',
        acs_name, acs_name, i)
    # print(write_filename_summary)
    # print(write_filename_raw)
    print(tenure.head())
    write_csv_s3(tenure, knox_census_bucket, write_filename_summary)
    write_csv_s3(c_ratio, knox_census_bucket, write_filename_raw)


#






