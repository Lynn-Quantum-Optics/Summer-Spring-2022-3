#Calibrate Motors COPY

import save_file_path as save # save one file.
import Motors.allmotors as am # motor controller
import ccu_record_to_a_given_file as record # get the data from the instrument                                                          
import save_averages_out # save the averages in a unique file.                                              #####
import matplotlib.pyplot as plt # visualize the data at the end. No error bars plotted yet though.
import time
import save_file_path
import os.path
import datetime

base_path = "C:\\Users\\lynnlab\\Desktop" 
date = datetime.date.today()


# Choose a motor to vary. AHWP, BHWP, AQWP, BQWP.
options = ["AHWP", "BHWP", "BQWP", "AQWP"]
serial_numbers = [83811667, 83811904, 83811901, 83811646]
print("before")

Motors = am.AllMotors(serial_numbers)
print("after")

def chooseMotor():
    valid = False
    while(not(valid)):
        userin = input("Choose a motor to calibrate. (AHWP, BHWP, AQWP, BQWP.)")
        if not(userin in options):
            print("Try again")
        else:
            name = str(userin)
            for motor in Motors.motorList:                                                                                      
                if motor.name == name:
                    print("Found it")
                    return motor
            valid = True  
    
def getNumSamples():
    """ This portion of the code was written by Kye Shi so that it
     can interface with the ccu_record.py file."""
    samples = 25
    while True:
        try:
            print('# of samples:')
            entry = input('(default: 25) > ')
            if not entry:
                samples = 25

            samples = int(entry)

            if samples < 0:
                print('must be non-negative')
                continue

            break
        except ValueError:
            print('not a valid integer')
        print()
    return samples

def setupAngleSweep():
    print('select start angle:')
    start = 0
    while True:
        try:
            entry = input('(default: 0) > ').strip()

            if not entry:
                break

            start = float(entry)
            break

        except ValueError:
            print('please enter a valid number')

    print()

    print('select end angle:')
    end = 180
    while True:
        try:
            entry = input('(default: 180)> ').strip() 
            # remove any whitespace from the input.
            
            if not entry:
                break

            end = float(entry)

            break
        except ValueError:
            print('please enter a valid number')

    print()

    print('select step size:')
    step = 5
    while True:
        try:
            entry = input('(default: 5) > ').strip()

            if not entry:
                break

            step = float(entry)

            if step <= 0:
                print('step angle must be positive')
                continue

            break

        except ValueError:
            print('please enter a valid number')
    return [start, end, step]   

def LIST_ANGLES(start, end, step):
    """ The input angles are in degrees and so we need to reduce them mod 360
    to get values between 0 and 359. This should be able to go from the start
    angle to the end angle or from the end angle to the start angle. Step is
    assumed to be positive. It is guaranteed to be if step is entered from
    setupAngleSweep()
    
    Returns: A list of angles for the motor to step through.
    """
    newstart = start%360
    curr = newstart
    newend = end%360
    newstep = step%360
    upBool = True
    if newstart > newend:
        newstep *= -1 # Need to go backwards to get from start to end.
        upBool = False
        
    output = []
    while curr != newend:
        output += [curr]
        curr = (curr+newstep)
        endcondition_up = (upBool and curr >= newend)
        endcondition_going_down = (not upBool and curr<=newend)
        if endcondition_up or endcondition_going_down:
            curr = newend
    output += [newend]
    return output
        
def buildFilenamehead():
    angleSet = setupAngleSweep()
    output = "Calibrating " + "BHWP at "
    return [output, angleSet]      
    
def main():
    print("main")
    motorToCalibrate = chooseMotor()
    start, end, step = setupAngleSweep()
    print(start, end, step)
    AngleList = LIST_ANGLES(start, end, step)
    
    numSamples = getNumSamples()
    print("The list of angles to cover is ", AngleList)
     
    Motors.move_to("HH") # Calibrating by maxing HH. so move to measure HH.
    UVHWPAngle = save.UV_HWP_Query()
    PCCAngle = save.PCC_Query()
    QPAngle = save.QP_Query()
    setUp = "UV_HWP " + str(UVHWPAngle) + " PCC " + str(PCCAngle) + " QP " + str(QPAngle) + " "
    setUp = save_averages_out.clean(setUp) # remove "." from the angles and replace with "_".                                                           ###
    filepath = base_path +"\\" + str(date) + "\\Calibration\\" + setUp + str(motorToCalibrate.name) + " at "
    dataAvgoutdict = {}
    means = []
    growingAngleL = []
    plt.figure(1)
    plt.axis([0, 360, 0, 3500])
    plt.xlabel("Angles (degrees)")
    plt.ylabel("Coincidence Counts")
    plt.title("Calibration of " + str(motorToCalibrate) + " " + str(numSamples) + " samples at 10Hz")    
    for angle in AngleList:
        basePath = filepath
        filepath +=  str(angle) + ".csv" 
        # Save all the data from the each state in a unique file
        # and then save the averages and uncertainties to another file.

        save.makeDir(filepath) # make sure that the file exists. Otherwise make it and the directories to reach it.
        # this will overwrite any file at the same path.
        
        print("type of angle ", type(angle))
        print(angle)
        motorToCalibrate.move_to(angle)
        
        print("Waiting 5 seconds for everything to stabilize")
        time.sleep(5) # sleep 5 seconds so that everything can stabilize.
        

        datasummary = record.measure(numSamples, filepath)
        # datasummary is a list of two lists. The zeroth is the means 
        # and the first is the uncertainties in those means given
        # the number of data points taken.
        C4mean = datasummary[0][4]
        C4uncertainty = datasummary[1][4]
        
        dataAvgoutdict[angle] = [C4mean, C4uncertainty]
        means += [C4mean]
        growingAngleL += [angle]

        filepath = basePath
    #save_averages_out.saveData(dataAvgoutdict, experimentName)
    #save_averages_out.saveData(dataAvgoutdict, "Calibration")   #note for later: there is no experiment name "Calibration" in save_averages_out                                                      ###
    
    # Now we should write out the summary of the coincidence counts values to a file.
    direct = os.path.split(basePath) # The directory name is in output 0
    baseFilename = direct[1] # get the file name
    directory = direct[0]
    filename_for_full_data = "Recalibration of " + baseFilename + ".csv"

    filepath = os.path.join(directory, filename_for_full_data)

    save.makeDir(filepath)

    #save(outputDict, filepath, "By Hand")
    save(dataAvgoutdict, filepath, "By Hand")   #???? what is the save command?
    plt.plot(growingAngleL, means)
    plt.show()        
    return # exit the program.
    
