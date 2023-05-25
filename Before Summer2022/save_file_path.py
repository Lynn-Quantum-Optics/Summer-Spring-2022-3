import os.path
import datetime


base_path = "C:\\Users\\lynnlab\\Desktop" 
date = datetime.date.today()
months = ["Jan", "Feb", "Mar", "Apr", "May","Jun", "Jul","Aug","Sep","Oct"
    , "Nov", "Dec"]

def UV_HWP_Query():
    while True:
        try:
            entry = input('What is the current angle of the UV HWP (degrees)?')
            UV_HWP_Angle = float(entry)
            break
        except ValueError:
            print('not a valid floating point number')
        print()
    return UV_HWP_Angle

def QP_Query():
    while True:
        try:
            print('The base rotation of the Quartz Plate is read off the dial'
            + ' that rotates in the plane of the optical table')
            entry = input('What is the current angle of the base rotation of'
            + ' the Quartz Plate (degrees)?')
            QP_Angle = float(entry)
            break
        except ValueError:
            print('not a valid floating point number')
        print()
    return QP_Angle
    
def PCC_Query():
    while True:
        try:
            entry = input('What is the current angle of the Precompensation'
            + 'Crystal (degrees)?')
            PCC_Angle = float(entry)
            break
        except ValueError:
            print('not a valid floating point number')
        print()
    return PCC_Angle
    
def Experiment_Query():
    while True:
        try:
            query ='What is the name of the type of scan you are about to run?'
            query += "\n"+" (Full Tomography, Steering Measurement,"
            query += " Purity, HV Basis, Bell, Diagonal Smileyface,"
            query += " Antidiagonal Sailboat, etc.?) "
            entry = input(query)
            experimentName = str(entry)
            while " " in experimentName: # Replace spaces with underscores
                experimentName = experimentName.replace(" ", "_")
                print(experimentName)
            break
        except ValueError:
            print('not a valid experimental name string')
        print()
    return experimentName

def getFolderName():
    day = date.day
    m = date.month # goes from 1 to 12
    year = date.year
    monthString = months[m-1] # Indexed starting at 0.
    return monthString + " " + str(day) + " " + str(year)
    
def baseToSaveFolder(**kwargs):
    local_BP = base_path
    print(local_BP)
    # Swap getFolderName() and Experiment_Query() if it is more efficient
    # to save to an experiment folder and then the date as opposed to date
    # first and then the experiment.
    experimentname = "" # Initialize it.
    if 'userDefined' in kwargs:
        experimentName = kwargs["User Defined"]
    else:
        experimentName = Experiment_Query()
    relative = os.path.join("Measurements", getFolderName())
    relative = os.path.join(relative, experimentName)
    local_BP = os.path.join(local_BP, relative)
    return local_BP, experimentName
    # local_BP stands for local variable version of base_path.

def buildFilehead():
    PCC_Angle = PCC_Query()
    QP_Angle = QP_Query()
    UV_HWP_Angle = UV_HWP_Query()
    output = "UV_HWP "+str(UV_HWP_Angle)+" QP at "+str(QP_Angle)+" "+"PCC "
    # date.isoformat() yields "YYYY-MM-DD"
    output += str(PCC_Angle) + " " + date.isoformat() + " "
    return output
    
def correctedFileHead():
    filehead = str(buildFilehead())
    while "." in filehead:
        filehead = filehead.replace(".", "_")
        # The decimal char needs to be corrected to an underscore so that the
        # file extension can be read appropriately.
    return filehead
    
def FullBase(**kwargs):
    base = baseToSaveFolder(**kwargs)
    baseFilePath = base[0]
    experimentName = base[1]
    output = os.path.join(baseFilePath, correctedFileHead())
    return output, experimentName

def makeDirRecurHelper(directory, stackToAddBack):
    if len(stackToAddBack)!=0: # The stack has some elements remaining
        try:
            # directory is known to already exist 
            # so I need to add to it before calling mkdir
            directory = os.path.join(directory, stackToAddBack[-1])
            os.mkdir(directory)
            # The list object I am treating as a stack appends elements to the 
            # end. So the most recent addition is the last element in the list.
            # Therefore to pop the top off the stack: simply remove the last
            # element and make the list from 0 to -1 (inclusive, exclusive)
            stackToAddBack = stackToAddBack[:-1]
            print(stackToAddBack)
            return makeDirRecurHelper(directory, stackToAddBack)
        except OSError:
            if not os.path.isdir(directory):
                raise # This should raise the OSError that was caught.
    else:
        return directory # The recursive task has been completed.
        

def makeDir(fullPath):
    # Assume that full path includes a file name and extension.
    directory = os.path.dirname(fullPath)
    filename = os.path.split(fullPath)[1] 
    # File name is in the 1st & dir in the 0th indices respectively.
    stackToAddBack = []
    while os.path.isdir(directory) == False:
        # isdir only returns true if the directory exists.
        splitname = os.path.split(directory) # Go back a folder
        stackToAddBack += [splitname[1]]
        directory = splitname[0]
        
    makeDirRecurHelper(directory, stackToAddBack)
    
    return
    
    

def CompleteFilePath(State, samples, basePath, numPrev):
    localtime = datetime.datetime.now().time() # HH:MM:SS.microseconds
    HHMM = str(localtime)[0:5]#There is a colon separating the hours and the minutes
    basePath += HHMM.replace(":", "") # replacing the colon with nothing.
    basePath += "-meas " + str(State) + " " + str(samples) + " samp at 10Hz"
    basePath += " t" +str(numPrev+1) + ".csv"
    
    makeDir(basePath)
    
    with open(basePath, "w+") as file:
        # Warning this will overwrite any file that his been already created.
        # which should not happen because every file should have a unique name.
        # It is not entirely guaranteed for the files to have unique names
        # unless only one computer is running the script at a time.
        file.close()
    return basePath
