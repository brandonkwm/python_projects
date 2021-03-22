import carParkData
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def util_data(thold):
    #take config file value threshold for lot utilization
    carParkData.dfgrouped = carParkData.dfmergecol.groupby('car_park_no')
    carParkData.dfmergecol['total_lots'] = carParkData.dfmergecol['total_lots'].astype(float)
    carParkData.dfmergecol['lots_available'] = carParkData.dfmergecol['lots_available'].astype(float)
    carParkData.dfmergecol['lot % utilization'] = round((carParkData.dfmergecol['total_lots']-carParkData.dfmergecol['lots_available']) / carParkData.dfmergecol['total_lots']*100,3)
    filtmerge = carParkData.dfmergecol['lot % utilization'] <= float(thold)
    dfutil_merge = carParkData.dfmergecol.loc[filtmerge].sort_values(by=['update_date','lot % utilization'], ascending=False)
    dfutil_merge = dfutil_merge[dfutil_merge['lot % utilization'] > 0] #filtering out bad data
    #year_filter = pd.to_datetime(dfutil_merge['update_date']).year() >= '2021' #filtering out outdated data
    #########to consider time series analysis of carpark availability within the day############
    #dfutil_merge = dfutil_merge.lo c[year_filter].sort_values(by=['update_date', 'lot % utilization'],ascending=False)
    dfutil_merge.to_excel(os.path.join(os.getcwd(),carParkData.util_report_name),index=False,header=True)
    dfutil_merge['update_date'] = pd.to_datetime(dfutil_merge['update_date'])
    dfutil_merge.plot(x='update_date', y='lot % utilization', kind='bar')
    plt.show()


def large_carpark_data(quant):
     dfsize = carParkData.dfmergecol.sort_values(by=['update_date','total_lots'],ascending=False)
     dfsize['total_lots percentile'] = round((dfsize['total_lots'] / dfsize['total_lots'].quantile(1.0))*100,3)
     filt = dfsize['total_lots percentile'] >= float(quant)
     dfsize_quantile = dfsize.loc[filt]
     dfsize_quantile = dfsize_quantile.drop_duplicates()
     dfsize_quantile = dfsize_quantile.sort_values(by=['car_park_no','update_date'],ascending=False)
     # dfsize_quantile.groupby(['car_park_no','update_date'])
     #dfsize_quantile.to_excel(os.path.join(os.getcwd(),carParkData.size_report_name),index=False, header=True)


util_data(carParkData.lot_threshold)
large_carpark_data(carParkData.totallots_quantile)

#drawing stacked
