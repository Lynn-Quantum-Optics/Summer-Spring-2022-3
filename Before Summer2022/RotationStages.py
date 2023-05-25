import serial
#use this one

ser = serial.Serial("COM5", timeout = 2)

#don't forget to flush

#setting polarizers, not HWP - angle is twice as big

#note that module 1 is address 0

def close():
  #closes the serial port so we can open it in the next program
  ser.close()
  
def degreesToHex(degrees):
  #convert degrees to steps
  decimalSteps = degrees*(143360/360) #143360 steps per rotation
  
  #convert steps to hex
  decimalSteps = int(decimalSteps)
  hexSteps = hex(decimalSteps)
  
  #remove first two characters- 0x
  hexSteps = hexSteps[2:]

  #capitalize all letters 
  hexSteps = hexSteps.upper()

  #add zeroes to beginning
  zeroesNeeded = 8-len(hexSteps)
  zeroString = zeroesNeeded*'0'
  hexString = zeroString+hexSteps

  return hexString.encode()
  
def degreeByteToInt(byteInput): #to be used only for reading output of degrees
  stringHex = str(byteInput)
  print(stringHex)
  noHead = stringHex[5:-1] # delete b' + the header + '
  print("noHead", noHead)
  stringDegree = noHead.split("\\")[0]
  print("stringDegree", stringDegree)
  integer = int(stringDegree)
  degree = integer/398 #rough estimate based on Fitting Degrees data
  return degree
  

def moveRelative(degrees, serialPort = ser, motor = '0', report = False): 
  hexString = degreesToHex(degrees)

  #write this into serial
  ser.write(bytes(motor,'utf-8')+b'mr'+hexString)
  if report:
  #use function
    bits = ser.readall()
    return bits

def moveAbsolute(degrees, serialPort = ser, motor = '0', report = False): 
  hexString = degreesToHex(degrees)

  #write this into serial
  ser.write(bytes(motor,'utf-8')+b'ma'+hexString)
  if report:
  #use function
    bits = ser.readall()
    return bits

def homeClockwise(serialPort = ser, motor = '0', report = False):
  ser.write(bytes(motor,'utf-8')+b'ho0')
  if report:
  #use function
    bits = ser.readall()
    return bits

def homeCounterClockwise(serialPort = ser, motor = '0', report = False):
  ser.write(bytes(motor,'utf-8')+b'ho1')
  if report:
  #use function
    bits = ser.readall()
    return bits
    
def jogForward(serialPort = ser, motor = '0'):
  ser.write(bytes(motor,'utf-8')+b'fw')

def jogBackward(serialPort = ser, motor = '0'):
  ser.write(bytes(motor,'utf-8')+b'bw')
  
def getMotorInfo(serialPort = ser, motor = '0'):
  ser.write(bytes(motor,'utf-8')+b'i1')
  print(ser.readall())
  
def changeAddress(motor2, motor1 = '0', serialPort = ser):
  ser.write(bytes(motor1,'utf-8')+b'ca'+bytes(motor2,'utf-8'))
  
def saveData(motor, serialPort = ser):
  ser.write(bytes(motor,'utf-8')+b'us')
  print(ser.readall())
  
#check which addresses are being used
#for i in ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']:
 #    print(i)
#     getMotorInfo(motor = i)

