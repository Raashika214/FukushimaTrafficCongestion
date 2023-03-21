import pandas as pd

columnNames = ('year', 'month', 'day', 'time', 'roadName', 'direction', 'dwLocation', 'dwLatitude', 'dwLongitude',
               'upLocation', 'upLatitude', 'upLongitude', 'allCount', 'heavyCongestion', 'lightCongestion',
               'averageLength', 'maxLength', 'congestionTime', 'congestionAmount', 'linkLength')

useColumns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23]

df = pd.read_csv('table2.csv', sep='[\t/ ]', engine='python', header=None, usecols=useColumns)
# print(df)
df.to_csv('table3.csv', sep=',', index=False, header=False)
df = pd.read_csv('table3.csv', header=None, names=columnNames)
print(df)
df.to_csv('table4.csv', sep=',', index=False)
# print(df.head())

# PSQL読み込み用に変換して保存。数分かかる。
from shapely.geometry import Point, LineString, Polygon
import geopandas

# 日本測地系から世界測地系に変換
def tky2wgs_approx(lon_tky, lat_tky):
    L = lon_tky - 135
    B = lat_tky - 35
    a00,a01,a02,a03,a04,a05,a10,a11,a12,a13,a14,a15 = -2.79648156e-03, -3.64571151e-05, -1.00958714e-06, -8.83091873e-05, -8.33002662e-07, 3.54561248e-07, 3.19774649e-03, -1.13997082e-04, -7.51313530e-07, 2.34640477e-05, 6.06731757e-07, 3.28340222e-07
    dL = a00+a01*B+a02*B**2+a03*L+a04*B*L+a05*L**2
    dB = a10+a11*B+a12*B**2+a13*L+a14*B*L+a15*L**2
    return lon_tky + dL, lat_tky + dB

# 度分秒60進法から10進法へ変換
def deg2dec(lon,lat):
    d,m,s = str(lat)[:2], str(lat)[2:4], str(lat)[4:6]
    b_lat = float(d) + float(m) / 60 + float(s) / 60 / 60
    d,m,s = str(lon)[:3], str(lon)[3:5], str(lon)[5:7]
    b_lng = float(d) + float(m) / 60 + float(s) / 60 / 60
    return b_lng, b_lat


for index, row in df.iterrows():
    try:
        # JARTIC度分秒60進法から10進法へ変換
        a_dw_lng, a_dw_lat = deg2dec(row['dwLongitude'], row['dwLatitude'])
        a_up_lng, a_up_lat = deg2dec(row['upLongitude'], row['upLatitude'])
    except:
        # print(index, row['senor_dw_lng'], row['senor_dw_lat'], row['senor_up_lng'], row['senor_up_lat'])
        print('error')

    # 道路区間リンク判別用IDとして記録残す
    # df.at[index, 'link_id'] = str(int(row['sensor_dw_longitude'])) + '-' + str(
    #     int(row['sensor_dw_latitude'])) + '-' + str(int(row['sensor_up_longitude'])) + '-' + str(
    #     int(row['sensor_up_latitude']))

    # 日本測地系から世界測地系に変換
    b_dw_lon, b_dw_lat = tky2wgs_approx(a_dw_lng, a_dw_lat)
    b_up_lon, b_up_lat = tky2wgs_approx(a_up_lng, a_up_lat)

    df.at[index, 'dwLongitude'] = b_dw_lon
    df.at[index, 'dwLatitude'] = b_dw_lat
    df.at[index, 'upLongitude'] = b_up_lon
    df.at[index, 'upLatitude'] = b_up_lat

df.to_csv('congestion.csv', sep=',', encoding="utf-8", header=False, index=False)