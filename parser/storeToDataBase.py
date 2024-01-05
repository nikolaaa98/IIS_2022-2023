import datetime

from modelWeather import Weather, store_to_database
import pandas as pd
from numpy import nan, isnan, pi, sin, cos

#funkcija koja vraca podatke koje procita 
def return_data_frame(path: str) -> pd.DataFrame:
    data_frame = pd.read_csv(path)
    return data_frame

# pokupi datume praznika iz excela i iz dataseta izbaci te vrednosti 
def oduzmi_praznike_iz_dataseta(data_frame):

    holiday_frame = pd.read_excel('C:/Users/User/Desktop/InteligentniSiste/IIS_2022-2023/Training Data/US Holidays 2018-2021.xlsx')
    data_frame['Date'] = pd.to_datetime(data_frame['Time Stamp'] ,format='%Y-%m-%d').dt.date
    holiday_frame['Date'] = pd.to_datetime(holiday_frame['Unnamed: 2']).dt.date
    data_frame = data_frame[~(data_frame['Date'].isin(holiday_frame['Date']))]
    return data_frame

#funkcija koja vraca da li je radni dan radan ili neradan (vikend)
def radni_dan(frame , year):
    help = frame
    help = help.groupby('Date').mean()
    help = help.drop([ 'temp', 'humidity', 'feelslike', 'windgust','winddir', 'windspeed', 'sealevelpressure',
                      'cloudcover', 'visibility','Unnamed: 0', 'PTID', 'Load'], axis =1)
    help['day'] = 0
    help['day_week'] = 0
    help['day_sin'] = 0
    help['day_cos'] = 0
    week_days = 0
    if year == '2019':
        week_days = 1
    if year == '2020':
        week_days = 2
    if year == '2021':
        week_days = 2

    for index in range(len(help)):
        day = 1
        if week_days % 6 == 0:
            day = 0
        if week_days % 7 == 0:
            week_days = 0
            day = 0

        help['day'][index] = day
        help['day_week'][index] = week_days
        help['day_sin'][index] = sin(2 * pi * week_days / 7)
        help['day_cos'][index] = cos(2 * pi * week_days / 7) # svaki dan se ponavlja u mesecu pa koristimo sin/cos

        week_days += 1

    frame = pd.merge(frame , help , on='Date')
    return frame

#dodajemo sin/cos satima i mesecima da bi program razumeo da se ponavaljaju 
def add_sin_cos(data_frame):
    hours = 24
    months = 12

    data_frame['sin_time'] = sin(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.hour / hours)
    data_frame['cos_time'] = cos(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.hour / hours)

    data_frame['sin_month'] = sin(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.month / months)
    data_frame['cos_month'] = cos(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.month / months)

    return data_frame

def yesterday_temp(data_frame):
    data_frame['yesterday_temperature'] = data_frame.temp.shift(-24)
    data_frame['day_bef_yesterday_temperature'] = data_frame.temp.shift(-48)
    data_frame['last_hour_temperature'] = data_frame.temp.shift(-1)
    data_frame['last_hour_load'] = data_frame.Load.shift(-1)
    return data_frame

#funckija koja popunjva nan vrednosti
def popuni(df, col_name):
    for ind in df.index:
        if isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind:ind + 5].dropna()
            df[col_name][ind] = temp.mean()

    for ind in df.index:
        if isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind:ind + 10].dropna()
            df[col_name][ind] = temp.mean()
    return  df

#funckija koja popunjva nan vrednosti
def popuni_before(df, col_name):
    for ind in df.index:
        if isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind-10:ind].dropna()
            df[col_name][ind] = temp.mean()

    for ind in df.index:
        if isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind-5:ind].dropna()
            df[col_name][ind] = temp.mean()
    return  df

#funckija koja popunjava null i nan vrednosti sa pravim vrednostima
def upisi_data_dataset(data):

    columns = ['temp', 'last_hour_temperature', 'yesterday_temperature', 'day_bef_yesterday_temperature', 'humidity', 'feelslike',
               'windgust', 'windspeed', 'sealevelpressure', 'cloudcover',
               'visibility','last_hour_load', 'Load']

    for item in columns:
        data = popuni(data, item)

    for item in columns:
        data = popuni_before(data, item)

    return  data

#funckija ucitava u bazu podatka ako je vrednost nan ili mu menja vrednost sa pravom vrednoscu
def ucitaj_u_bazu_podataka(data_frame):

    data = data_frame

    last_condition, last_load, feelslike, windgust, yesterday_load, winddir\
        ,yesterday_temp = "", 0, 0, 0, 0, 0 ,0
    list_hours = [0,1,2,3,4,5,6,7,22,23]
    winter_months =[12,1,2]
    spring_months =[3,4,5]
    summer_months =[6,7,8]
    autumn_months =[9,10,11]

    for index, row in data.iterrows():
        #logic to change conditions where is null
        row_dict = row.to_dict()
        #if something is nan from data set cover that
        if row_dict['windgust'] is nan:
            row_dict['windgust'] = windgust
        if row_dict['conditions'] is nan:
            row_dict['conditions'] = last_condition
        if row_dict['Load'] is nan:
            row_dict['Load'] = last_load
        if row_dict['feelslike'] is nan:
            row_dict['feelslike'] = feelslike
        row_dict['day_part'] = 1
        if pd.to_datetime(row_dict['Time Stamp']).hour in list_hours:
            row_dict['day_part'] = 0

        #year part :D
        if row['Date'].month in winter_months:
            row_dict['year_part'] = 0
        if row['Date'].month in spring_months:
            row_dict['year_part'] = 0.25
        if row['Date'].month in summer_months:
            row_dict['year_part'] = 0.5
        if row['Date'].month in autumn_months:
            row_dict['year_part'] = 1

        #temperature offset
        row_dict['temp_day'] = 1
        if row_dict['temp'] > 10 and row_dict['temp'] < 30: # ako je temp izmedju 10 i 30 ne treba nam grejanje ili hladjenje
            row_dict['temp_day'] = 0


        if row_dict['winddir'] is nan:
            row_dict['winddir'] = winddir

        row_dict['corona'] = 0
        helper = pd.to_datetime(row_dict['Time Stamp'])
        if datetime.date(helper.year,helper.month,helper.day) > datetime.date(2020,4,1):
            row_dict['corona'] = 1
        w = Weather(**row_dict)
        store_to_database(w)
        last_condition, feelslike, windgust, winddir , last_load =\
            row_dict['conditions'] ,  row_dict['feelslike'] , row_dict['windgust'] \
                , row_dict['winddir'], row_dict['Load'],


if __name__ == '__main__':

    lista_godina = ['2018','2019','2020','2021']
    
    for item in lista_godina:
        data = return_data_frame('C:/Users/User/Desktop/InteligentniSiste/IIS_2022-2023/packed_data_{}.csv'.format(item))
        # procitaj podatke u nekom vremenskom opsegu
        #data['Date'] = pd.to_datetime(data['Time Stamp'], format='%Y-%m-%d').dt.date
        
        #uzmi u obzir podatke kada su praznici, dani koji nisu radni itd...
        data = radni_dan(data, item)
        frame = oduzmi_praznike_iz_dataseta(data)

        frame = add_sin_cos(frame)
        frame = yesterday_temp(frame)
        
        data = upisi_data_dataset(frame)
        ucitaj_u_bazu_podataka(frame)
