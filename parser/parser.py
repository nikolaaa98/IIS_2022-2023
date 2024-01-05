import pandas as pd
import numpy as np
import os

#funckija koja prolazi kroz polja koja su prazna i popunjava radi boljeg proracuna
def popuni_prazna_polja(podaci, col_name):
    for ind in podaci.index:
        if np.isnan(podaci[col_name][ind]):
            temp = podaci[col_name].iloc[ind:ind +10].dropna()
            podaci[col_name][ind] = temp.mean()
            
def popuni_prazna_polja_before(podaci, col_name):
    for ind in podaci.index:
        if np.isnan(podaci[col_name][ind]):
            temp = podaci[col_name].iloc[ind-5:ind +10].dropna()
            podaci[col_name][ind] = temp.mean()

def popuni_prazna_polja_above(podaci, col_name):
    for ind in podaci.index:
        if abs(podaci[col_name][ind]) > 60:
            temp = podaci[col_name].iloc[ind - 10:ind].mean()
            podaci[col_name][ind] = temp

def preuzmi_podatke(podaci):
    podaci['datetime'] = pd.to_datetime(podaci['datetime'])
    columns = ['humidity', 'feelslike', 'windgust', 'windspeed','winddir', 'sealevelpressure', 'cloudcover', 'visibility']

    for col in columns:
        popuni_prazna_polja(podaci, col)
    for col in columns:
        popuni_prazna_polja_before(podaci, col)

    return podaci

def cover_loads_for_explicit_year(podaci, putanja, godina):
    ind = 0
    lista = []

    for list in os.listdir(putanja):
        if godina not in list:
            continue

        for list_csv in os.listdir(putanja + '\\' + list):
            place = putanja + '\\' + list + '\\' + list_csv
            if godina not in place:
                continue
            data_frame1 = pd.read_csv(putanja + '\\' + list + '\\' + list_csv)
            data_frame1['Time Stamp'] = pd.to_datetime(data_frame1['Time Stamp'])
            data_frame1['Time Stamp'] = data_frame1['Time Stamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
            data_frame1['Time Stamp'] = pd.to_datetime(data_frame1['Time Stamp'],format='%Y-%m-%dT%H:%M:%S')

            data1 = function_to_better_cover(data_frame1)

            temp  = pd.merge(podaci, data1, on ='Time Stamp')
            lista.append(temp)
            ind += 1

    return  pd.concat(lista)


#funckija koja parsira vreme i kolona Name
def function_to_better_cover(data_frame1):
    data1 = data_frame1[data_frame1['Name'] == 'N.Y.C.']
    m = (data1['Time Stamp'].dt.minute == 0) & (data1['Time Stamp'].dt.second == 0)
    return data1[m]


#funckija koja ucita excel za sve godine (2018, 2019, 2020, 2021)
def prodji_kroz_godine(godine):

    for godina in godine:
        #ucitaj excel koji je za neku godinu (2018, 2019, 2020, 2021)
        putanja = 'C:/Users/User/Desktop/InteligentniSiste/IIS_2022-2023/Training Data/NYS Weather Data/New York City, NY/New York City, ... {}-01-01 to {}-12-31.csv'.format(godina,godina)
        podaci = pd.read_csv(putanja)
        kolona = podaci[ # izvuci iz excela samo kolone koje su mi bitne
            ['datetime', 'temp', 'feelslike', 'humidity', 'windgust', 'windspeed','winddir', 'sealevelpressure', 'cloudcover', 'visibility',
             'conditions']]
        kolona = preuzmi_podatke(kolona)
        kolona = kolona.rename(columns={'datetime' : 'Time Stamp'}) # mora da se promeni ime, zato se u drugom excelu zove Time Stamp
        putanjaNVSLoadData = 'C:/Users/User/Desktop/InteligentniSiste/IIS_2022-2023/Training Data/NYS Load  Data'
        kolona['Time Stamp'] = pd.to_datetime(kolona['Time Stamp'], format='%Y-%m-%dT%H:%M:%S') #transformisi datum u format koji nam odgovara

        result_for_year = cover_loads_for_explicit_year(kolona,putanjaNVSLoadData,godina)
        result_for_year.to_csv('packed_data_{}.csv'.format(godina))


#funckija koja prolazi kroz svaku godinu posebno (kroz svaki excel)
def prodji_kroz_godinu(podaci):

        kolona = podaci[
            ['datetime', 'temp', 'feelslike', 'humidity', 'windgust', 'windspeed','winddir', 'sealevelpressure', 'cloudcover', 'visibility',
             'conditions']]
        kolona = preuzmi_podatke(kolona)
        
        kolona = kolona.rename(columns={'datetime' : 'Time Stamp'})
        kolona['Time Stamp'] = pd.to_datetime(kolona['Time Stamp'], format='%Y-%m-%dT%H:%M:%S')
        
        return kolona


if __name__ == '__main__':
    lista_godina = ['2018','2019','2020','2021']
    prodji_kroz_godine(lista_godina)
