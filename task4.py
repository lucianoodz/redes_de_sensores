#Integrantes grupo 12: Luciano Ortiz de Zárate - Matías Castillo - Franco Fierro
import requests
import pandas as pd
import time

# Función que permite realizar la escritura en thingSpeak
def postThingSpeak(field1, field2, field3, field4):
    apiKey = "8QWGE6MDCHODF0T9"
    r = requests.get(f"https://api.thingspeak.com/update?api_key={apiKey}&field1={field1}&field2={field2}&field3={field3}&field4={field4}")
    return r

# Función para pasar formato de horas hh:mm:ss a solo cantidad de horas como número flotante
def hoursCalculated(hhmmss):
    totalHours = 0.0
    splitOfHhmmss = hhmmss.split(':')
    totalHours = float(splitOfHhmmss[0])*1 + float(splitOfHhmmss[1])/60 +float(splitOfHhmmss[2])/3600
    return totalHours

# Función que limpia el dataset y envía los datos para ser escritos en thingSpeak
def postExecution():
    # Limpieza de dataset
    dataFrame = pd.read_csv("ChargePoint_Data_CY20Q4.csv")
    interestColumns = ['User ID','Start Date', 'End Date', 'Total Duration (hh:mm:ss)','Charging Time (hh:mm:ss)','Energy (kWh)','Latitude','Longitude']
    evse1Data = dataFrame[dataFrame['EVSE ID']==4.358300e+04]
    evse1Data = evse1Data[interestColumns].copy()
    evse1Data['Start Date'] = evse1Data['Start Date'].astype('datetime64[ns]')
    evse1Data['End Date'] = evse1Data['End Date'].astype('datetime64[ns]')
    evse1Data = evse1Data.sort_values(by=['Start Date'], ascending=False)
    # Número de envíos de datos
    for i in range(15):
        row = evse1Data.sample()
        # latitud = row['Latitude']     #En caso de querer enviar la latitud y longitud del EVSE
        # longitud = row['Longitude']
        latitud = 29.97416777 
        longitud = 31.1339477975
        tiempoCarga = row['Charging Time (hh:mm:ss)']
        energia = row['Energy (kWh)']
        r = postThingSpeak(latitud, longitud, hoursCalculated(tiempoCarga.values[0]), float(energia.values))
        print(r)
        time.sleep(15)

postExecution()