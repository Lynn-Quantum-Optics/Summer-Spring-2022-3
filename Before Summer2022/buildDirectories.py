
# This file is a helper file that build appropriate directory structures when saving a file.

import os

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