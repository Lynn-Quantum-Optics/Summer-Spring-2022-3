import math
import scipy.optimize as spo

# Dealing with uncertainty
from uncertainties import ufloat
from uncertainties.umath import *
import numpy as np

def getProb(c4, ExpType):
    if ExpType == "Full Tomography":
        HH = c4['HH']
        HV = c4['HV']
        VH = c4['VH']
        VV = c4['VV']

        DD = c4['DD']
        DA = c4['DA']
        AD = c4['AD']
        AA = c4['AA']

        RR = c4['RR']
        RL = c4['RL']
        LR = c4['LR']
        LL = c4['LL']
            
        DR = c4['DR']
        DL = c4['DL']
        AR = c4['AR']
        AL = c4['AL']

        RD = c4['RD']
        RA = c4['RA']
        LD = c4['LD']
        LA = c4['LA']

        RH = c4['RH']
        RV = c4['RV']
        LH = c4['LH']
        LV = c4['LV']

        HR = c4['HR']
        HL = c4['HL']
        VR = c4['VR']
        VL = c4['VL']

        DH = c4['DH']
        DV = c4['DV']
        AH = c4['AH']
        AV = c4['AV']

        HD = c4['HD']
        HA = c4['HA']
        VD = c4['VD']
        VA = c4['VA']
        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA, RH, RV, LH, LV, HR, HL, VR, VL, DH, DV, AH, AV, HD, HA, VD, VA

    elif ExpType == "Witness":
        HH = c4['HH']
        HV = c4['HV']
        VH = c4['VH']
        VV = c4['VV']

        DD = c4['DD']
        DA = c4['DA']
        AD = c4['AD']
        AA = c4['AA']

        RR = c4['RR']
        RL = c4['RL']
        LR = c4['LR']
        LL = c4['LL']
        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL
    
    elif ExpType == "W1 prime to W3 prime":
        HH = c4['HH']
        HV = c4['HV']
        VH = c4['VH']
        VV = c4['VV']

        DD = c4['DD']
        DA = c4['DA']
        AD = c4['AD']
        AA = c4['AA']

        RR = c4['RR']
        RL = c4['RL']
        LR = c4['LR']
        LL = c4['LL']
            
        DR = c4['DR']
        DL = c4['DL']
        AR = c4['AR']
        AL = c4['AL']

        RD = c4['RD']
        RA = c4['RA']
        LD = c4['LD']
        LA = c4['LA']
        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA
    
    elif ExpType == "W4 prime to W6 prime":
        HH = c4['HH']
        HV = c4['HV']
        VH = c4['VH']
        VV = c4['VV']

        DD = c4['DD']
        DA = c4['DA']
        AD = c4['AD']
        AA = c4['AA']

        RR = c4['RR']
        RL = c4['RL']
        LR = c4['LR']
        LL = c4['LL']

        RH = c4['RH']
        RV = c4['RV']
        LH = c4['LH']
        LV = c4['LV']

        HR = c4['HR']
        HL = c4['HL']
        VR = c4['VR']
        VL = c4['VL']

        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, RH, RV, LH, LV, HR, HL, VR, VL
    elif ExpType == "W7 prime to W9 prime":
        HH = c4['HH']
        HV = c4['HV']
        VH = c4['VH']
        VV = c4['VV']

        DD = c4['DD']
        DA = c4['DA']
        AD = c4['AD']
        AA = c4['AA']

        RR = c4['RR']
        RL = c4['RL']
        LR = c4['LR']
        LL = c4['LL']

        DH = c4['DH']
        DV = c4['DV']
        AH = c4['AH']
        AV = c4['AV']

        HD = c4['HD']
        HA = c4['HA']
        VD = c4['VD']
        VA = c4['VA']
        
        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DH, DV, AH, AV, HD, HA, VD, VA
    else: 
        raise Exception("Invalid Experiment Type. Possible Experiment types: Full Tomography, Witness, W1 prime to W3 prime, W4 prime to W6 prime, W7 prime to W9 prime")

