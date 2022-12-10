import serial
from datetime import datetime
import sys
import time
from pathlib import Path


port = "COM8"
file_ts = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
baud_rate = 9600  # In arduino, Serial.begin(baud_rate)
file_name = "pulse_ " + str(file_ts) + ".txt"
file_path = file_name
output_file = open(file_path, "w+")
# Abriendo la comunicacion serial
try:
    ser = serial.Serial(port, baud_rate)
except:
    print("\n\tInvalid port entered!\n")
    sys.exit()

datos={}
def lectura():
    tiempo=10
    lectura_per_second=(1/1000)*100
    while tiempo>0:
        line = ser.readline()
        #line=str(line)
        line = line.decode("utf-8")
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # line = line.decode("utf-8") #ser.readline returns a binary, convert to string
        try:
            valor=int(line)
            datos[ts]=valor
        except ValueError:
            print("Error de lectura")

        time.sleep(lectura_per_second)
        tiempo=tiempo-lectura_per_second



lectura()
print(datos)
print(len(datos))


folder_name = "database"

ruta_actual = Path.cwd()
print(ruta_actual)

ruta_db = ruta_actual.joinpath(folder_name)

existe_db: bool = ruta_db.exists()


if(not existe_db):
    ruta_db.mkdir()

file_name:str= "Muestra"
databasepath = Path(folder_name).joinpath(file_name)
print(databasepath)
with open(databasepath.resolve(), 'w') as f:
    for key, value in datos.items():
        f.write('%s;%s\n' % (key, value))
