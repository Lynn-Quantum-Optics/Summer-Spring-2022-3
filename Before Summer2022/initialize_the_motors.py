# Initialization Of the Motors Script
import thorlabs_apt as apt
serial_numbers = [83811904, 83811667, 83811901, 83811646]























  
# A dictionary of dictionaries of all the settings for the half wave plates.
WavePlateSettings = { 83811904 : # This is Alice's QWP
    # Settings are in the form H, V, D, A, R, L for all wave plates
    {"H": 0.46, "V": 0.46, "D": 0.46, "A": 0.46, "R": 135.46, "L": 45.46, 
    "B":  0.46, "P":  0.46, "Z": 0.46, "S": 0.46,
    "Arbitrary" : 0}#An internal dictionary.
    
    , 83811901 : # This is Bob's HWP
    # Settings are in the form H, V, D, A, R, L for all wave plates
    {"H": -6.12, "V": 38.88, "D": 61.38, "A": 16.38, "R": -6.12, "L": -6.12,
    "P": 50.13, "B": 5.13, "Z": 27.63, "S": -17.37, "Arbitrary" : 0}

    # For theta = pi/8
    # P=50.46 B=5.46 Z=27.96 S=72.96

    # For theta = pi/4
    # P=61.71 B=16.71 Z=16.71 S=61.71

    # For theta = pi/16
    # P=44.835 B=89.835 Z=33.585 S=78.585

    # For theta = 3pi/16
    # P=56.085 B=11.085 Z=22.335 S=67.335
    
    , 83811667 : # This is Alice's HWP
    # Settings are in the form H, V, D, A, R, L for all wave plates
    {"H": -1.10, "V": 43.9, "D": 66.4, "A": 21.4, "R": -1.1, "L": -1.1,
    "P": 55.15, "B": 10.15, "Z": 32.65, "S": -12.35, "Arbitrary" : 0}#An internal dictionary.
    
    , 83811646 : # This is Bob's QWP
     # Settings are in the form H, V, D, A, R, L for all wave plates
    {"H": 97.08, "V": 97.08, "D": 97.08, "A": 97.08, "R": 232.08, "L": 142.08, "B": 97.08,
    "P": 97.08, "Z": 97.08, "S": 97.08, "Arbitrary" : 0}
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

Bob_QWP = aptWrapper(83811646, "Bob QWP")
Alice_HWP = aptWrapper(83811667, "Alice HWP")
Alice_QWP = aptWrapper(83811904, "Alice QWP")
Bob_HWP = aptWrapper(83811901, "Bob HWP")

