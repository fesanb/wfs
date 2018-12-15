import serial

ser = serial.Serial('COM5', 19200)
while True:
     cc=str(ser.readline())
     print(cc[2:][:-5])