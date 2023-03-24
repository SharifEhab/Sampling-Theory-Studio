class Signal():
    
    def __init__(self,amplitude,frequency,phase) :
        
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        
"""
This class is used to represent our signals, where each signal is an object        

Defined only a constructor that takes 3 attributes to define the signal object

amplitude: float 
represent magnitude of the signal

frequency: float 
corresponds to number of cycles per unit time

phase : float
how far the signal is shifted 

"""