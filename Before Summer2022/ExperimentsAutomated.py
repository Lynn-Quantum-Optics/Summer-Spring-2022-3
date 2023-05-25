"""
Wrapper for all the automated experiments
Full Tomography scans, Purity Scans, Steering Measurements
anything that moves the motors to states defined by 2 letters
where those 2 letters are in the alphabet 'HVADRLSBPZ' capital or lower-case.
"""
import time
import save_file_path as save
import Motors.allmotors as am
import ccu_record_to_a_given_file as record

serial_numbers = [83811667, 83811904, 83811901, 83811646]    

Motors = am.AllMotors(serial_numbers)

import save_averages_out

experimentStates = { "Full_Tomography": # This is a list of the states in the
        # order in which the measurements will take place. Underscores are used
        # to separate any words to avoid any potential problems with spaces on
        # different operating systems. We have not experienced any problems on
        # our Windows 7 machine.
        [ "LA", "RA", "VA", "HA", "DA", "AA",
        "AD", "DD", "HD", "VD", "RD",  "LD",
        "LH", "RH", "VH", "HH", "DH", "AH", 
        "AV", "DV", "HV", "VV", "RV", "LV",
        "LL", "RL", "VL", "HL", "DL", "AL",
        "AR", "DR", "HR", "VR", "RR", "LR"],
    "Witness": ["HH", "HV", "VH", "VV",  
                "DD", "DA", "AD", "AA",   
                "RR", "RL", "LR", "LL"], 
    "Purity": ["DD", "AA", "AD", "DA"],
    "Steering_Measurement": ["HH", "VV", "HV", "VH", "DD", 
        "DA", "AD", "AA", "DS", "DZ", "AS", "AZ", "SD", "ZD",
        "SA", "ZA", "BA", "PA", "BD", "PD", "DB", "DP", "AB","AP"],
    "HV_Basis": ["HH", "VV", "HV", "VH"],
    "Circular": ["RR", "LR", "LL", "RL"],
    "Bell": ["VP", "HB", "HP", "VB",
             "VZ", "HS", "HZ", "VS",
             "DP", "AB", "AP", "DB",
             "AZ", "DS", "DZ", "AS"],
    "Diagonal_Smileyface": ["DS","DZ","AS","AZ"],
    "Antidiagonal_Sailboat": ["AB","AP","DB","DP"]
    }

experiments = experimentStates.keys()
OrderedStates = []


def setupExperiment(**keyword_arguments):
    if 'states' in keyword_arguments:
        OrderedStates = keyword_arguments['states']
        ExperimentName = "User Defined"
        baseFilePath,ExperimentName=save.FullBase(userDefined = ExperimentName)
        return baseFilePath, ExperimentName, OrderedStates
    else:
        while True:
            baseFilePath, ExperimentName = save.FullBase()
            if ExperimentName in experiments:
                OrderedStates = experimentStates[ExperimentName]
                return baseFilePath, ExperimentName, OrderedStates
            else:
                print("Experiment could not be found. The valid options are: ")
                for key in experiments:
                    name = str(key)
                    while "_" in name:
                        name = name.replace("_", " ")
                    print(name)

def getNumSamples():
    """ This portion of the code was written by Kye Shi so that it
     can interface with the ccu_record.py file."""
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
                
def conductExperiment(setupCluster, sampleNumber):
    basePath = setupCluster[0]
    ExperimentName = setupCluster[1]
    OrderedStates = setupCluster[2]
    
    numSamples = sampleNumber
    
    outputdict = {} # Make an empty dictionary which will hold the output.
        
    # The move_to code handles the case where the motor is asked to move to
    # the position it was at in the previous state.
    for i in range(len(OrderedStates)):
        State = OrderedStates[i]
        # Motors object handles moving all the motors including Bob's QWP.
        Motors.move_to(State)
        
        print("Waiting 7 seconds for the measurement to stabilize")
        time.sleep(7) # Should sleep for 7 seconds before proceeding.
        
        print("Proceeding with the measurement.")
        # Call the measurement script with the number of samples as requested.
        numCalls = 0
        output_path = save.CompleteFilePath(State, numSamples,
            basePath,numCalls)
        datasummary = record.measure(numSamples, output_path)
        # datasummary is a list of two lists. The zeroth is the means 
        # and the first is the uncertainties in those means given
        # the number of data points taken.
        C4mean = datasummary[0][4]
        C4uncertainty = datasummary[1][4]
        
        outputdict[State] = [C4mean, C4uncertainty]
    return outputdict
    
    
def main(**kwargs):
    """ kwargs is an optional argument that if you pass the key 'states'
    with an associated value will allow the program to measure over 
    that user defined set of states. The states still need to be in the
    form of 2 uppercase letters from the set 'HVADRLSBPZ'.
    
    If you do not provide this argument it will ask you which predefined
    set of states you would like to use.
    """
    setupCluster = setupExperiment(**kwargs)
    
    experimentName = setupCluster[1] 
    # the experimentName is in the 1st index of the setupCluster. See above
    
    numSamples = getNumSamples()
    
    dataAvgoutdict = conductExperiment(setupCluster, numSamples)

    save_averages_out.saveData(dataAvgoutdict, experimentName)
    
    return dataAvgoutdict
    
main()
