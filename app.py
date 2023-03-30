import streamlit as st
import pandas as pd
import numpy as np 
import Sampling_Theory_Studio_functions as functions 
from math import ceil
import csv 
import random
st.set_page_config(page_title="Sample", page_icon=":radio:", layout="wide")

# ___________ Elements styling ___________ #

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define a function to upload a CSV file and return its content as a Pandas DataFrame
def read_csv_file(file):
    if file is not None:
        data = pd.read_csv(file, usecols=["Time", "Amplitude"])
        return data
    else:
        return None

#____________Variables____________#
dropdown_signal_list = []
file_signal_amplitude = None

# SIDEBAR SECTION
with st.sidebar:
    st.markdown('<h1 class="sidebar-title">Manage Signals</h1>', unsafe_allow_html=True)
    file = st.file_uploader("Choose a CSV file", type="csv")
    if file is not None:
        signal = read_csv_file(file)
        file_signal_amplitude = signal['Amplitude'].values
    else:
        functions.Reintialize_values()
            
    add_noise = st.checkbox("Noise",False)
    if add_noise:
        noise_level = st.slider("SNR", 1, 100, 50)
    else:
        noise_level = 1
            
    st.markdown("---")
    
    st.write("Signal Properties")

    amp_slider_col, phase_slider_col = st.columns(2)
    
    with amp_slider_col:
        amplitude_slider = st.slider("Amplitude", 0.1,1.0,0.1,0.01,format="%f") #(min,max,default,step)
    
    with phase_slider_col:
        phase_slider = st.slider('Phase', 0.0, 2.0, 0.0, 0.1, format="%fπ")
    
    frequency_slider = st.slider("Frequency", 0.5, 20.0, 10.0, 0.1, format="%f")

    AddSignalButton=st.button("Add Signal",key="addbutton")
    
    if AddSignalButton:
        functions.addSignalToList(amplitude_slider,frequency_slider,phase_slider)
        
    for signal in functions.get_Total_signal_list():
        
        dropdown_signal_list.append(f"Signal : Amp: {signal.amplitude:n} / Freq: {signal.frequency:n} / Phase: {signal.phase:n} π")    
    selected_signals = st.selectbox("Signals", dropdown_signal_list) 
    split_signals_to_strings = str(selected_signals).split(" ") 
    if len(split_signals_to_strings) !=1:
        amp_slider = float(split_signals_to_strings[3])
        freq_slider = float(split_signals_to_strings[6])
        ph_slider = float(split_signals_to_strings[9]) 
      
        
    remove_col,clear_col = st.columns(2)

    with remove_col:
        signal_remove_button = st.button("Remove",key="remove_butt",disabled = len(functions.get_Total_signal_list())<=0)
        
        if signal_remove_button:
            functions.removeSignalFromList(amp_slider,freq_slider,ph_slider)
            st.experimental_rerun()

    with clear_col:
        
        signals_clear_button = st.button("Clear", key="clear_button",disabled = len(functions.get_Total_signal_list())<=0)
        
        if signals_clear_button:
            functions.Reintialize_values()
            functions.SignalListClean()
            st.experimental_rerun()

    st.markdown("---")
    

    st.header("Sampling")
    is_normalized = st.checkbox("Normalized",False)
    if is_normalized:
        sample_rate = st.slider("Sampling rate Fs/Fmax", 0.1, 6.0, 1.0, 0.1, format="%f")
    else:
        sample_rate = st.slider("Fs",max(1.5,ceil(functions.max_frequency*0.5)*1.0),4.0*functions.max_frequency,1.0*functions.max_frequency,0.5,format="%f")
        

# HEADER SECTION
with st.container():
    st.title("Task 2 – Sampling-Theory Studio")
    functions.sinGeneration(amplitude_slider,frequency_slider,phase_slider)
    functions.generateFinalSignal(add_noise,file_signal_amplitude,noise_level)
    fig1,fig2,fig3,reconstructed_signal = functions.renderSampledSignal(sample_rate,is_normalized)
    
    st.plotly_chart(fig1,use_container_width="True")
    st.plotly_chart(fig2,use_container_width="True")
    st.plotly_chart(fig3,use_container_width="True")
    