def getProbandUncertainty(c4, c4_un, ExpType):
    print('c4 type', type(c4))
    print('c4_un type', type(c4_un))
    if ExpType == "Full Tomography":
        HH = ufloat(c4['HH'], c4_un['HH'])
        HV = ufloat(c4['HV'], c4_un['HV'])
        VH = ufloat(c4['VH'], c4_un['VH'])
        VV = ufloat(c4['VV'], c4_un['VV'])

        DD = ufloat(c4['DD'], c4_un['DD'])
        DA = ufloat(c4['DA'], c4_un['DA'])
        AD = ufloat(c4['AD'], c4_un['AD'])
        AA = ufloat(c4['AA'], c4_un['AA'])

        RR = ufloat(c4['RR'], c4_un['RR'])
        RL = ufloat(c4['RL'], c4_un['RL'])
        LR = ufloat(c4['LR'], c4_un['LR'])
        LL = ufloat(c4['LL'], c4_un['LL'])
            
        DR = ufloat(c4['DR'], c4_un['DR'])
        DL = ufloat(c4['DL'], c4_un['DL'])
        AR = ufloat(c4['AR'], c4_un['AR'])
        AL = ufloat(c4['AL'], c4_un['AL'])

        RD = ufloat(c4['RD'], c4_un['RA'])
        RA = ufloat(c4['RA'], c4_un['RA'])
        LD = ufloat(c4['LD'], c4_un['LD'])
        LA = ufloat(c4['LA'], c4_un['LA'])

        RH = ufloat(c4['RH'], c4_un['RH'])
        RV = ufloat(c4['RV'], c4_un['RV'])
        LH = ufloat(c4['LH'], c4_un['LH'])
        LV = ufloat(c4['LV'], c4_un['LH'])

        HR = ufloat(c4['HR'], c4_un['HR'])
        HL = ufloat(c4['HL'], c4_un['HL'])
        VR = ufloat(c4['VR'], c4_un['VR'])
        VL = ufloat(c4['VL'], c4_un['VL'])

        DH = ufloat(c4['DH'], c4_un['DH'])
        DV = ufloat(c4['DV'], c4_un['DV'])
        AH = ufloat(c4['AH'], c4_un['AH'])
        AV = ufloat(c4['AV'], c4_un['AV'])

        HD = ufloat(c4['HD'], c4_un['HD'])
        HA = ufloat(c4['HA'], c4_un['HA'])
        VD = ufloat(c4['VD'], c4_un['VD'])
        VA = ufloat(c4['VA'], c4_un['VA'])
        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA, RH, RV, LH, LV, HR, HL, VR, VL, DH, DV, AH, AV, HD, HA, VD, VA

    elif ExpType == "Witness":
        HH = ufloat(c4['HH'], c4_un['HH'])
        HV = ufloat(c4['HV'], c4_un['HV'])
        VH = ufloat(c4['VH'], c4_un['VH'])
        VV = ufloat(c4['VV'], c4_un['VV'])

        DD = ufloat(c4['DD'], c4_un['DD'])
        DA = ufloat(c4['DA'], c4_un['DA'])
        AD = ufloat(c4['AD'], c4_un['AD'])
        AA = ufloat(c4['AA'], c4_un['AA'])

        RR = ufloat(c4['RR'], c4_un['RR'])
        RL = ufloat(c4['RL'], c4_un['RL'])
        LR = ufloat(c4['LR'], c4_un['LR'])
        LL = ufloat(c4['LL'], c4_un['LL'])

        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL
    
    elif ExpType == "W1 prime to W3 prime":
        HH = ufloat(c4['HH'], c4_un['HH'])
        HV = ufloat(c4['HV'], c4_un['HV'])
        VH = ufloat(c4['VH'], c4_un['VH'])
        VV = ufloat(c4['VV'], c4_un['VV'])

        DD = ufloat(c4['DD'], c4_un['DD'])
        DA = ufloat(c4['DA'], c4_un['DA'])
        AD = ufloat(c4['AD'], c4_un['AD'])
        AA = ufloat(c4['AA'], c4_un['AA'])

        RR = ufloat(c4['RR'], c4_un['RR'])
        RL = ufloat(c4['RL'], c4_un['RL'])
        LR = ufloat(c4['LR'], c4_un['LR'])
        LL = ufloat(c4['LL'], c4_un['LL'])
            
        DR = ufloat(c4['DR'], c4_un['DR'])
        DL = ufloat(c4['DL'], c4_un['DL'])
        AR = ufloat(c4['AR'], c4_un['AR'])
        AL = ufloat(c4['AL'], c4_un['AL'])

        RD = ufloat(c4['RD'], c4_un['RA'])
        RA = ufloat(c4['RA'], c4_un['RA'])
        LD = ufloat(c4['LD'], c4_un['LD'])
        LA = ufloat(c4['LA'], c4_un['LA'])

        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA
    
    elif ExpType == "W4 prime to W6 prime":
        HH = ufloat(c4['HH'], c4_un['HH'])
        HV = ufloat(c4['HV'], c4_un['HV'])
        VH = ufloat(c4['VH'], c4_un['VH'])
        VV = ufloat(c4['VV'], c4_un['VV'])

        DD = ufloat(c4['DD'], c4_un['DD'])
        DA = ufloat(c4['DA'], c4_un['DA'])
        AD = ufloat(c4['AD'], c4_un['AD'])
        AA = ufloat(c4['AA'], c4_un['AA'])

        RR = ufloat(c4['RR'], c4_un['RR'])
        RL = ufloat(c4['RL'], c4_un['RL'])
        LR = ufloat(c4['LR'], c4_un['LR'])
        LL = ufloat(c4['LL'], c4_un['LL'])

        RH = ufloat(c4['RH'], c4_un['RH'])
        RV = ufloat(c4['RV'], c4_un['RV'])
        LH = ufloat(c4['LH'], c4_un['LH'])
        LV = ufloat(c4['LV'], c4_un['LH'])

        HR = ufloat(c4['HR'], c4_un['HR'])
        HL = ufloat(c4['HL'], c4_un['HL'])
        VR = ufloat(c4['VR'], c4_un['VR'])
        VL = ufloat(c4['VL'], c4_un['VL'])

        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, RH, RV, LH, LV, HR, HL, VR, VL
    elif ExpType == "W7 prime to W9 prime":
        HH = ufloat(c4['HH'], c4_un['HH'])
        HV = ufloat(c4['HV'], c4_un['HV'])
        VH = ufloat(c4['VH'], c4_un['VH'])
        VV = ufloat(c4['VV'], c4_un['VV'])

        DD = ufloat(c4['DD'], c4_un['DD'])
        DA = ufloat(c4['DA'], c4_un['DA'])
        AD = ufloat(c4['AD'], c4_un['AD'])
        AA = ufloat(c4['AA'], c4_un['AA'])

        RR = ufloat(c4['RR'], c4_un['RR'])
        RL = ufloat(c4['RL'], c4_un['RL'])
        LR = ufloat(c4['LR'], c4_un['LR'])
        LL = ufloat(c4['LL'], c4_un['LL'])

        DH = ufloat(c4['DH'], c4_un['DH'])
        DV = ufloat(c4['DV'], c4_un['DV'])
        AH = ufloat(c4['AH'], c4_un['AH'])
        AV = ufloat(c4['AV'], c4_un['AV'])

        HD = ufloat(c4['HD'], c4_un['HD'])
        HA = ufloat(c4['HA'], c4_un['HA'])
        VD = ufloat(c4['VD'], c4_un['VD'])
        VA = ufloat(c4['VA'], c4_un['VA'])
        return HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DH, DV, AH, AV, HD, HA, VD, VA
    else: 
        raise Exception("Invalid Experiment Type. Possible Experiment types: Full Tomography, Witness, W1 prime to W3 prime, W4 prime to W6 prime, W7 prime to W9 prime")
   

