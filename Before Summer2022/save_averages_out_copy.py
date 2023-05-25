# This is a script to write the output dictionary to a csv file
# Not done yet

import csv
import os
import datetime as dt
from buildDirectories import makeDir

date = dt.date.today() # Today's date is held in date.

experiments = { # A dictionary of all the experiments and the order in which
    # the states for that measurement should be presented.
    "Full_Tomography": ["HH", "VV", "HV", "VH", "DD", "AA", "DA", "AD", "RR",
    "LL", "RL", "LR", "HD", "VA", "HA", "VD", "HR", "VL", "HL", "VR", 
    "DH","AV", "DV", "AH", "DR", "AL", "DL", "AR", "RH", "LV", "RV", "LH",
    "RD", "LA", "RA", "LD"],
    "Purity": ["DD", "AA", "DA", "AD"],
    "HV_Basis": ["HH", "VV", "HV", "VH"],
    "Steering": ["DS","AS", "DZ", "AZ", "DB", "AB", "DP", "AP", 
    "HH", "VV", "HV", "VH", "DD", "AA", "DA", "AD", "SD", "SA", "ZD", "ZA",
    "BD", "BA", "PD", "PA"], # B = sailboat state P = sailboat perpendicular
    # S = smilely face state and Z = smilely face perpendicular state.
    "Circular": ["RR", "LL", "LR", "RL"],
    "Diagonal_Smileyface": ["DS","DZ","AS","AZ"],
    "Antidiagonal_Sailboat": ["AB","AP","DB","DP"],


    }
    

def save(outputdict, savefilepath, experimentName, headers = ["State", "Coincident Counts Average", "Coincident Counts Uncertainty"]):
    orderedstates = experimenttype(experimentName, outputdict)

    # Check if the file exists, and if not if the directory exists. If neither exist, then make the appropriate directory structure.
    stringName = str(savefilepath)
    if stringName[::-1].find(".") == -1:
        # You did not find any periods in the filename.
        raise ValueError("The filename that you input is not a file valid name. It does not contain a file extension. The filename you input is",savefilepath)
    makeDir(savefilepath)

    print("You are saving the full data set to")
    print(savefilepath)
    with open(savefilepath, "w+", newline = "\n") as csvfile:
        if len(headers) != 0:
            writehead(csvfile, headers, experimentName) 
            # Write the first row as headers
        loopcount = 0
        probBool = False
        singleBasis = ['Circular', 'HV_Basis', 'Purity']
        if experimentName in singleBasis:
            probBool = True
            total = 0
            dataList = list(outputdict.values())
            for i in range(len(dataList)):
                total += dataList[i][0]
            # These experiments only have 1 basis
        for state_ind in range(len(orderedstates)):
            state = orderedstates[state_ind]
            row = ""
            # Increment Loop count so that the data can be more easily read.
            if experimentName != "Calibration":
                if state_ind%4 == 0 and state_ind != 0:
                    # Add an extra newline for readability to separate the states
                    # by basis. It also enables easy data transfer to Summer_2018
                    # which holds the full tomography calculations.
                    row += "\n"
            row += str(state)
            data = "" # A blank string to hold the data to be separated by ','
            for x in outputdict[state]:
                data += "," + str(x)
            if probBool:
                data += "," + str(outputdict[state][0]/total) # outputdict[state][0] holds the coincindent counts which is what is used to calculate the probabilities.
                #Probability is that states counts/all counts in the basis.
            row += data + "\n"
            csvfile.write(row)

        csvfile.close() # We are done writing to the file so close it.
        # This way it can be opened in other editors like Excel or Origin.
    return

def getStateName():
    while True:
        try:
            entry = input('What is the name of the state you made?')

            name = str(entry)
            
            while "." in name:
                name = name.replace(".", "_")
            break
        except ValueError:
            print('Not a valid


                  state name')
        print()
    return name    
 
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

 
def saveData(outputdict, experimentName):
    basePath = "C:\\users\\lynnlab\\Desktop" 
    # Always start at the desktop so that the file can be easily found later.
    stateName = getStateName()
    filename = stateName + "-" + experimentName + " " + date.isoformat()
    currtime = dt.datetime.now().time() # HH:MM:SS.microseconds
    currtime = clean(str(currtime))
    
    filename += " at " + currtime + ".csv"
    savefilepath = os.path.join(basePath, filename)
    save(outputdict, savefilepath, experimentName)
    return
        
def writehead(csvfile, headers, experimentName):
    linetowrite = ""
    singleBasis = ['Circular', 'HV_Basis', 'Purity']
    if experimentName in singleBasis:
        headers += ["Probability of this State"]
    for x in headers:
        linetowrite += x + ","
    linetowrite += "\n" 
    # Add a newline character at the end 
    # so that the data will be below the headers.
    csvfile.write(linetowrite)
    
def experimenttype(experimentName, outputdict):
    """ This function takes in a string and returns the desired output list of 
    states in the order determined based upon the experiment name """
    
    if experimentName in experiments.keys():
        return experiments[experimentName]
    else:
        return outputdict.keys()
