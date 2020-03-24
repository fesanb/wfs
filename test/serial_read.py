import serial

ser = serial.Serial('/dev/ttyS0', 19200)
while True:
	cc = str(ser.readline())
	print(cc[2:][:-5])
