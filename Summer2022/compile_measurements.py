import pandas as pd
import glob


"""
For older data folders
"""
def compile(exportCSV = True,expType = "Full_Tomography"):
    path = input("Enter folder directory:")
    path.replace('\'' , '\\')

    def getFileInfo(filename):
        info = filename.split(path)[1]
        info = info.split(' ')
        uv_hwp = info[1]
        qp = info[4]
        pcc = info[6]
        basis = info[9]
        return uv_hwp, qp, pcc, basis

    # read all the files with extension .xlsx i.e. excel 
    filenames = glob.glob(path + "\*.csv")

    rows = []
    for file in filenames:
        uv_hwp, qp, pcc, basis = getFileInfo(file)

        df = pd.read_csv(file)
        numRows = df.shape[0]

        c4_data = df.at[numRows - 1,'C4']
        c4_uncertainty = df.at[numRows -1, 'C4 uncertainty']
        rows += [[uv_hwp, qp, pcc, basis, c4_data, c4_uncertainty]]


    newdf = pd.DataFrame(rows, columns = ['UV_HWP', 'QP', 'PCC', 'Basis', 'C4 average', 'C4 average uncertainty'])

    # just for naming new file
    date = filenames[0].split(path)[1]
    newFileName = date.split(' ')[7] + '_' + expType + '.csv'

    # Saves to folder where you are running this file i.e. probably Summer 2022 folder, should move to correct folder
    if exportCSV:
        newdf.to_csv(newFileName, index=False)
        print("Created C4 averages file with name: ", newFileName)
    
    basis_order = []
    if expType == "Full_Tomography":
        basis_order = ["LA", "RA", "VA", "HA", "DA", "AA",
                       "AD", "DD", "HD", "VD", "RD",  "LD",
                       "LH", "RH", "VH", "HH", "DH", "AH", 
                       "AV", "DV", "HV", "VV", "RV", "LV",
                       "LL", "RL", "VL", "HL", "DL", "AL",
                       "AR", "DR", "HR", "VR", "RR", "LR"]
    elif expType == "Purity":
        basis_order = ["DD", "AA", "AD", "DA"]
    elif expType == "Witness":
        basis_order = ["HH", "HV", "VH", "VV",  
                       "DD", "DA", "AD", "AA",   
                       "RR", "RL", "LR", "LL"]
    elif "W1 prime to W3 prime":
        basis_order = ["HH", "HV", "VH", "VV",  
                       "DD", "DA", "AD", "AA",   
                       "RR", "RL", "LR", "LL",
                       "DR", "DL", "AR", "AL",
                       "RD", "RA", "LD", "LA"]
    elif "W4 prime to W6 prime": 
        basis_order = ["HH", "HV", "VH", "VV", 
                       "DD", "DA", "AD", "AA", 
                       "RR", "RL", "LR", "LL",
                       "RH", "RV", "LH", "LV",
                       "HR", "HL", "VR", "VL"]
    elif "W7 prime to W9 prime": 
        basis_order = ["HH", "HV", "VH", "VV", 
                       "DD", "DA", "AD", "AA",
                       "RR", "RL", "LR", "LL",
                       "DH", "DV", "AH", "AV",
                       "HD", "HA", "VD", "VA"]

    clist = []
    for i in basis_order:
        for item in rows:
            if item[3] == i:
                clist += [item[4]]
    return clist

"""
returns a dictionary with items in the format as follows {basis:c4_average}
"""
def get_c4():
    file = input("Enter summary file:")
    file.replace('\'' , '\\')

    df = pd.read_csv(file)
    basis_list = df.loc[:,'State'].tolist()
    df.set_index("State", inplace = True)
    c4_data = {}

    for i in basis_list:
        c4 = df.loc[i, ['C4']].tolist()[0]
        c4_data.update({i: c4})

    return c4_data

"""
returns 2 dictionarys with items in the format as follows {basis:c4_average} and {basis:c4_uncertainty}
"""
def compile_and_get_uncertainty():
    file = input("Enter summary file:")
    file.replace('\'' , '\\')

    df = pd.read_csv(file)
    basis_list = df.loc[:,'State'].tolist()
    df.set_index("State", inplace = True)
    c4_data = {}
    c4_uncertainty = {}

    for i in basis_list:
        c4 = df.loc[i, ['C4']].tolist()[0]
        c4_un = df.loc[i, ['C4 uncertainty']].tolist()[0]
        c4_data.update({i: c4})
        c4_uncertainty.update({i:c4_un})

    return c4_data, c4_uncertainty
    
