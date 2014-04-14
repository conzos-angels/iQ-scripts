# Program to get laser hours from a standard 405,488,561(not Gen3),640 ALC set-up

def coherent():
	# Initialise COM Port
	port=serial.Serial(comport,baud, timeout=3)
	# Write to laser
	port.write('?HH\r'.encode('latin-1'))
	# Wait
	time.sleep(1)
	# Print the laser hours	
	print(comport, ':    ' + port.read(10).decode('latin-1'))
	# Close COM Port
	port.close()
	
def cobolt():
	# Initialise COM port
	port=serial.Serial(comport,baud, timeout=3)
	port.write('hrs?\r'.encode('latin-1'))
	# Wait
	time.sleep(1)	
	# Print the laser hours	
	print(comport, ':   ' + port.read(10).decode('latin-1'))
	# Close COM Port
	port.close()
	
import time
import serial
# Set Baud
baud=19200
# Check coherent 405 hours
comport='COM201'
coherent()
# Check coherent 488 hours
comport='COM202'	
coherent()
# Check cobolt 561 hours, not Gen3
comport='COM203'	
cobolt()
# Check coherent 640 hours
comport='COM204'	
coherent()
