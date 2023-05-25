# Theresa Lynn 7/26/19 - 8/1/19
# from skeleton code by Lorenzo Calvano 6/16/18
# that was edited by Helen Chaffee 7/9/19 and preceding days

from readcsvinpython import *
from math import *

#countsL is the name of the coincidence counts matrix, with bob's angles the rows and alice's angles the columns or vice versa for the transposed matrix.
#if you want to run this code with Alice as the steering party, you must use the transposed matrix as input!

#data analysis no longer uses theory, so V and z below are not necessary in the code.
#V = 0.85 #defines the proportion of state 1, cos(z)|HH> + sin(z)|VV> . State 2 has proportion (1-V).
#z = (pi/8) #defines the sin and cosine argument in states 1 and 2

step = 2.5 # in degrees
initialAngle = 0
finalAngle = 90 # remember to change this to 100 if we're analyzing the data from summer 2018
# The three lines above describe the angle coverage and precision of our data
# This only supports symmetric data currently (same angle sweeps on Bob and Alice)
# The angle sweep must cover at least a quarter-turn (say, 0 to 90)
# It's ideal for 45-degree offsets to be defined in the data (see next calculation)

index_plus45 = int(45//step) # the index of the angle that is 45 degrees off an index we're looking at
                       # this should correspond to a data point in countsL
possible_angles = 2*index_plus45  # we can only sweep to 90 degrees relative from where we started

BobHWPaxis=-5.79
AliceHWPaxis=-1.17


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#conditionalstates3 takes given omega, alpha, beta, and finds the conditional states for omega (mostly alpha) and omegaperp (mostly beta)
#also takes coincidence data and finds coincidence data from +/- states (+ gives cond state mostly phi, - gives cond state mostly gamma)
#Based on data, looks for LHS Bloch vectors according to my modification of the 2016 PRL appendix.  If all exist with magnitude <=1, reports no steering.
#If any Bloch vectors have magnitude >1, calculates x_b and x_g from 2014 PRL.  If x_b<=x_g, reports no steering.
#If legitimate LHS Bloch vectors do not exist and x_b > x_g, reports steering.

def conditionalstates3(alphaperpindex,betaindex,betaperpindex,omegaperpindex,countsL,errorsL,omegaindex,alphaindex,steeringparty,errorcond):
    '''Actually does the calculations and returns list(s) of conditional states that Alice has for Bob, if any.'''
    #The calculation theta' = 2*(90-theta) is done to convert the angle index of measurement(like omegaindex) into the angle that defines the relative proportions of |H> and |V>
    if steeringparty == 'Alice' or steeringparty == 'alice': #these cases decide which axis angle needs to be subtracted from our measurement angles
        axisER = AliceHWPaxis
        axisEE = BobHWPaxis
    elif steeringparty == 'Bob' or steeringparty == 'bob':
        axisER = BobHWPaxis
        axisEE = AliceHWPaxis
    
    #omegaindex is the steerer's angle index
    omega=2*(90-(omegaindex*step - axisER))*(pi/180)
    omegaperp=2*(90-(omegaperpindex*step - axisER))*(pi/180)
    #first conditional state of non-steerer defined by alphaindex
    alpha=2*(90-(alphaindex*step - axisEE))*(pi/180)
    alphaperp=2*(90-(alphaperpindex*step - axisEE))*(pi/180)
    #second conditional state of non-steerer defined by betaindex
    beta=2*(90-(betaindex*step - axisEE))*(pi/180)
    betaperp=2*(90-(betaperpindex*step - axisEE))*(pi/180)
    
    if type(omegaindex) == float or type(alphaperpindex) == float or type(alphaindex) == float or type(omegaperpindex) == float or type(betaperpindex) == float or type(betaindex) == float:
        print("Omegaindex: ",omegaindex,". Alphaperpindex: ",alphaperpindex,". Alphaindex: ",alphaindex,omegaperpindex,betaperpindex,betaindex)
    #eAlpha and eBeta are the probabilities of getting the state that is orthogonal to the conditional state alpha/beta for Alice
    eAlpha=(countsL[omegaindex][alphaperpindex]-errorcond*errorsL[omegaindex][alphaperpindex])/(countsL[omegaindex][alphaperpindex]-errorcond*errorsL[omegaindex][alphaperpindex]+countsL[omegaindex][alphaindex]+errorcond*errorsL[omegaindex][alphaindex])
    eBeta=(countsL[omegaperpindex][betaperpindex]-errorcond*errorsL[omegaperpindex][betaperpindex])/(countsL[omegaperpindex][betaperpindex]-errorcond*errorsL[omegaperpindex][betaperpindex]+countsL[omegaperpindex][betaindex]+errorcond*errorsL[omegaperpindex][betaindex])
    

    #ProbH is the probability of getting h for steeree
    #since h may not be in data, just use the index closest to it
    hindex = (round((90+axisEE)/step)) % possible_angles
    vindex = (hindex+index_plus45) % possible_angles
    PhL=[] #calculate Ph for each steerer angle and average them
    for windex in range(len(countsL)): #loop through all steerer angles (all rows of Excel file)
        wperpindex = (windex+index_plus45) % possible_angles
        prob = (countsL[windex][hindex]+countsL[wperpindex][hindex])/(countsL[windex][hindex]+countsL[wperpindex][hindex]+countsL[windex][vindex]+countsL[wperpindex][vindex])
        PhL.append(prob)
    ProbH = sum(PhL)/len(PhL)
 
    #Now find conditional states for meas halfway between omega and omegaperp
    #if data doesn't have halfway between, check two bracketing cases and take the purest state
    plusindex1 = floor((omegaindex+omegaperpindex)/2)
    plusindex2 = ceil((omegaindex+omegaperpindex)/2) #will almost always find the same plus state for both Bobangle and Bobangleperp.  Need to search the minus data too, then.
    #to calculate probability of plusindex,potentialThetaA need to have perps of both of these
    #uses modular arithmetic to find minus index -- will only try one minus index if there is more than one.
    minusindex1 = (plusindex1 + index_plus45) % possible_angles
    minusindex2 = (plusindex2 + index_plus45) % possible_angles
    #finding conditional state phi for + measurement bracketer 1
    plus1countsmax = max(countsL[plusindex1])
    phiindex1 = countsL[plusindex1].index(plus1countsmax)
    plus1countsmin = min(countsL[plusindex1])
    phiperpindex3 = countsL[plusindex1].index(plus1countsmin)
    #if max counts and min counts not 45 deg offset, then see which one comes closer to pure state
    phiperpindex1 = (phiindex1+index_plus45) % possible_angles
    phiindex3 = (phiperpindex3 + index_plus45) % possible_angles
    ePhi1 = (countsL[plusindex1][phiperpindex1]-errorcond*errorsL[plusindex1][phiperpindex1])/(countsL[plusindex1][phiindex1]+errorcond*errorsL[plusindex1][phiindex1] + countsL[plusindex1][phiperpindex1]-errorcond*errorsL[plusindex1][phiperpindex1])
    ePhi3 = (countsL[plusindex1][phiperpindex3]-errorcond*errorsL[plusindex1][phiperpindex3])/(countsL[plusindex1][phiindex3]+errorcond*errorsL[plusindex1][phiindex3] + countsL[plusindex1][phiperpindex3]-errorcond*errorsL[plusindex1][phiperpindex3])
    if ePhi3 < ePhi1:
        phiindex1 = phiindex3
        phiperpindex1 = phiperpindex3
        ePhi1 = ePhi3
    #finding conditional state phi for + measurement bracketer 2
    plus2countsmax = max(countsL[plusindex2])
    phiindex2 = countsL[plusindex2].index(plus2countsmax)
    plus2countsmin = min(countsL[plusindex2])
    phiperpindex4 = countsL[plusindex2].index(plus2countsmin)
    #if max counts and min counts not 45 deg offset, then see which one comes closer to pure state
    phiperpindex2 = (phiindex2+index_plus45) % possible_angles
    phiindex4 = (phiperpindex4 + index_plus45) % possible_angles
    ePhi2 = (countsL[plusindex2][phiperpindex2]-errorcond*errorsL[plusindex2][phiperpindex2])/(countsL[plusindex2][phiindex2]+errorcond*errorsL[plusindex2][phiindex2] + countsL[plusindex2][phiperpindex2]-errorcond*errorsL[plusindex2][phiperpindex2])
    ePhi4 = (countsL[plusindex2][phiperpindex4]-errorcond*errorsL[plusindex2][phiperpindex4])/(countsL[plusindex2][phiindex4]+errorcond*errorsL[plusindex2][phiindex4] + countsL[plusindex2][phiperpindex4]-errorcond*errorsL[plusindex2][phiperpindex4])
    if ePhi4 < ePhi2:
        phiindex2 = phiindex4
        phiperpindex2 = phiperpindex4
        ePhi2 = ePhi4
    #if data lacks plus state for steerer, pick bracketing case with purer conditional state
    if ePhi2 < ePhi1:
        phiindex = phiindex2
        phiperpindex = phiperpindex2
        ePhi = ePhi2
    else:
        phiindex=phiindex1
        phiperpindex = phiperpindex1
        ePhi = ePhi1
    phi = 2*(90-(phiindex*step - axisEE))*(pi/180)

    #Now find conditional states for other meas outcome halfway between omega and omegaperp
    #if data doesn't have halfway between, check two bracketing cases and take the purest state        
    #finding conditional state gamma for - measurement bracketer 1
    minus1countsmax = max(countsL[minusindex1])
    gammaindex1 = countsL[minusindex1].index(minus1countsmax)
    minus1countsmin = min(countsL[minusindex1])
    gammaperpindex3 = countsL[minusindex1].index(minus1countsmin)
    #if max counts and min counts not 45 deg offset, then see which one comes closer to pure state
    gammaperpindex1 = (gammaindex1+index_plus45) % possible_angles
    gammaindex3 = (gammaperpindex3 + index_plus45) % possible_angles
    eGamma1 = (countsL[minusindex1][gammaperpindex1]-errorcond*errorsL[minusindex1][gammaperpindex1])/(countsL[minusindex1][gammaindex1]+errorcond*errorsL[minusindex1][gammaindex1] + countsL[minusindex1][gammaperpindex1]-errorcond*errorsL[minusindex1][gammaperpindex1])
    eGamma3 = (countsL[minusindex1][gammaperpindex3]-errorcond*errorsL[minusindex1][gammaperpindex3])/(countsL[minusindex1][gammaindex3]+errorcond*errorsL[minusindex1][gammaindex3] + countsL[minusindex1][gammaperpindex3]-errorcond*errorsL[minusindex1][gammaperpindex3])
    if eGamma3 < eGamma1:
        gammaindex1 = gammaindex3
        gammaperpindex1 = gammaperpindex3
        eGamma1 = eGamma3        
    #finding conditional state gamma for - measurement bracketer 2
    minus2countsmax = max(countsL[minusindex2])
    gammaindex2 = countsL[minusindex2].index(minus2countsmax)
    minus2countsmin = min(countsL[minusindex2])
    gammaperpindex4 = countsL[minusindex2].index(minus2countsmin)
    #if max counts and min counts not 45 deg offset, then see which one comes closer to pure state
    gammaperpindex2 = (gammaindex2+index_plus45) % possible_angles
    gammaindex4 = (gammaperpindex4 + index_plus45) % possible_angles
    eGamma2 = (countsL[minusindex2][gammaperpindex2]-errorcond*errorsL[minusindex2][gammaperpindex2])/(countsL[minusindex2][gammaindex2]+errorcond*errorsL[minusindex2][gammaindex2] + countsL[minusindex2][gammaperpindex2]-errorcond*errorsL[minusindex2][gammaperpindex2])
    eGamma4 = (countsL[minusindex2][gammaperpindex4]-errorcond*errorsL[minusindex2][gammaperpindex4])/(countsL[minusindex2][gammaindex4]+errorcond*errorsL[minusindex2][gammaindex4] + countsL[minusindex2][gammaperpindex4]-errorcond*errorsL[minusindex2][gammaperpindex4])
    if eGamma4 < eGamma2:
        gammaindex2 = gammaindex4
        gammaperpindex2 = gammaperpindex4
        eGamma2 = eGamma4
    #if data lacks minus state for steerer, pick bracketing case with purer conditional state
    if eGamma2 < eGamma1:
        gammaindex = gammaindex2
        gammaperpindex = gammaperpindex2
        eGamma = eGamma2
    else:
        gammaindex=gammaindex1
        gammaperpindex = gammaperpindex1
        eGamma = eGamma1
    gamma = 2*(90-(gammaindex*step - axisEE))*(pi/180)

    #know all 4 conditional states, so go ahead and calculate a,b,d,c
    #calculate Bloch vectors of the 4 conditional states
    C1x = 2*(1-2*eAlpha)*sin(alpha)*cos(alpha)
    C1z = 2*((1-eAlpha)*cos(alpha)**2+eAlpha*sin(alpha)**2)-1
    C2x = 2*(1-2*eBeta)*sin(beta)*cos(beta)
    C2z = 2*((1-eBeta)*cos(beta)**2+eBeta*sin(beta)**2)-1
    D1x = 2*(1-2*ePhi)*sin(phi)*cos(phi)
    D1z = 2*((1-ePhi)*cos(phi)**2+ePhi*sin(phi)**2)-1
    D2x = 2*(1-2*eGamma)*sin(gamma)*cos(gamma)
    D2z = 2*((1-eGamma)*cos(gamma)**2+eGamma*sin(gamma)**2)-1
    C1sq=C1x**2+C1z**2
    C2sq=C2x**2+C2z**2
    D1sq=D1x**2+D1z**2
    D2sq=D2x**2+D2z**2
    lenmax=max(C1sq,C2sq,D1sq,D2sq)
    if lenmax > 1:
        print("For omega=",omega,", max cond state Bloch vector length is ",lenmax,".")
    #calculate Bloch vectors for the 4 local hidden states
    ax = (C1x+D1x)/(1+C1x*D1x)
    ay = 0
    #az = C1z*D1z/((1+C1x*D1x)*cos(2*z)*(2*V-1)) 
    az = C1z*D1z/((1+C1x*D1x)*(2*ProbH-1))   
    bx = (C2x+D2x)/(1+C2x*D2x)
    by = 0
    #bz = C2z*D2z/((1+C2x*D2x)*cos(2*z)*(2*V-1))
    bz = C2z*D2z/((1+C2x*D2x)*(2*ProbH-1))
    cx = (C2x+D1x)/(1+C2x*D1x)
    cy = 0
    #cz = C2z*D1z/((1+C2x*D1x)*cos(2*z)*(2*V-1))
    cz = C2z*D1z/((1+C2x*D1x)*(2*ProbH-1))
    dx = (C1x+D2x)/(1+C1x*D2x)
    dy = 0
    #dz = C1z*D2z/((1+C1x*D2x)*cos(2*z)*(2*V-1))
    dz = C1z*D2z/((1+C1x*D2x)*(2*ProbH-1))
    #deal with singular case where z denominators are zero; in this case 4-state solution may fail but
    #can find 3 conditional states as long as either az or bz or cz or dz has magnitude <=1. 
    if abs(ProbH-0.5)<0.01:
        if abs(az)<=1 or abs(bz)<=1 or abs(cz)<=1 or abs(dz)<=1:
            return []
    #lengths of those LHS Bloch vectors (legit if all less than or equal to 1)
    asq = ax**2+ay**2+az**2
    bsq = bx**2+by**2+bz**2
    csq = cx**2+cy**2+cz**2
    dsq = dx**2+dy**2+dz**2
    maxBloch=max(asq,bsq,csq,dsq)
    
    if maxBloch<=1:
        return []
    else:
        #print("For omegaHWP=",omegaindex*step,": asquared=",asq,", bsquared=",bsq,", csquared=",csq,", dsquared=",dsq,".")
        #calculate a bunch of things to get Xb and Xg from 2014 PRL proof
        blochangle = pi/2-(abs(alpha)+abs(beta)) #this is angle up from x axis on Bloch sphere, so 90 minus 2*(mean of alpha, beta).
        if blochangle == 0:
            blochangle = 0 + 0.000000000001 #to avoid numerical error below
        r1 = 1-2*max(eAlpha,eBeta)
        z0 = 2*(ProbH)-1
        Xb = (z0 - r1*(cos(blochangle))**2/(sin(blochangle)) - r1*sin(blochangle))*(-1)*tan(blochangle)
        Ez = 1-2*ePhi
        Ex = sqrt(1-Ez**2)
        Fz = 1-2*eGamma
        Fx = sqrt(1-Fz**2)
        Xg = (z0-Ez)*(Ex-Fx)/(Ez-Fz) + Ex
        
        if abs(Xb) <= abs(Xg):
            return [[],[],[maxBloch],['OmegaHWP:',omegaindex*step,'OmegaperpHWP:',omegaperpindex*step,'AlphaHWP:',alphaindex*step,'AlphaperpHWP:',alphaperpindex*step,'BetaHWP:',betaindex*step,'BetaperpHWP:',betaperpindex*step]]
        else:
            return [[round(Xb,4)],[round(Xg,4)],[maxBloch],['OmegaHWP:',omegaindex*step,'OmegaperpHWP:',omegaperpindex*step,'AlphaHWP:',alphaindex*step,'AlphaperpHWP:',alphaperpindex*step,'BetaHWP:',betaindex*step,'BetaperpHWP:',betaperpindex*step]]

   
#call onewaysteeringtest with the data array [created by readcvsinpython routine(s)] and Alice/Bob as arguments.
#does not find alpha, but tries every Alice angle as alpha.
def onewaysteeringtest(countsL,errorsL,steeringparty,errorcond):
    '''Finds omega and alpha, and does cases for what we consider alphaperp.'''
    violationL=[] #if nonempty, Bob may be able to steer Alice (we can't claim he can't)
    for omegaindex in range(len(countsL)): #loop through all Bob angles in the data (should be all rows of Excel file)
        omegaperpindex = (omegaindex+index_plus45) % possible_angles
        omegacountsmax = max(countsL[omegaindex])
        alphaindex1 = countsL[omegaindex].index(omegacountsmax)
        omegacountsmin = min(countsL[omegaindex])
        alphaperpindex2 = countsL[omegaindex].index(omegacountsmin)

        #if max counts and min counts not 45 deg offset, then see which one comes closer to pure state
        alphaperpindex1 = (alphaindex1+index_plus45) % possible_angles
        alphaindex2 = (alphaperpindex2 + index_plus45) % possible_angles

        eAlpha1 = countsL[omegaindex][alphaperpindex1]/(countsL[omegaindex][alphaindex1] + countsL[omegaindex][alphaperpindex1])
        eAlpha2 = countsL[omegaindex][alphaperpindex2]/(countsL[omegaindex][alphaindex2] + countsL[omegaindex][alphaperpindex2])
        if eAlpha2 < eAlpha1:
            alphaindex = alphaindex2
            alphaperpindex = alphaperpindex2
        else:
            alphaindex = alphaindex1
            alphaperpindex = alphaperpindex1

        omegaperpcountsmax = max(countsL[omegaperpindex])
        betaindex1 = countsL[omegaperpindex].index(omegaperpcountsmax)
        omegaperpcountsmin = min(countsL[omegaperpindex])
        betaperpindex2 = countsL[omegaperpindex].index(omegaperpcountsmin)
        #if max counts and min counts not 45 deg offset, then see which one comes closer to pure state
        betaperpindex1 = (betaindex1+index_plus45) % possible_angles
        betaindex2 = (betaperpindex2 + index_plus45) % possible_angles

        eBeta1 = countsL[omegaperpindex][betaperpindex1]/(countsL[omegaperpindex][betaindex1] + countsL[omegaperpindex][betaperpindex1])
        eBeta2 = countsL[omegaperpindex][betaperpindex2]/(countsL[omegaperpindex][betaindex2] + countsL[omegaperpindex][betaperpindex2])
        if eBeta2 < eBeta1:
            betaindex = betaindex2
            betaperpindex = betaperpindex2
        else:
            betaindex = betaindex1
            betaperpindex = betaperpindex1

        #print("omegaindex ", Bobangle, ", alphaindex ", alphaindex, ", betaindex ", betaindex, ".")

        violationL += [conditionalstates3(alphaperpindex,betaindex,betaperpindex,omegaperpindex,countsL,errorsL,omegaindex,alphaindex,steeringparty,errorcond)]
        #violationL += [conditionalstates1(alphaperpindex2,betaindex1,betaperpindex1,omegaperpindex,countsL,Bobangle,alphaindex2,steeringparty)]
        #violationL += [conditionalstates1(alphaperpindex1,betaindex2,betaperpindex2,omegaperpindex,countsL,Bobangle,alphaindex1,steeringparty)]
        #violationL += [conditionalstates1(alphaperpindex2,betaindex2,betaperpindex2,omegaperpindex,countsL,Bobangle,alphaindex2,steeringparty)]
            #if probcond >= limit:
                    #violationL += [conditionalstates1(alphaperpindex,potentialBetaAngle,betaperpindex,omegaperpindex,countsL,Bobangle,Aliceangle,steeringparty)]
            #if (Aliceangle-9)%(len(countsL[Bobangle])-1)!=(Aliceangle+9)%(len(countsL[Bobangle])-1)
            #    alphaperpindex=(Aliceangle-9) % (len(countsL[Bobangle])-1)

            #    probcond=(countsL[Bobangle][Aliceangle])/(countsL[Bobangle][Aliceangle] + countsL[Bobangle][alphaperpindex])
            #    if probcond >= limit:
            #        violationL += [conditionalstates1(alphaperpindex,countsL,Bobangle,Aliceangle,steeringparty)]
            
            #if Aliceangle <= 9:
             #   alphaperpindex=Aliceangle+9
             #   probcond=(countsL[Bobangle][Aliceangle])/(countsL[Bobangle][Aliceangle] + countsL[Bobangle][Aliceangle+9])
             #   if probcond >= limit:
             #       violationL+=[conditionalstates1(alphaperpindex,countsL,Bobangle,Aliceangle,steeringparty)]
            #case below will go away if data only goes from 0 to 90 degrees on HWP.
            #if Aliceangle >9 and Aliceangle <12: #has two cases, one in which the orthogonal is pi/4 above and one in which it is pi/4 below Alice's angle
            #    probcond1=(countsL[Bobangle][Aliceangle])/(countsL[Bobangle][Aliceangle] + countsL[Bobangle][Aliceangle+9])
            #    alphaperpindex1=Aliceangle+9
            #    probcond2=(countsL[Bobangle][Aliceangle])/(countsL[Bobangle][Aliceangle] + countsL[Bobangle][Aliceangle-9])
            #    alphaperpindex2=Aliceangle-9
            #    if probcond1 >= limit:
            #        violationL+=[conditionalstates1(alphaperpindex1,countsL,Bobangle,Aliceangle,steeringparty)]
            #    if probcond >= limit: #should have been probcond2
            #        violationL+=[conditionalstates1(alphaperpindex2,countsL,Bobangle,Aliceangle,steeringparty)]
            #case below will turn into >9 if data only goes from 0 to 90 degrees on HWP.
            #if Aliceangle >=12:
            #    alphaperpindex=Aliceangle-9
            #    probcond=(countsL[Bobangle][Aliceangle])/(countsL[Bobangle][Aliceangle] + countsL[Bobangle][Aliceangle-9])
            #    if probcond >= limit:
            #        violationL+=[conditionalstates1(alphaperpindex,countsL,Bobangle,Aliceangle,steeringparty)]

    #all the stuff with the counter is for the case where there's duplicate data at a single polarization.  Maybe get rid of it all if data only taken from 0 to 90 on HWPs.
    #actually the statement above seems NOT to be true.
    counter=0
    violationsNonempty=[]
    for element1 in violationL: #as a result of the cases where Aliceangle is >9 and <12, some weirdly-formatted lists arise. The next two for-loops unelegantly solve that.
        #print(element1)
        if element1 == [] or element1==[[],[]]:
            #violationL.remove(element1)
            #violationL.append(element1)
            counter+=1
        else:
            violationsNonempty.append(element1)
    print("Number of omegas without violation is ", counter)
    #violationL=violationL[:-counter]
    violationsActual = []
    for element2 in violationsNonempty:
        if len(element2)==2: 
            violationsActual+=element2[0],element2[1]
        else:
            violationsActual.append(element2)

    violationsStringent = []
    for element3 in violationsActual:
        if element3[0] != []:
            violationsStringent.append(element3)
    

    #the stuff below is NOT for duplicate angle cleanup.  It is needed.
    biggestviolation=0
    violationindex=0
    for element0 in violationsActual:
        if element0[0] != []:
            if type(element0[2][0]) == float:
                violationsize=element0[2][0]-1
            if type(element0[2][0]) == list: #accounts for my messy code to get the same variable desired
                violationsize=element0[0][2][0]-1
            if abs(violationsize) >=abs(biggestviolation):
                biggestviolation=violationsize
                violationindex=violationsActual.index(element0)
    if len(violationsActual) != 0:
        print("This is the maximum violation setting:", violationsActual[violationindex])
        for element2 in violationsActual:
            print(element2)
    if len(violationsActual) == 0:
        print("There is no violation of the a,b,c,d criterion to indicate steering.")
    print("We found ", len(violationsActual), " violations overall.")
    print("")

    biggeststringent=0
    stringentindex=0
    for element0 in violationsStringent:
        if element0[0] != []:
            if type(element0[0][0]) == float:
                violationsize=element0[0][0]-element0[1][0]
            if type(element0[0][0]) == list: #accounts for my messy code to get the same variable desired
                violationsize=element0[0][0][0]-element0[0][1][0]
            if abs(violationsize) >=abs(biggeststringent):
                biggeststringent=violationsize
                stringentindex=violationsStringent.index(element0)
    if len(violationsStringent) != 0:
        print("This is the maximum stringent violation setting:", violationsStringent[stringentindex])
        for element2 in violationsStringent:
            print(element2)
    if len(violationsStringent) == 0:
        print("There is no violation of the stringent criterion to indicate steering.")
    print("We found ", len(violationsStringent), " stringent violations overall.")