def getStokesParameters(c4, c4_un, ExpType, getUncertainty = False):
    if ExpType == "Full Tomography":
        if getUncertainty:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA, RH, RV, LH, LV, HR, HL, VR, VL, DH, DV, AH, AV, HD, HA, VD, VA = getProbandUncertainty(c4, c4_un, ExpType)
        else:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA, RH, RV, LH, LV, HR, HL, VR, VL, DH, DV, AH, AV, HD, HA, VD, VA = getProb(c4, ExpType)
        p_xx = (DD - DA - AD + AA)/(DD + DA + AD + AA)
        p_yy = (RR - RL - LR + LL)/(RR + RL + LR + LL)
        p_zz = (HH - HV - VH + VV)/(HH + HV + VH + VV)

        p_xI = (DD - AD - AA + DA)/(DD + AD + AA + DA)
        p_Ix = (DD - DA - AA + AD)/(DD + DA + AA + AD)

        p_yI = (RR + RL - LL - LR)/(RR + RL + LL + LR)
        p_Iy = (RR + LR - LL - RL)/(RR + LR + LL + RL)

        p_zI = (HH - VH - VV + HV)/(HH + VH + VV + HV)
        p_Iz = (HH - HV - VV + VH)/(HH + HV + VV + VH)

        p_xy = (DR - DL - AR + AL)/(DR + DL + AR + AL)
        p_yx = (RD - RA - LD + LA)/(RD + RA + LD + LA)

        p_yz = (RH - RV - LH + LV)/(RH + RV + LH + LV)
        p_zy = (HR - HL - VR + VL)/(HR + HL + VR + VL)

        p_xz = (DH - DV - AH + AV)/(DH + DV + AH + AV)
        p_zx = (HD - HA - VD + VA)/(HD + HA + VD + VA)
        return p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_xy, p_yx, p_yz, p_zy, p_xz, p_zx
    
    elif ExpType == "Witness":
        if getUncertainty: 
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL = getProbandUncertainty(c4, c4_un, ExpType)
        else:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL = getProb(c4, ExpType)
        p_xx = (DD - DA - AD + AA)/(DD + DA + AD + AA)
        p_yy = (RR - RL - LR + LL)/(RR + RL + LR + LL)
        p_zz = (HH - HV - VH + VV)/(HH + HV + VH + VV)

        p_xI = (DD - AD - AA + DA)/(DD + AD + AA + DA)
        p_Ix = (DD - DA - AA + AD)/(DD + DA + AA + AD)

        p_yI = (RR + RL - LL - LR)/(RR + RL + LL + LR)
        p_Iy = (RR + LR - LL - RL)/(RR + LR + LL + RL)

        p_zI = (HH - VH - VV + HV)/(HH + VH + VV + HV)
        p_Iz = (HH - HV - VV + VH)/(HH + HV + VV + VH)
        return p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz
    
    elif ExpType == "W1 prime to W3 prime":
        if getUncertainty: 
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA = getProbandUncertainty(c4, c4_un, ExpType)
        else:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DR, DL, AR, AL, RD, RA, LD, LA = getProb(c4, ExpType)
        p_xx = (DD - DA - AD + AA)/(DD + DA + AD + AA)
        p_yy = (RR - RL - LR + LL)/(RR + RL + LR + LL)
        p_zz = (HH - HV - VH + VV)/(HH + HV + VH + VV)

        p_xI = (DD - AD - AA + DA)/(DD + AD + AA + DA)
        p_Ix = (DD - DA - AA + AD)/(DD + DA + AA + AD)

        p_yI = (RR + RL - LL - LR)/(RR + RL + LL + LR)
        p_Iy = (RR + LR - LL - RL)/(RR + LR + LL + RL)

        p_zI = (HH - VH - VV + HV)/(HH + VH + VV + HV)
        p_Iz = (HH - HV - VV + VH)/(HH + HV + VV + VH)

        p_xy = (DR - DL - AR + AL)/(DR + DL + AR + AL)
        p_yx = (RD - RA - LD + LA)/(RD + RA + LD + LA)
        return p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_xy, p_yx
    
    elif ExpType == "W4 prime to W6 prime":
        if getUncertainty:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, RH, RV, LH, LV, HR, HL, VR, VL = getProbandUncertainty(c4, c4_un, ExpType)
        else:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, RH, RV, LH, LV, HR, HL, VR, VL = getProb(c4, ExpType)
        p_xx = (DD - DA - AD + AA)/(DD + DA + AD + AA)
        p_yy = (RR - RL - LR + LL)/(RR + RL + LR + LL)
        p_zz = (HH - HV - VH + VV)/(HH + HV + VH + VV)

        p_xI = (DD - AD - AA + DA)/(DD + AD + AA + DA)
        p_Ix = (DD - DA - AA + AD)/(DD + DA + AA + AD)

        p_yI = (RR + RL - LL - LR)/(RR + RL + LL + LR)
        p_Iy = (RR + LR - LL - RL)/(RR + LR + LL + RL)

        p_zI = (HH - VH - VV + HV)/(HH + VH + VV + HV)
        p_Iz = (HH - HV - VV + VH)/(HH + HV + VV + VH)

        p_yz = (RH - RV - LH + LV)/(RH + RV + LH + LV)
        p_zy = (HR - HL - VR + VL)/(HR + HL + VR + VL)
        return p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_yz, p_zy
    
    elif ExpType == "W7 prime to W9 prime":
        if getUncertainty:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DH, DV, AH, AV, HD, HA, VD, VA = getProbandUncertainty(c4, c4_un, ExpType)
        else:
            HH, HV, VH, VV, DD, DA, AD, AA, RR, RL, LR, LL, DH, DV, AH, AV, HD, HA, VD, VA = getProb(c4, ExpType)
        p_xx = (DD - DA - AD + AA)/(DD + DA + AD + AA)
        p_yy = (RR - RL - LR + LL)/(RR + RL + LR + LL)
        p_zz = (HH - HV - VH + VV)/(HH + HV + VH + VV)

        p_xI = (DD - AD - AA + DA)/(DD + AD + AA + DA)
        p_Ix = (DD - DA - AA + AD)/(DD + DA + AA + AD)

        p_yI = (RR + RL - LL - LR)/(RR + RL + LL + LR)
        p_Iy = (RR + LR - LL - RL)/(RR + LR + LL + RL)

        p_zI = (HH - VH - VV + HV)/(HH + VH + VV + HV)
        p_Iz = (HH - HV - VV + VH)/(HH + HV + VV + VH)

        p_xz = (DH - DV - AH + AV)/(DH + DV + AH + AV)
        p_zx = (HD - HA - VD + VA)/(HD + HA + VD + VA)
        return p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_xz, p_zx
    else: 
        raise Exception("Invalid Experiment Type. Possible Experiment types: Full Tomography, Witness, W1 prime to W3 prime, W4 prime to W6 prime, W7 prime to W9 prime")

