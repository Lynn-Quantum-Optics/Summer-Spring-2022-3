import Motors.allmotors as am
from ccu_record_to_a_given_file import measure
import os
import datetime as dt
#from datetime import date
import csv
from buildDirectories import makeDir
import save_averages_out
import time

serial_numbers = [83811667, 83811904, 83811901, 83811646]    
Motors = am.AllMotors(serial_numbers) 
# The above will reset everything to its axis upon being called.
Alice_HWP = Motors.AHWP
Bob_HWP = Motors.BHWP
Alice_QWP = Motors.AQWP
Bob_QWP = Motors.BQWP

today = dt.date.today()
months = ["Jan", "Feb", "Mar", "Apr", "May","Jun", "Jul","Aug","Sep","Oct"
    , "Nov", "Dec"]


def setupAngleSweep(party):
    print('select start angle for ',party,':')
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
    
def buildFilenamehead(party):
    angleSet = setupAngleSweep(party)
    output = "BHWP and AHWP 2d steering sweep " + "BHWP at "
    return [output, angleSet]
 
def main():
	# This will run once at the beginning.
    baseFilename = "C:\\Users\\lynnlab\\Desktop"
    baseFilename = os.path.join(baseFilename, "Measurements")
    baseFilename = os.path.join(baseFilename, getFolderName())
    outofbuildA = buildFilenamehead('Alice')
    outofbuildB = buildFilenamehead('Bob')
    baseFilename = os.path.join(baseFilename, str(outofbuildA[0]))
    #print([baseFilename, outofbuildA, outofbuildB])
    return [baseFilename, outofbuildA, outofbuildB]

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



def clean(output):
    """ Takes a string with decimal points in it and returns
    that string with the decimal points replaced by underscores. """
    # Eliminate the decimal points in the filename assume
    # no file extension in the name.
    while "." in output:
        output = output.replace(".", "_")
    while ":" in output:
        output = output.replace(":", "_")
    return output
    
    
