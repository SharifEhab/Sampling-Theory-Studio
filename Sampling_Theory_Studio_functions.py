import numpy as np
import pandas as pd
from Signal_Class import Signal
import plotly.express as px
import streamlit as st
import base64
from scipy.fftpack import fft


#___Initializing variables__#
signal_default_time = np.arange(0,4,0.001)    #1000 default samples for the time axis   


signal_default_values = np.zeros(len(signal_default_time))    

max_frequency = 1   

Final_signal_sum = None       

total_signals_list = [Signal(amplitude=1,frequency=1,phase=0)]  #contains all individual signals (freq components) forming the final or resulted signal   

signals_uploaded_list = []

generate_sine_signal =  None

snr_value = 50       



#___Main Functions__#




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
        temp_final_signal+=signal.amplitude*np.cos(signal.frequency*2*np.pi*signal_default_time + signal.phase* np.pi )
    
    
    if noise_flag:
        Final_signal_sum = temp_final_signal + generate_noisy_signal(SNR)   
    
    else:
        Final_signal_sum = temp_final_signal
      
    Final_signal_data={'Time':signal_default_time, 'Amplitude':Final_signal_sum}
    Final_sig_dataframe = pd.DataFrame(Final_signal_data)
    return Final_sig_dataframe


def interpolate(time_new, signal_time, signal_amplitude):

    """
        Sinc Interpolation
        Parameters
        ----------
        time_new : array of float
            new time to smple at
        signal_time : array of float
            samples of time
        signal_amplitude : array of float
            amplitudes at signal_time 
        Return
        ----------
        new_Amplitude : array of float
            new amplitudes at time_new
            
        ## Interpolation using the whittaker-shannon interpolation formula that sums shifted and weighted sinc functions to give the interpolated signal
        ## Each sample in original signal corresponds to a sinc function centered at the sample and weighted by the sample amplitude
        ## summing all these sinc functions at the new time array points gives us the interploated signal at these points.     
    """


    # sincM is a 2D matrix of shape (len(signal_time), len(time_new))
    
    # By subtracting the sampled time points from the interpolated time points
    
    sincMatrix = np.tile(time_new, (len(signal_time), 1)) - np.tile(signal_time[:, np.newaxis], (1, len(time_new)))

    # sinc interpolation 
    
    #This dot product results in a new set of amplitude values that approximate the original signal at the interpolated time points.
    signal_interpolated = np.dot(signal_amplitude, np.sinc(sincMatrix/(signal_time[1] - signal_time[0])))   
    return signal_interpolated



def renderSampledSignal(nyquist_rate, is_normalized_freq):
    """
        render sampled and interpolated signal
        Parameters
        ----------
        nyquist_rate : float
            F_sample/max_frequency
        Return
        ----------
        fig : Figure
            plot of the interpolated sampled signal
        downloaded_df : Dataframe
            the resulted signal to be downloaded
    """
    global max_frequency
    
    
    if is_normalized_freq:
       time  = np.arange(0, signal_default_time[-1], 1/(nyquist_rate * max_frequency))         
    else:
        time = np.arange(0, signal_default_time[-1], 1/(nyquist_rate))


    # points on graph  , 20 , amp of sample 
    y_samples = interpolate(time, signal_default_time, Final_signal_sum )  #sampling/samples taken with input sampling frequency

    # amp of reconstructed 
    y_interpolated = interpolate(signal_default_time, time, y_samples)   # interploated signal or reconstructed signal
    df = pd.DataFrame(signal_default_time, y_interpolated)

 # Original signal with markers for sampled points
    original_signal = px.scatter(x=time, y=y_samples , labels={"x": "Time (s)", "y": "Amplitude (mv)"}, color_discrete_sequence=['red'])
    original_signal['data'][0]['showlegend'] = True
    original_signal['data'][0]['name'] = ' Samples '
    original_signal.add_scatter(name="Original_Signal", x=signal_default_time, y=Final_signal_sum,line_color = 'blue' )
    original_signal.update_traces(marker={'size': 10})
    original_signal.update_layout( showlegend=True, margin=dict(l=50, r=50, t=50, b=50), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), height=330) 
    original_signal.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
    original_signal.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
    
    # Reconstructed signal along with sampling points/markers
    constructed_signal = px.scatter(x=time, y=y_samples , labels={"x": "Time (s)", "y": "Amplitude (mv)"}, color_discrete_sequence=['red'])
    constructed_signal['data'][0]['showlegend'] = True
    constructed_signal['data'][0]['name'] = ' Samples '
    constructed_signal.add_scatter(name="Reconstructed",x=signal_default_time, y=y_interpolated,  line_color="#FF4B4B")
    constructed_signal.update_traces(marker={'size': 10}, line_color="#FF4B4B")
    constructed_signal.update_layout( showlegend=True, margin=dict(l=50, r=50, t=25, b=50), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), height=330)  
    constructed_signal.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
    constructed_signal.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))

    # Difference between original and reconstructed signal
    difference_signal = px.scatter(x =signal_default_time,y =Final_signal_sum - y_interpolated, labels={"x": "Time (s)", "y": "Amplitude (mv)"}, color_discrete_sequence=['red'])
    difference_signal.add_scatter(name="Difference", x =signal_default_time,y =Final_signal_sum - y_interpolated,line_color='Green')
    difference_signal.update_traces(marker={'size': 1.5})
    difference_signal.update_layout( showlegend=True, margin=dict(l=50, r=50, t=25
                                                                  , b=50), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), height=330)  
    difference_signal.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
    difference_signal.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))

    return original_signal, constructed_signal, difference_signal,df.drop(df.columns[[0]], axis=1)  # returns 3 figs along with interpolated signal values where each row corresponds to interpolated signal value at specific time point.





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
    max_frequency = float(max(max_frequency, signal.frequency))



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

    for signals in total_signals_list:
        if signals.amplitude==amplitude and signals.frequency == frequency and signals.phase == phase:
            total_signals_list.remove(signals)        

    if max_frequency == frequency:
        SetmaxFreq()