def optimizeW(fxn, fxn_uncertainty, p_un_list):
    Witness = spo.minimize(fxn, 0, bounds = [(0, 2*math.pi)],  options={"disp": True})
    if Witness.success: 
        t = Witness.x[0]
        uncertainty = fxn_uncertainty(t, p_un_list)
        W = [Witness.fun, t, 0, 0, uncertainty]
    else:
        W = [0,0,0,0,0]
    return W

def maxW(fxn, fxn_uncertainty, p_un_list):
    Witness = spo.minimize(fxn, 0, bounds = [(0, 2*math.pi)],  options={"disp": True})
    if Witness.success: 
        t = Witness.x[0]
        uncertainty = fxn_uncertainty(t, p_un_list)
        W = [-Witness.fun, t, 0, 0, uncertainty]
    else:
        W = [0,0,0,0,0]
    return W

def optimizeW_2p(fxn, fxn_uncertainty, p_un_list):
    x0 = [(0,2*math.pi), (0,2*math.pi)]
    Witness = spo.minimize(fxn,[0,0], bounds = x0,  options={"disp": True})

    if Witness.success: 
        t = Witness.x[0]
        a = Witness.x[1]
        uncertainty = fxn_uncertainty(t, a, p_un_list)
        W = [Witness.fun, t, a, 0, uncertainty]
    else:
        W = [0,0,0,0,0]
    return W

