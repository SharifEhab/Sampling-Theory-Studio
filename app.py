import streamlit as st
import pandas as pd
import numpy as np
import Sampling_Theory_Studio_functions as functions

st.set_page_config(page_title="Sample", page_icon=":radio:", layout="wide")


# ___________ Elements styling ___________ #

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

##########################################################################


# Define a function to upload a CSV file and return its content as a Pandas DataFrame
def read_csv_file(file):
    if file is not None:
        data = pd.read_csv(file, usecols=["Time", "Amplitude"])
        return data
    else:
        return None

# SIDEBAR SECTION
with st.sidebar:
    st.title("Manage Signals")
    # Add Signal button
    file = st.file_uploader("Choose a CSV file", type="csv")
        # Sliders for signal properties
    st.write("Signal Properties")
    amplitude = st.sidebar.slider("Amplitude", 0, 5, 2)
    frequency = st.sidebar.slider("Frequency", 0.1, 20.0, 1.0)
    signal_phase_slider = st.sidebar.slider('Phase', 0.0, 2.0, 0.0, 0.1, format="%fπ")
    if st.button("Add Signal") and file is not None:
        signal = read_csv_file(file)
        # Add the signal to the list of signals
    
    # Remove Signal button
    selected_signal = st.selectbox("Select signal to remove", ["Signal 1", "Signal 2", "Signal 3"]) # TODO: Replace with actual signal list
    if st.button("Remove Signal") and selected_signal is not None:
        st.write("gbgfb")
        # Remove the selected signal from the list of signals


# HEADER SECTION
with st.container():
    st.title("Task 2 – Sampling-Theory Studio")