def cosGeneration(amplitude, Freq, phase):
    global generate_sine_signal
    generate_sine_signal=np.cos(2*np.pi*(signal_default_time*Freq)+phase*np.pi)*amplitude
    


def SetmaxFreq(): #set the maximum freq where loops on the signal stored by the user and select the max frequency uploaded by the user
    findMaxFreq = 1
    global max_frequency
    for signals in total_signals_list:
        findMaxFreq = max(findMaxFreq ,signals.frequency )
             

    max_frequency= float(findMaxFreq)


def get_Total_signal_list():
    return total_signals_list


def set_snr_level(snr_level):
    global snr_value
    snr_value = snr_level


def get_snr_level():
    global snr_value
    return snr_value 

def Reintialize_values():
    global signal_default_time, max_frequency
    signal_default_time = np.arange(0,4,0.001)       
    max_frequency = 1
    
    for signals in  total_signals_list : 
        if signals.frequency > max_frequency:
            max_frequency = float(signals.frequency)
        


def SignalListClean():
   global max_frequency
   max_frequency=1.0
   total_signals_list.clear()
   
def signal_set_time(array_time,F_sample):
    global signal_default_time,max_frequency
    signal_default_time = array_time.copy()
    max_frequency = float(F_sample/2)
    



def calculate_max_freq_uploadedfile(signal_amp,signal_time):
    """
    uses the Fast Fourier Transform (FFT) to find the frequency domain representation of the signal
    
    """
    n = len(signal_time)  # Get number of samples in signal amp array
    Fs = 1 / (signal_time[1] - signal_time[0]) #sampling frequency
    signal_freq = fft(signal_amp) / n  #Apply FFT to sig_amp results in array of complex values representing amplitude and phase of each component 
    #which is likely imported from a library (e.g., NumPy or SciPy). The result is an array of complex values representing the amplitude and phase of each frequency component in the signal. The array is then divided by n to normalize the amplitudes.
    freqs = np.linspace(0, Fs / 2, n // 2)  #array of frequencies based on Fs 
    max_freq_index = np.argmax(np.abs(signal_freq[:n//2]))  #get index of highest magnitude in frequency components
    max_freq = freqs[max_freq_index]  #Get the frequency corresponding to greatest magnitude
    return max_freq    #Return max frequency




def download_final_signal(data_frame):
    csv = data_frame.to_csv(index=False)   #convert pandas df to a csv string and removes indexing
    b64 = base64.b64encode(csv.encode()).decode()
    #csv.encode(): This is a method in Python that encodes the string csv into bytes using the default encoding (usually UTF-8).
    #base64.b64encode(csv.encode()): This is a function from the base64 module that takes the encoded bytes
    # and encodes them using the Base64 algorithm, which converts binary data into ASCII characters for safe transport over text protocols, such as email or HTTP.
    """
    Base64-encoded version of csv string
     This is done by first encoding the csv string into bytes using the .encode() method, then using the b64encode() function from the base64 module to encode those bytes as Base64.

The resulting Base64-encoded string is then decoded using the decode() method to get a regular string.

This encoding and decoding is necessary for creating a URL-safe representation of the csv data, which can then be used in the href attribute of the download link.

    """
    
    file_name = 'Downloaded_signal.csv'
    data = f'data:file/csv;base64,{b64}' #create data url scheme
    download_button_str = f'<a href="{data}" download={file_name}>Download CSV File</a>' #html string for the download button
    st.markdown(download_button_str, unsafe_allow_html = True) #display button in app
   #The unsafe_allow_html=True argument is needed because the download_button_str variable contains HTML code.
     
    