def optimizeW_3p(fxn, fxn_uncertainty, p_un_list):
    x0 = [(0,2*math.pi), (0,2*math.pi), (0,2*math.pi)]
    Witness = spo.minimize(fxn,[0,0,0], bounds = x0,  options={"disp": True})
    
    if Witness.success:
        t = Witness.x[0]
        a = Witness.x[1]
        b = Witness.x[2]
        uncertainty = fxn_uncertainty(t, a, b, p_un_list)
        W = [Witness.fun, t, a, b, uncertainty]
    else:
        W = [0,0,0,0,0]
    return W

def W1_uncertainty(t, p_list):
    W1 = 1/4*(p_list[2] + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[0] 
                + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[1]
                + 2*math.sin(t)*math.cos(t)*(p_list[7] + p_list[8]))
    return W1

def W2_uncertainty(t, p_list):
    W2  = 1/4*(p_list[2]  + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[0] 
                + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[1]
                + 2*math.sin(t)*math.cos(t)*(p_list[7] + p_list[8]))
    return W2

def W3_uncertainty(t, p_list):
    W3 = 1/4*(p_list[0] + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[2] 
                + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[1]
                + 2*math.sin(t)*math.cos(t)*(p_list[3] + p_list[4]))
    return W3

def W4_uncertainty(t, p_list):
    W4= 1/4*(p_list[0] + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[2] 
                + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[1]
                + 2*math.sin(t)*math.cos(t)*(p_list[3] + p_list[4]))
    return W4

