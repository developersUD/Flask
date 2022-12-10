import serial
from datetime import datetime
import sys
import time
from pathlib import Path
import os
import database


class CodigoArduino:
    ser = None
    port: str = None
    baud_rate: int = 9600  # In arduino, Serial.begin(baud_rate)

    file_ts = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    # file_name = "pulse_ " + str(file_ts) + ".txt"
    # file_path = file_name
    # output_file = open(file_path, "w+")

    def __init__(_self, puerto_arduino: str = "COM8"):

        _self.port = puerto_arduino

        try:
            _self.ser = serial.Serial(_self.port, _self.baud_rate)
            line = _self.ser.readline()
            print(line)

        except Exception as e:
            print("\n\tPuerto invalido !\n");
            print(e)

    def lectura(_self) -> dict:

        datos: dict = {}

        tiempo = 10
        lectura_per_second = (1 / 1000) * 100
        while tiempo > 0:
            line = _self.ser.readline()
            line = line.decode("utf-8")
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # line = line.decode("utf-8") #ser.readline returns a binary, convert to string

            try:
                valor = int(line)
                datos[ts] = valor
                _self.write_csv(valor, _self.file_ts)
            except ValueError:
                print("Error de lectura")

            time.sleep(lectura_per_second)
            tiempo = tiempo - lectura_per_second

        return datos

    def write_csv(_self, column2, column3):
        basedir = os.path.abspath(os.path.dirname(__file__))
        data_file = os.path.join(basedir, 'database/data.csv')
        with open(data_file, 'a') as f:
            line = f"{column2},{column3}\n"
            f.write(line)
            f.close()

        return True
