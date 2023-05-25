# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:26:35 2018

@author: Nick
"""
import initialize_the_motors
import time
states = "HhVvAaDdRrLlsSbBpPzZ" 
# The capital and lowercase versions of HVADRLSBPZ.

class AllMotors:
    
    def __init__(self, serial_numbers):
        # serial_numbers is a list of serial numbers used to control the motors
        # in the order Alice HWP, Alice QWP, and then Bob's HWP.
        if len(serial_numbers) < 3:
            raise ValueError("expected at least 3 motors to be controlled")
        # Initialize all the motors.
        self.AHWP = initialize_the_motors.aptWrapper(serial_numbers[0], "AHWP")
        self.AQWP = initialize_the_motors.aptWrapper(serial_numbers[1], "AQWP")
        self.BHWP = initialize_the_motors.aptWrapper(serial_numbers[2], "BHWP")
        self.BQWP = initialize_the_motors.aptWrapper(serial_numbers[3], "BQWP")
        self.state = self.reset() # Move everything to measure HH.
        
        self.motorList = [self.AHWP, self.AQWP, self.BHWP, self.BQWP]
    def __repr__(self):
        
        output = "This is a class used to control Alice's HWP, and QWP as well"
        output += " Bob's HWP and Bob's QWP (requires human input for BQWP)."
        output += "/n" + "Alice HWP: " + self.AHWP.position() + "/n"
        output += "Alice QWP: " + self.AQWP.position() + "/n"
        output += "Bob HWP: " + self.BHWP.position() + "/n"
        output += "Bob QWP should be at "+ self.Bob_QWP_RL_Settings[self.state]
        output += "/n" + "This corresponds to the state: " + self.state
        return output
               
    def move_to(self, State):
        # This function assumes that there is a move_quick function in
        # the class aptWrapper
        if type(State) == str:
            print(State)
            # Confirm the input is the right type
            if "_" in State:
                Splice = State.index("_")
                A_State = State[0:Splice]    # Alice's state is in the first index
                B_State = State[Splice+1:] # Bob's state is in the second index.
            else:
                A_State = State[0]
                B_State = State[1]
            if A_State in states:
                print("states,",states)   ###edit
                if B_State in states:
                    # We can reach this state with the motors so move there
                    self.AHWP.move_to(str(A_State).upper())
                    self.AQWP.move_to(str(A_State).upper())
                    self.BHWP.move_to(str(B_State).upper())
                    self.BQWP.move_to(str(B_State).upper())
                    # So that the delay does not start 
                    # until all the motors have moved to their proper location.
                    return True
                else:
                    raise ValueError("The value of the second index you entered is not a valid state")
            else:
                raise ValueError("The value of the first index is not a valid state")

        elif type(State) == tuple:
            # A coordinate pair of angles or a 4 tuple.
            if len(State) == 2:
                # Move both of Alice's plates to the first and Bob's to the second.
                A_State = State[0:State.index("_")]             #prev: A_State = State[0]
                B_State = State[State.index("_")+1:-1]          #prev: B_State = State[1]
                self.AHWP.move_to(A_State)
                self.AQWP.move_to(A_State)
                
                self.BHWP.move_to(B_State)
                self.BQWP.move_to(B_State)
                
            elif len(State) == 4:
                AH = State[0]
                AQ = State[1]
                BH = State[2]
                BQ = State[3]
                
                self.AHWP.move_to(AH)
                self.AQWP.move_to(AQ)
                self.BHWP.move_to(BH)
                self.BQWP.move_to(BQ)
                
            else:
                raise ValueError("Invalid tuple")
        else:
            raise ValueError("The value you input is not a string or tuple. It is " + type(stringState))
    
    def reset(self):
        self.move_to("HH")
    
serial_numbers = [83811667, 83811904, 83811901, 83811646]    

Motors = AllMotors(serial_numbers)