def W5_uncertainty(t, p_list):
    W5 = 1/4*(p_list[1] + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[2] 
                + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[0]
                + 2*math.sin(t)*math.cos(t)*(p_list[5] + p_list[6]))
    return W5

def W6_uncertainty(t, p_list):
    W6 = 1/4*(p_list[1] + ((math.cos(t))**2 + (math.sin(t))**2)*p_list[2] 
                + ((math.cos(t))**2 - (math.sin(t))**2)*p_list[0]
                + 2*math.sin(t)*math.cos(t)*(p_list[5] + p_list[6]))        
    return W6

#//////////////////////////////////New 9 Prime Witnesses///////////////////////////////////////

#//////////////////////////////////Triplet 1: require p_list[9] and p_list[10] as well///////////////////////////////////////
"""
Might need to update this, as this calculation of witness uncertainty might not be entirely correct
"""

def W1p_uncertainty(t, a, p_list):
    W1p = 1/4*(p_list[2] + math.cos(2*t)*(p_list[0] + p_list[1])
            + math.sin(2*t)*math.cos(a)*(p_list[7] + p_list[8])
            + math.sin(2*t)*math.sin(a)*(p_list[9] + p_list[10]))
    return W1p

def W2p_uncertainty(t, a, p_list):
    W2p = 1/4*(p_list[2] + math.cos(2*t)*(p_list[0] + p_list[1])
            + math.sin(2*t)*math.cos(a)*(p_list[7] + p_list[8])
            + math.sin(2*t)*math.sin(a)*(p_list[9] + p_list[10]))
    return W2p

def W3p_uncertainty(t, a, b, p_list):
    W3p = 1/4*(((math.cos(t))**2)*(p_list[2])
            + ((math.sin(t))**2)*(p_list[2])
            + ((math.cos(t))**2)*math.cos(b)*(p_list[0] + p_list[1])
            + ((math.sin(t))**2)*math.cos(2*a -b)*(p_list[0] + p_list[1])
            + math.sin(2*t)*math.cos(a)*p_list[3]
            + math.sin(2*t)*math.cos(a-b)*p_list[4]
            + math.sin(2*t)*math.sin(a)*p_list[5]
            + math.sin(2*t)*math.sin(a-b)*p_list[6]
            + ((math.cos(t))**2)*math.sin(b)*(p_list[10] + p_list[9])
            + ((math.sin(t))**2)*math.sin(2*a-b)*(p_list[10] + p_list[9]))
    return W3p

