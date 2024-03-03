import json
import os

import pandas as pd
from shapely.geometry import Polygon, Point, MultiPolygon

state_codes = {
    'Alabama': 1,
    'Arizona': 2,
    'Arkansas': 3,
    'California': 4,
    'Colorado': 5,
    'Connecticut': 6,
    'Delaware': 7,
    'Florida': 8,
    'Georgia': 9,
    'Idaho': 10,
    'Illinois': 11,
    'Indiana': 12,
    'Iowa': 13,
    'Kansas': 14,
    'Kentucky': 15,
    'Louisiana': 16,
    'Maine': 17,
    'Maryland': 18,
    'Massachusetts': 19,
    'Michigan': 20,
    'Minnesota': 21,
    'Mississippi': 22,
    'Missouri': 23,
    'Montana': 24,
    'Nebraska': 25,
    'Nevada': 26,
    'New Hampshire': 27,
    'New Jersey': 28,
    'New Mexico': 29,
    'New York': 30,
    'North Carolina': 31,
    'North Dakota': 32,
    'Ohio': 33,
    'Oklahoma': 34,
    'Oregon': 35,
    'Pennsylvania': 36,
    'Rhode Island': 37,
    'South Carolina': 38,
    'South Dakota': 39,
    'Tennessee': 40,
    'Texas': 41,
    'Utah': 42,
    'Vermont': 43,
    'Virginia': 44,
    'Washington': 45,
    'West Virginia': 46,
    'Wisconsin': 47,
    'Wyoming': 48,
    'Not Used': 49,
    'Alaska': 50,
    'Hawaii': 51,
    'Puerto Rico': 66,
    'Virgin Islands': 67,
    'Pacific Islands': 91
}


def resolveState(long, lat):
    data = json.load(open(os.getcwd()+'/data/gz_2010_us_040_00_500k.json'))
    df = pd.DataFrame(data["features"])

    df['Location'] = df['properties'].apply(lambda x: x['NAME'])
    df['Type'] = df['geometry'].apply(lambda x: x['type'])
    df['Coordinates'] = df['geometry'].apply(lambda x: x['coordinates'])

    df_new = pd.DataFrame()

    for idx, row in df.iterrows():

        if row['Type'] == 'MultiPolygon':
            list_of_polys = []
            df_row = row['Coordinates']
            for ll in df_row:
                list_of_polys.append(Polygon(ll[0]))
            poly = MultiPolygon(list_of_polys)

        elif row['Type'] == 'Polygon':
            df_row = row['Coordinates']
            poly = Polygon(df_row[0])

        else:
            poly = None

        row['Polygon'] = poly
        df_new = pd.concat([df_new, pd.DataFrame([row])], ignore_index=True)

    df_selection = df_new.drop(columns=['type', 'properties', 'geometry', 'Coordinates'])

    point = Point(lat, long)
    state = df_selection.apply(lambda row: row['Location'] if row['Polygon'].contains(point) else None, axis=1).dropna()
    if len(state.tolist()) >= 1:
        return state_codes[state.tolist()[0]]
    return None
