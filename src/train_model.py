import os

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

months = [
    "jan", "feb", "mar", "apr",
    "may", "jun", "jul", "aug",
    "sep", "oct", "nov", "dec"
]
years = [ "2011" , "2012" , "2013" ]

prev_day = 1

with open(os.getcwd()+"/data/processed_data.csv" , "w") as data_proc:
    data_proc.writelines(f"state,year,month,reading\n")
    for year in years:
        for month in months:
            print( month , year )
            with open(f'{os.getcwd()}/data/extracted/state_data/by_month{year}/3260{month}{year}.dat') as data_file:
                for line in data_file:
                    header = line[:30]
                    if "QGAG" not in header:
                        continue
                    readings = line[30:].split()
                    state = int(header[3:5])
                    month = int(header[21:23])
                    day = int(header[23:27])
                    if day-prev_day > 1:
                        for i in range(day-prev_day):
                            data_proc.writelines(f"{state},{year},{month},{0}\n")
                    for index in range(1,len(readings),2):
                        try:
                            reading = int(readings[index])
                            data_proc.writelines(f"{state},{year},{month},{reading}\n")
                        except:
                            pass
                    prev_day = day

df= pd.read_csv(os.getcwd()+'/data/processed_data.csv')
df.info()

X = df.iloc[:,0:3].values
y = df.iloc[:,3].values

regressor = RandomForestRegressor(n_estimators=20, random_state=0, oob_score=True, n_jobs=-1)

regressor.fit(X, y)

joblib.dump(regressor, os.getcwd()+'/model/random_forest_regressor_model.pkl')