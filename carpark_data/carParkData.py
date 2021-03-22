import pandas as pd
import requests
from datetime import datetime, timedelta
from configparser import ConfigParser
config=ConfigParser(allow_no_value=True)
config.read('config.cfg')
date = config['dateTime']['date']
time = config['dateTime']['time']
shifter = config['dateTime']['shifter']
lot_threshold = config['dataFilter']['utilization_percentage']
totallots_quantile = config['dataFilter']['totallots_quantile']
size_report_name = config['reportPath']['size_name']
util_report_name = config['reportPath']['util_name']

i=0
dateshift = []
date_time_obj = datetime.strptime(date, '%Y-%m-%d')
for i in range(0,int(shifter)):
    date_time_shift= date_time_obj - timedelta(days=int(i-1))
    dateshift.append(date_time_shift)
    url = 'https://api.data.gov.sg/v1/transport/carpark-availability?date_time='+ str(date_time_shift)[:10] + 'T'+ time[:2] +'%3A'+ time[-2:]+'%3A00'
    print(url)
    data = requests.get(url).json()['items']
    if i == 0:
        # data transform on json input
        dfapi = pd.json_normalize(data, 'carpark_data', errors='ignore')
        dfapi['total_lots'] = dfapi['carpark_info'].apply(lambda x: x[0]['total_lots'])
        dfapi['lot_type'] = dfapi['carpark_info'].apply(lambda x: x[0]['lot_type'])
        dfapi['lots_available'] = dfapi['carpark_info'].apply(lambda x: x[0]['lots_available'])
        dfapi = dfapi.drop(['carpark_info'], axis=1)
        dfapi = dfapi.rename(columns={'carpark_number': 'car_park_no'}, inplace=False)
    elif int(shifter) > 0:
        dfapi2 = pd.json_normalize(data, 'carpark_data', errors='ignore')
        dfapi2['total_lots'] = dfapi2['carpark_info'].apply(lambda x: x[0]['total_lots'])
        dfapi2['lot_type'] = dfapi2['carpark_info'].apply(lambda x: x[0]['lot_type'])
        dfapi2['lots_available'] = dfapi2['carpark_info'].apply(lambda x: x[0]['lots_available'])
        dfapi2 = dfapi2.drop(['carpark_info'], axis=1)
        dfapi2 = dfapi2.rename(columns={'carpark_number': 'car_park_no'}, inplace=False)
        dfapi = dfapi.append(dfapi2)

#reading csv
data_file = 'hdb-carpark-information.csv'
csv = pd.read_csv(data_file)
dfcsv = pd.DataFrame(csv)
filt = (dfcsv['type_of_parking_system'].str.contains('ELECTRONIC')) & (dfcsv['short_term_parking'].str.contains('WHOLE DAY'))
dfcsv_filter = dfcsv.loc[filt]
# dfcsv_filter.to_excel(r'/Users/brandonwong/Desktop/pycharm/Projects/CarParkAvailability/filter.xlsx',index=False,header=True)

#merging data sets
dfmergecol = pd.merge(dfapi,dfcsv_filter, on='car_park_no',how='left')
dfmergecol = dfmergecol.dropna(subset = ['type_of_parking_system'], inplace = False)
dfmergecol['update_date']=dfmergecol['update_datetime'].astype('string')
dfmergecol['update_date'] = dfmergecol['update_date'].apply(lambda x: x[:10])
# dfmergecol.to_excel(r'/Users/brandonwong/Desktop/pycharm/Projects/CarParkAvailability/dataset_merge.xlsx',index=False,header=True)
