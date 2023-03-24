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
def produce_Noise_signal(SNR):
    
    noise = np.random.normal(0,1,1000)
    return noise  

  
  #This function 
def generateFinalSignal(noise_flag,signal_uploaded_browser,SNR=40):
    global Final_signal_sum
    
    if signal_uploaded_browser is not None:
        
        temp_final_signal = signal_uploaded_browser.copy()        
    else:
        temp_final_signal = signal_default_values.copy()          
              
    
    for signal in total_signals_list:      
        temp_final_signal+=signal.amplitude*np.sin(signal.frequency*2*np.pi*signal_default_time + signal.phase* np.pi )
    
    
    if noise_flag:
        Final_signal_sum = temp_final_signal + produce_Noise_signal(SNR)   
    
    else:
        Final_signal_sum = temp_final_signal
      
    
    return pd.DataFrame(Final_signal_sum,signal_default_time)