def sweep(numsamples):
    mainsoutput = main()
    build = mainsoutput[1::] # is of the form ["BHWP and AHWP 2d steering sweep BHWP at", [alice anglestuff], [bob anglestuff]
    # angleSet is len 3. start angle, end angle, step. 
    #print(build)
    angleSetA = build[0][1]
    angleSetB = build[1][1]
    
    baseFilename = mainsoutput[0]
        
    basePath = buildDirectory(baseFilename)
    basePathSummary = "C:\\users\\lynnlab\\Desktop"
    filenameSummary1 =  "anglesweep" + str(angleSetA) + str(angleSetB[1]) + "part1"
    filenameSummary2 =  "anglesweep" + str(angleSetA) + str(angleSetB[1]) + "part2"
    currtime = dt.datetime.now().time() # HH:MM:SS.microseconds
    currtime = clean(str(currtime))
    filenameSummary1 += " at " + currtime + ".csv"
    filenameSummary2 += " at " + currtime + ".csv"
    savefilepath1 = os.path.join(basePathSummary, filenameSummary1)
    savefilepath2 = os.path.join(basePathSummary, filenameSummary2)

    makeDir(savefilepath1)
    
    anglesA = LIST_ANGLES(*angleSetA)
    anglesB = LIST_ANGLES(*angleSetB) # Pass the angleSet as a positional
    # argument so that python knows to unpack it since everything is in
    # the proper order already. (start, end, step).
    
    outputDict = {}
    #data will hold comma separated values to go into summary file rows
    data = ""
    with open(savefilepath1, "w+") as csvfile1:

        #Write column labels for Alice's HWP settings into the summary file
        data = ""
        for z in anglesA:
            data += "," + str(z)
        #data = "Bob HWP" + "," + "Alice HWP" + "," + "C4 mean" + "," + "C4 uncertainty"
        row = ''
        row += "Alice HWP settings ->" + data + "," + "," + "(Uncertainties) Alice HWP settings ->" + data + "\n"
        csvfile1.write(row)

        for x in anglesB[0:len(anglesB)//2+1]: # Rotate Bob to this angle.
            # Reset the baseFilename variable
            baseFilename = basePath
            Bob_HWP.motor.move_to(x, True)
            #time.sleep(5)
            stringx = str(x).replace(".", "_")
            Bobs_info = stringx + "deg AHWP at "
            baseFilename += Bobs_info
            data = str(x) #to write Bob's HWP setting into summary file
            uncertainty_data = str(x)   
            for y in anglesA: # Rotate Alice to this angle.
                Alice_HWP.motor.move_to(y, True)
                Alice_info = str(y).replace(".","_")
                fileext = ".csv"
                
                Alicefext = Alice_info + fileext
                baseFilename += Alicefext
                print("This is the file name and location")
                print(baseFilename)
                
                
                with open(baseFilename, "w+", newline = "\n") as file:
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

                #linetowrite = str(angleKey)+" "+str(C4mean)+"\n"
                #csvfile1.write(linetowrite)

                #to write coincidence mean into the summary file
                #data = str(angleKey[0]) + "," + str(angleKey[1])
                data += "," + str(outputDict[angleKey][0])
                uncertainty_data += "," + str(outputDict[angleKey][1])

            

                # Remove Alice's information for next preparation for the next
                # file name.Convert to a string and then find and remove Alice_info
                stringFilename = str(baseFilename)
                # Use rfind since we know that her information will be closer 
                # to the end of the string.
                startindexofAliceinfo = stringFilename.rfind(Alice_info)
                baseFilename = stringFilename[:startindexofAliceinfo]

            #out of Alice's loop, so write the full row of data to summary file

            row = ''
            row += data + "," + "," + uncertainty_data + "\n"
            csvfile1.write(row)
            
            # Remove Bob's information in preparation for the next set of angles.
            stringFilename = str(baseFilename)
            startindexofBobinfo = stringFilename.rfind(Bobs_info)
            baseFilename = stringFilename[:startindexofBobinfo]
            
    # Out of both loops so the measurement is done.
    # Time to close the file
    # figure out how to save data from angleKey and outputDict to a csv file
        csvfile1.close()
        
    makeDir(savefilepath2)

    data = ""
    with open(savefilepath2, "w+") as csvfile2:

        #Write column labels for Alice's HWP settings into the summary file
        data = ""
        for z in anglesA:
            data += "," + str(z)
        #data = "Bob HWP" + "," + "Alice HWP" + "," + "C4 mean" + "," + "C4 uncertainty"
        row = ''
        row += "Alice HWP settings ->" + data + "," + "," + "(Uncertainties) Alice HWP settings ->" + data + "\n"
        csvfile2.write(row)

        for x in anglesB[len(anglesB)//2::]: # Rotate Bob to this angle.
            # Reset the baseFilename variable
            baseFilename = basePath
            Bob_HWP.motor.move_to(x)
            #time.sleep(5)
            stringx = str(x).replace(".", "_")
            Bobs_info = stringx + "deg AHWP at "
            baseFilename += Bobs_info
            data = str(x) #to write Bob's HWP setting into summary file
            uncertainty_data = str(x)   
            for y in anglesA: # Rotate Alice to this angle.
                Alice_HWP.motor.move_to(y, True)
                Alice_info = str(y).replace(".","_")
                fileext = ".csv"
                
                Alicefext = Alice_info + fileext
                baseFilename += Alicefext
                print("This is the file name and location")
                print(baseFilename)
                
                
                with open(baseFilename, "w+", newline = "\n") as file:
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

                #linetowrite = str(angleKey)+" "+str(C4mean)+"\n"
                #csvfile2.write(linetowrite)

                #to write coincidence mean into the summary file
                #data = str(angleKey[0]) + "," + str(angleKey[1])
                data += "," + str(outputDict[angleKey][0])
                uncertainty_data += "," + str(outputDict[angleKey][1])

            

                # Remove Alice's information for next preparation for the next
                # file name.Convert to a string and then find and remove Alice_info
                stringFilename = str(baseFilename)
                # Use rfind since we know that her information will be closer 
                # to the end of the string.
                startindexofAliceinfo = stringFilename.rfind(Alice_info)
                baseFilename = stringFilename[:startindexofAliceinfo]
            row = ''
            row += data + "," + "," + uncertainty_data + "\n"
            csvfile2.write(row)
            
            # Remove Bob's information in preparation for the next set of angles.
            stringFilename = str(baseFilename)
            startindexofBobinfo = stringFilename.rfind(Bobs_info)
            baseFilename = stringFilename[:startindexofBobinfo]
            
    # Out of both loops so the measurement is done.
    # Time to close the file
    # figure out how to save data from angleKey and outputDict to a csv file
        csvfile2.close()

    
        
        return 
            



