import Motors.allmotors as am
from ccu_record_to_a_given_file import measure
import os
from datetime import date

serial_numbers = [83811667, 83811904, 83811901, 83811646]    
Motors = am.AllMotors(serial_numbers) 
# The above will reset everything to its axis upon being called.
Alice_HWP = Motors.AHWP
Bob_HWP = Motors.BHWP
Alice_QWP = Motors.AQWP
Bob_QWP = Motors.BQWP

today = date.today()
months = ["Jan", "Feb", "Mar", "Apr", "May","Jun", "Jul","Aug","Sep","Oct"
    , "Nov", "Dec"]


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
    assumed to be positive. It is gauranteed to be if step is entered from
    setupAngleSweep()"""
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
    
def getFolderName():
    day = today.day
    m = today.month # goes from 1 to 12
    year = today.year
    monthString = months[m-1] # Indexed starting at 0.
    return monthString + " " + str(day) + " " + str(year)
    
def buildFilenamehead():
    angleSet = setupAngleSweep()
    output = "BHWP and AHWP 2d steering sweep " + "BHWP at "
    return [output, angleSet]
 
def main():
	# This will run once at the beginning.
    baseFilename = "C:\\Users\\lynnlab\\Desktop"
    baseFilename = os.path.join(baseFilename, "Measurements")
    baseFilename = os.path.join(baseFilename, getFolderName())
    outofbuild = buildFilenamehead()
    baseFilename = os.path.join(baseFilename, str(outofbuild[0]))
    return [baseFilename, outofbuild]

def buildDirectory(baseFilename):
    directory = os.path.split(baseFilename)[0]
    basePath = os.path.split(baseFilename)[1]
    try: 
        os.mkdir(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise # This should raise the OSError that was caught.
    basePath = os.path.join(directory, basePath)
    return basePath
    
def sweep(numsamples):
    mainsoutput = main()
    build = mainsoutput[1]
    # angleSet is len 3. start angle, end angle, step. 
    # This is assumed to be a linear sweep.
    angleSet = build[1]

    baseFilename = mainsoutput[0]
        
    basePath = buildDirectory(baseFilename)
    
    angles = LIST_ANGLES(*angleSet) # Pass the angleSet as a positional
    # argument so that python knows to unpack it since everything is in
    # the proper order already. (start, end, step).
    
    outputDict = {}
    
    for x in angles: # Rotate Bob to this angle.
        # Reset the baseFilename variable
        baseFilename = basePath
        Bob_HWP.motor.move_to(x)
        stringx = str(x).replace(".", "_")
        Bobs_info = stringx + "deg AHWP at "
        baseFilename += Bobs_info
        for y in angles: # Rotate Alice to this angle.
            Alice_HWP.motor.move_to(y, True)
            Alice_info = str(y).replace(".","_")
            fileext = ".csv"
            
            Alicefext = Alice_info + fileext
            baseFilename += Alicefext
            print("This is the file name and location")
            print(baseFilename)
            
            
            with open(baseFilename, "w+") as file:
                # Warning this will overwrite any file that
                # his been already created, which should not happen because
                # every file should have a unique name. It is not entirely
                # guaranteed for the files to have unique names
                # unless only one computer is running the script at a time.
                file.close()
        
            # Get the code for the state of the angles being measured.
            angleKey = tuple([x, y]) # Bob is mentioned before Alice. 

            # Call the record function with the appropriate file location.
            datasummary = measure(numsamples, baseFilename)
        
            C4mean = datasummary[0][4]
            C4uncertainty = datasummary[1][4]
            outputDict[angleKey] = [C4mean, C4uncertainty]

            
            
            # Remove Alice's information for next preparation for the next
            # file name.Convert to a string and then find and remove Alice_info
            stringFilename = str(baseFilename)
            # Use rfind since we know that her information will be closer 
            # to the end of the string.
            startindexofAliceinfo = stringFilename.rfind(Alice_info)
            baseFilename = stringFilename[:startindexofAliceinfo]
        
        # Remove Bob's information in preparation for the next set of angles.
        stringFilename = str(baseFilename)
        startindexofBobinfo = stringFilename.rfind(Bobs_info)
        baseFilename = stringFilename[:startindexofBobinfo]
    
    # Out of both loops so the measurement is done.
    # Time to save the data.
    
    