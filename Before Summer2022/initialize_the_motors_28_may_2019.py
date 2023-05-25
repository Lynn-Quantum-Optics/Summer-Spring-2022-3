# Initialization Of the Motors Script
import thorlabs_apt as apt
serial_numbers = [83811904, 83811667, 83811901, 83811646]
serial_numbers = [83811667, 83811901]
  
# A dictionary of dictionaries of all the settings for the half wave plates.
WavePlateSettings = { #83811904 : # This is Alice's QWP
    # Settings are in the form H, V, D, A, R, L for all wave plates
 #   {"H": -1.765, "V": -1.765, "D": -1.765, "A": -1.765, "R": 133.235, "L": 43.235, 
  #  "B":  -1.765, "P":  -1.765, "Z": -1.765, "S": -1.765,
   # "Arbitrary" : 0}#An internal dictionary.
    
    #,
    83811901 : # This is Bob's HWP
    # Settings are in the form H, V, D, A, R, L for all wave plates
    {"H": -5.37, "V": 39.63, "D": 62.13, "A": 17.13, "R": -5.37, "L": -5.37,
    "P": 50.88, "B": 5.88, "Z": 28.38, "S": 73.38, "Arbitrary" : 0}
    
    , 83811667 : # This is Alice's HWP
    # Settings are in the form H, V, D, A, R, L for all wave plates
    {"H": -1.82, "V": 43.18, "D": 65.68, "A": 20.68, "R": -1.82, "L": -1.82,
    "P": 54.43, "B": 9.46, "Z": 31.93, "S": 76.93, "Arbitrary" : 0}#An internal dictionary.
    
#    , 83811646 : # This is Bob's QWP
     # Settings are in the form H, V, D, A, R, L for all wave plates
 #   {"H": 96.98, "V": 96.98, "D": 96.98, "A": 96.98, "R": 231.98, "L": 141.98, "B": 96.98,
  #  "P": 96.98, "Z": 96.98, "S": 96.98, "Arbitrary" : 0}
    }# Arbitrary is the state used for when the angle is directly specified.

class aptWrapper():
    """This class allows you to control the motor based upon its serial number.
    It also overloads the move_to command to take in strings as inputs so that
    it is easier to read when the command issued is printed.
    """
    def __init__(self, serial_num, Identifier): # Parameterized Constructor.
        if serial_num not in serial_numbers:
            raise ValueError("Serial Number not found")
        else:
            self.serial_num = serial_num
            
            # Initialize the appropriate equipment.
            self.motor = apt.Motor(serial_num)
            
            self.settings = WavePlateSettings[serial_num]
            
            self.name = Identifier
            
            self.state = "X"
            # Set the initial state to be X. 
            # This will be changed every move_to call
            
    
    def __repr__(self):
        # The representation of an object of aptWrapper when it is printed.
        string = str(self.name) + " is at " + str(self.angle()) + " degrees."
        return string
        
    def move_to(self, State, blocking=True):
        """ Moves the motor to the angle input through a float or a string which corresponds to a float value
        in this motor's dictionary of preset states. The blocking variable indicates whether or not you want the
        program to wait until this motor has finished moving before another command can be issued.
        """
        if type(State) == str:
            if State in self.settings.keys():
                if self.state != State:
                    print("Valid State: " + State)
                    print("Moving " + self.name + " to setting: " + State)
                    print("Command Issued: " + "self.motor.move_to(" + str(self.settings[State]) + ",True)")
                    self.motor.move_to(self.settings[State], blocking)
                    self.state = State
                    return
                else:
                    print(self.name + "is already at state: " + State)
                    print("Moving to next controller now.")
                    return
            else:
                # Throwing the error should stop all code at this point;
                # so no need to check what is returned.
                raise ValueError("Inappropriate string state was input."+ 
                "The valid options are H,V,D,A,R,L,S,B,Z,P")
        elif type(State) == float or type(State) == int:
            angle = float(State)%360
            self.motor.move_to(angle, True)
            self.state = "Arbitrary"
            print("Valid Angle: " + str(angle))
            print("Moving " + self.name + " to setting: " + str(angle))
            print("Command Issued: " + "self.motor.move_to(" + str(angle) + ",True)")
            return
        
    def move_quick(self, State):
        """ Same as self.move_to but with no option to block the movement of other motors."""
        self.move_to(State, blocking=False)
        return            
            
    def angle(self):
        return self.motor.position

#Bob_QWP = aptWrapper(83811646, "Bob QWP")
Alice_HWP = aptWrapper(83811667, "Alice HWP")
#Alice_QWP = aptWrapper(83811904, "Alice QWP")
Bob_HWP = aptWrapper(83811901, "Bob HWP")

