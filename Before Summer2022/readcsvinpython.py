# Lorenzo Calvano
# 6/16/18

# Edits and additional annotations by Helen Chaffee 
# 7/2/2019
# To use this code, simply call get_datalist('filename')
# if you want to read from the file filename.csv.
# Only works for .csv files as far as I can tell.

# I annotate the helper functions with this data, step by step
# Test on the following matrix
#   V1  V2  V3  V4  V5  V6
# 0 11  12  13  14  15  16
# 5 21  22  23  24  25  26

import csv 

# From Helen: I comment out a lot of lines that were originally uncommented
# These lines are from when you would have to run readcsvinpython() to
# get python to get your datalist. I removed this feature because 
# I want to be able to call the functions to a certain filename, not 
# just "counts.csv"

#with open("counts.csv",newline="") as csvfile:
#    counts=csvfile.readlines()

# At this point,
# counts = [',V1,V2,V3,V4,V5,V6\r\n', '0,11,12,13,14,15,16\r\n', '5,21,22,23,24,25,26\r\n']
#print("Raw reading:",counts)

#newcountsfile=[]

def steering2(newcountsfile,counts): #does some formatting
    for row in range(1,len(counts)):
        newrow=counts[row].split() #The counts variable, coming directly from the .csv file, is a single list of strings
        newcountsfile.append(newrow)
    return newcountsfile
#steering2()

# At this points,
# newcountsfile = [[',V1,V2,V3,V4,V5,V6'], ['0,11,12,13,14,15,16'], ['5,21,22,23,24,25,26']]
# Commented out lines in the next command and added final statement to eliminate Bob's angle

#print("Make subindices",newcountsfile)



def steering3(newcountsfile,counts): #does some more formatting
    newnewcountsfile=[]
    for row0 in range(len(newcountsfile)):
        newnewcountsfile.append([]) #this new list is the same index as row0
        lastcomma=0 #keeps track of the last comma so each data point can be identified out of the string

        # Note from Helen: this "lastcomma" variable does not, in fact, 
        # seem to be related to the last comma in the string. Instead,
        # we will use lastnumber_index as the index location of the 
        # last comma, and lastnumber as the number following the last 
        # comma.

        lastnumber_index = newcountsfile[row0][0].rfind(',')    # Locates the 
        lastnumber = newcountsfile[row0][0][1+lastnumber_index:]    # lastnumber is type string, not float or int.

        for digit in range(len(newcountsfile[row0][0])-1): #we loop over the length minus 1 because we have a special case below for the last comma and data point
            if newcountsfile[row0][0][digit] == ',':
                newnewcountsfile[row0].append(newcountsfile[row0][0][lastcomma:digit])
                lastcomma = digit+1
                if ',' not in newcountsfile[row0][0][lastcomma:]:   # i.e., if no commas remain in the sublist, then we only have the last number to add
                    newnewcountsfile[row0].append(lastnumber)   
    for row in range(len(newnewcountsfile)):    # this loop removes the first element, which is the label for Bob's angle
        newnewcountsfile[row] = newnewcountsfile[row][1:]
    return newnewcountsfile
#newnewcountsfile=steering3()

# At this point,
# newnewcountsfile = [['0', '11', '12', '13', '14', '15','16'], ['5', '21', '22', '23', '24', '25','26']]

#print("Split string",newnewcountsfile)

#newnewcountsfile[0][0] = newnewcountsfile[0][0][1:] #There is some weird notation to get rid of at this specific index, coming from how the .csv data was transfered 
# From Helen: The line above does not seem to apply anymore

def steering5(newnewcountsfile): #makes each string a float 
    for row2 in range(len(newnewcountsfile)):    
        for numberr in range(len(newnewcountsfile[row2])):
            newnewcountsfile[row2][numberr] = float(newnewcountsfile[row2][numberr])
    return newnewcountsfile
#steering5()   #

# At this point,
# newnewcountsfile = [['0', '11', '12', '13', '14', '15','16'], ['5', '21', '22', '23', '24', '25',26']]

#countsL=newnewcountsfile #the data how we want it, a list of lists.
#print("The input for the one-way steering data analysis is stored in th variable 'countsL'")

def transpose(matrix):
    '''Transposes a matrix, ie a list of lists.'''
    transposeL=[]
    for i in range(len(matrix[0])): 
        newrow=[]
        for row in range(len(matrix)):
            newrow.append(matrix[row][i])
        transposeL.append(newrow)
    return transposeL

def get_datalist(filename):
    '''This function calls functions from
    earlier into one command. Only input the filename
    of the excel, in the format "filename". Do not 
    include the .csv extension, but include quotes'''
    with open(filename+".csv",newline="") as csvfile:
        counts=csvfile.readlines()
    #print("Raw reading:",counts)
    newcountsfile_1=[]
    newcountsfile_2 = steering2(newcountsfile_1,counts)
    #print("Make subindices",newcountsfile_1)
    newcountsfile_3 = steering3(newcountsfile_2,counts)
    #print("Split string",newcountsfile_2)
    countsL_Bob = steering5(newcountsfile_3)
    #print("Convert strings to floats",countsL)

    # Have made the countsL list for Bob. That is, we index like countsL_Bob[bobangle][aliceangle]
    # To make this nice for the analysis code, need a countsL that indexes like countsL_Alice[aliceangle][bobangle]

    countsL_Alice = transpose(countsL_Bob)

    return countsL_Bob,countsL_Alice


def get_datalist_no_transpose(filename):
    '''This function calls functions from
    earlier into one command. Only input the filename
    of the excel, in the format "filename". Do not 
    include the .csv extension, but include quotes'''
    with open(filename+".csv",newline="") as csvfile:
        counts=csvfile.readlines()
    #print("Raw reading:",counts)
    newcountsfile_1=[]
    newcountsfile_2 = steering2(newcountsfile_1,counts)
    #print("Make subindices",newcountsfile_1)
    newcountsfile_3 = steering3(newcountsfile_2,counts)
    #print("Split string",newcountsfile_2)
    countsL_Bob = steering5(newcountsfile_3)
    #print("Convert strings to floats",countsL)
    return countsL_Bob

def merge_phi_psi(phi_csvdata,psi_csvdata,phi_csverror,psi_csverror,V):
    """5 arguments: phi_csvdata, psi_csvdata, phi_csverror,
    psi_csverror, V.
    Reads directly from the csv file, no need to call get_datalist.
    This function returns similarly as the get_datalist
    function, in the sense that you call it like so:
    countsB, countsA, errorB, errorA = merge_phi_psi(.........)
    This function assumes that Bob is the steering party in the 
    input files."""
    phi_data = get_datalist_no_transpose(phi_csvdata)
    psi_data = get_datalist_no_transpose(psi_csvdata)
    phi_error = get_datalist_no_transpose(phi_csverror)
    psi_error = get_datalist_no_transpose(psi_csverror)
    dataL_Bob = [[0] * len(phi_data[0]) for i in range(len(phi_data))] #Bob is steering party
    errorL_Bob = [[0] * len(phi_data[0]) for i in range(len(phi_data))]
    
    for row in range(len(phi_data)):     #equivalently, for row in psi_data
        for col in range(len(phi_data[0])): #equivalently, for col in psi_data
            dataL_Bob[row][col] = V*phi_data[row][col] + (1-V)*psi_data[row][col]
            errorL_Bob[row][col] = V*phi_error[row][col] + (1-V)*psi_error[row][col]

        
    dataL_Alice = transpose(dataL_Bob)
    errorL_Alice = transpose(errorL_Bob) 

    return dataL_Bob, dataL_Alice, errorL_Bob, errorL_Alice










