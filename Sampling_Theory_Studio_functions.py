import numpy as np
import pandas as pd
from Signal_Class import Signal
import plotly.express as px


#________Initializing variables_______#
signal_default_time = np.arrange(0,1,0.001)    #1000 default samples for the time axis   


signal_default_values = np.zeros(len(signal_default_time))    

max_frequency = 1   

Final_signal_sum = None       

total_signals_list = [Signal(amplitude=1,frequency=1,phase=0)]  #contains all individual signals (freq components) forming the final or resulted signal   

signals_uploaded_list = []

generate_sine_signal =  None

snr_value = 50       



#__________Main Functions_______#

#Continue 
def generate_noisy_signal(snr_level):
    
    #Generates a noisy signal with a controllable SNR level.
    
    #Args:
     #   snr_level (float): The desired SNR level in dB.
    #Returns:
      #noisy_signal (ndarray): The generated noisy signal.
      
 
      
    temp_signal = Final_signal_sum 
    signal_mean = np.mean(temp_signal)
     
    
    # Generate the signal
   # time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    
    # Calculate the power of the signal
    signal_power = np.sum((temp_signal-signal_mean) ** 2) / len(temp_signal)
    
    # Calculate the noise power based on the desired SNR level
    linear_ratio = 10 ** (snr_level / 10)  # Convert dB to power ratio
    noise_power = signal_power / linear_ratio 
    
    # Generate white noise with the same length as the signal
    noise = np.random.normal(0,np.sqrt(noise_power), size=len(temp_signal))
    
  
    return noise
  
 
def generateFinalSignal(noise_flag,signal_uploaded_browser,SNR=40):
    """
    This function checks if there is an uploaded signal from browser and checks if there is added
    noise, it then adds all signals (mixer,browser,noise) and generates a final signal.
    
    noise_flag:bool check if there is noise added
    signal_uploaded_browser: uploaded signal from browser
    SNR: Signal-to-noise ratio
    """
    
    global Final_signal_sum
    
    if signal_uploaded_browser is not None:
        
        temp_final_signal = signal_uploaded_browser.copy()        
    else:
        temp_final_signal = signal_default_values.copy()          
              
    
    for signal in total_signals_list:      
        temp_final_signal+=signal.amplitude*np.sin(signal.frequency*2*np.pi*signal_default_time + signal.phase* np.pi )
    
    
    if noise_flag:
        Final_signal_sum = temp_final_signal + generate_noisy_signal(SNR)   
    
    else:
        Final_signal_sum = temp_final_signal
      
    
    return pd.DataFrame(Final_signal_sum,signal_default_time)





def addSignalToList(amplitude, frequency, phase):
    """
    Add signals to added_list
    :param amplitude: the amplitude of the signal
    :param frequency: the frequency of the signal
    :param phase: the phase of the signal
    """
    global max_frequency
    signal = Signal(amplitude=amplitude, frequency=frequency, phase=phase)
    total_signals_list.append(signal)
    max_frequency = max(max_frequency, signal.frequency)


def removeSignalFromList(amplitude, frequency, phase):
    
    """
    remove signals from added_list
    Parameters
    ----------
    amplitude : float
    the amplitude of the signal
    frequency : float
    the frequancy of the signal
    phase : float
    the phase of the signal
    """

    for i in range(len(total_signals_list)):
        if total_signals_list[i].amplitude == amplitude and total_signals_list[i].frequency == frequency and total_signals_list[i].phase == phase:
            total_signals_list.pop(i)
            break

    #if max_frequency == frequency:
     #   reset_maximum_frequency()