#//////////////////////////////////Triplet 2: require p_list[11] and p_list[12] as well///////////////////////////////////////
def W4p_uncertainty(t, a, p_list):
    W4p = 1/4*(p_list[0] + math.cos(2*t)*(p_list[2] + p_list[1])
            + math.sin(2*t)*math.cos(a)*(p_list[4] + p_list[3])
            + math.sin(2*t)*math.sin(a)*(p_list[11] + p_list[12]))
    return W4p

def W5p_uncertainty(t, a, p_list):
    W5p = 1/4*(p_list[0] + math.cos(2*t)*(p_list[2] + p_list[1])
            + math.sin(2*t)*math.cos(a)*(p_list[4] + p_list[3])
            + math.sin(2*t)*math.sin(a)*(p_list[11] + p_list[12]))
    return W5p

def W6p_uncertainty(t, a, b, p_list):
    W6p = 1/4*(((math.cos(t))**2)*((math.cos(a))**2)*(p_list[2] + p_list[7] + p_list[8])
            + ((math.cos(t))**2)*((math.sin(a))**2)*(p_list[2] + p_list[7] + p_list[8])
            + ((math.sin(t))**2)*((math.cos(b))**2)*(p_list[2] + p_list[7] + p_list[8])
            + ((math.sin(t))**2)*((math.sin(b))**2)*(p_list[2] + p_list[7] + p_list[8])
            + math.sin(2*t)*math.cos(a)*math.cos(b)*(p_list[0] + p_list[1])
            + math.sin(2*t)*math.sin(a)*math.sin(b)*(p_list[0] + p_list[1])
            + math.sin(2*t)*math.cos(a)*math.sin(b)*(p_list[11] + p_list[5])
            + math.sin(2*t)*math.sin(a)*math.cos(b)*(p_list[11] + p_list[5])
            + ((math.cos(t))**2)*math.sin(2*a)*(p_list[12] + p_list[6])
            + ((math.sin(t))**2)*math.sin(2*b)*(p_list[12] + p_list[6]))
    return W6p

def W7p_uncertainty(t, a, p_list):
    W7p = 1/4*(p_list[1] + math.cos(2*t)*(p_list[2] + p_list[0])
            + math.sin(2*t)*math.cos(a)*(p_list[14] + p_list[13])
            + math.sin(2*t)*math.sin(a)*(p_list[5] + p_list[6]))
    return W7p

def W8p_uncertainty(t, a, p_list):
    W8p = 1/4*(p_list[1] + math.cos(2*t)*(p_list[2] + p_list[0])
            + math.sin(2*t)*math.cos(a)*(p_list[14] + p_list[13])
            + math.sin(2*t)*math.sin(a)*(p_list[5] + p_list[6]))
    return W8p

def W9p_uncertainty(t, a, b, p_list):
    W9p = 1/4*(((math.cos(t))**2)*((math.cos(a))**2)*(p_list[2] + p_list[7] + p_list[8])
            + ((math.cos(t))**2)*((math.sin(a))**2)*(p_list[2] + p_list[7] + p_list[8])
            + ((math.sin(t))**2)*((math.cos(b))**2)*(p_list[2] + p_list[7] + p_list[8])
            + ((math.sin(t))**2)*((math.sin(b))**2)*(p_list[2] + p_list[7] + p_list[8])
            + math.sin(2*t)*math.cos(a)*math.cos(b)*(p_list[0] + p_list[1])
            + math.sin(2*t)*math.sin(a)*math.sin(b)*(p_list[0] + p_list[1])
            + ((math.cos(t))**2)*math.sin(2*a)*(p_list[4] + p_list[14])
            + ((math.sin(t))**2)*math.sin(2*b)*(p_list[4] + p_list[14])
            + math.sin(2*t)*math.cos(a)*math.sin(b)*(p_list[3] + p_list[13])
            + math.sin(2*t)*math.sin(a)*math.cos(b)*(p_list[3] + p_list[13]))
    return W9p
