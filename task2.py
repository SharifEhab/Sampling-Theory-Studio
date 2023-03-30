# Import necessary libraries
import streamlit as st     # Streamlit library for creating interactive web apps
import pandas as pd        # Pandas library for data manipulation and analysis
import numpy as np         # NumPy library for numerical computing
import matplotlib.pyplot as plt  # Matplotlib library for data visualization
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk  # Matplotlib toolbar for interactive plots
import Sampling_Theory_Studio_functions

st.set_page_config(page_title="Sample", page_icon=":radio:", layout="wide")

# Initializing variables
signal_uploaded = False

# SESSION STATE INITIALIZATIONS
if 'add_sig_button_clicked' not in st.session_state:
   st.session_state['add_sig_button_clicked'] = 'not_clicked'

# HEADER SECTION
with st.container():
    st.title("Task 2 – Sampling-Theory Studio")

# Functions
def set_sigbutton():
    st.session_state.add_sig_button_clicked = 'clicked'

# SIDEBAR SECTION
with st.sidebar:
    st.header("Options")
    show_plot = st.checkbox("Show plot", True)
    plot_color = st.selectbox("Plot color", ["blue", "red", "green"])
    plot_style = st.selectbox("Plot style", ["-", "--", "-.", ":"])
    sample_freq_type = st.radio("Sampling frequency type", ["Actual frequency (Hz)", "Normalized frequency (fmax)"])
    if sample_freq_type == "Actual frequency (Hz)":
        sample_freq = st.slider("Sample Frequency (Hz)", 1, 100, 10)
    else:
        sample_freq = st.slider("Sample Frequency (fmax)", 1, 4, 2)
    st.write("ADD SIGNAL", text_align="right", font="bold")
        
    signal_frequency_slider_col, signal_amplitude_slider_col = st.sidebar.columns(2)
        
    signal_frequancy_slider = signal_frequency_slider_col.slider(
        'Frequency', 0.5, 20.0, 10.0, 0.1, format="%f")

    signal_amplitude_slider = signal_amplitude_slider_col.slider(
        'Amplitude', 0.1, 1.0, 0.1, 0.01, format="%f")

    signal_phase_slider = st.slider(
        'Phase', 0.0, 2.0, 0.0, 0.1, format="%fπ")

    add_signal_button = st.button("Add Signal", key="add_signal_button")
    if add_signal_button:
        
        Sampling_Theory_Studio_functions.addSignalToList(signal_amplitude_slider, signal_frequancy_slider, signal_phase_slider)
    selectbox_signals_list = []
    for signal in Sampling_Theory_Studio_functions.get_Total_signal_list():
        selectbox_signals_list.append(
            f"Amp: {signal.amplitude:n} / Freq: {signal.frequency:n} / Phase: {signal.phase :n} π")
    selected_signal = st.selectbox("Signals", selectbox_signals_list)
    selected_signal_split = str(selected_signal).split(" ")
    if len(selected_signal_split) != 1:
        amplitude_slider = float(selected_signal_split[1])
        frequency_slider = float(selected_signal_split[4])
        phase_slider = float(selected_signal_split[7])
    remove_button_col, clear_button_col = st.columns(2)
    with remove_button_col:
        remove_signal_button = st.button("Remove", key="remove_button", disabled=len(
            Sampling_Theory_Studio_functions.get_Total_signal_list()) <= 0)
        if remove_signal_button:
            Sampling_Theory_Studio_functions.removeSignalFromList(
                amplitude=amplitude_slider, frequency=frequency_slider, phase=phase_slider)
            st.experimental_rerun()

    with clear_button_col:
        clear_signals_button = st.button("Clear", key="clear_button", disabled=len(
            Sampling_Theory_Studio_functions.get_Total_signal_list()) <= 0)
        if clear_signals_button:
            Sampling_Theory_Studio_functions.Reintialize_values()
            Sampling_Theory_Studio_functions.SignalListClean()
            st.experimental_rerun()


# Main code
with st.container():
    st.write("---")
    uploaded_files = st.file_uploader("Upload a Signal", type=['csv'], accept_multiple_files=True)
    if uploaded_files:
        st.markdown("---")
        for uploaded_file in uploaded_files:
            data = pd.read_csv(uploaded_file)
            signal_uploaded = True
        label = st.text_input("Signal label")
        if label:
            dd_sig = st.button("Add Signal", on_click=set_sigbutton)
        if signal_uploaded and st.session_state.add_sig_button_clicked == 'clicked' and label:
            # extract Time and Amplitude columns
            time = data['Time']
            amplitude = data['Amplitude']

            # create a figure and axes objects
            fig, ax = plt.subplots()

            # plot the original data
            ax.plot(time, amplitude, color=plot_color, linestyle=plot_style)
            ax.set_xlabel('Time')
            ax.set_ylabel('Amplitude')
            st.write(label)
            ax.set_title('Original Signal')

           

            # sample the data
            if sample_freq_type == "Actual frequency (Hz)":
                sample_period = 1/sample_freq
            else:
                sample_period = 1/(sample_freq*2*time.max())
            sample_times = np.arange(time.min(), time.max(), sample_period)
            sample_amplitudes = np.interp(sample_times, time, amplitude)

            # plot the sampled data
            ax.scatter(sample_times, sample_amplitudes, color='black')

            # recover the original signal using Whittaker-Shannon interpolation formula
            interpolated_amplitudes = []
            for t in time:
                sinc_func = np.sinc((sample_times - t)/(sample_period))
                interpolated_amplitudes.append(np.sum(sample_amplitudes * sinc_func))
                        # plot the recovered signal
            if show_plot:
                st.write(5)
                ax.plot(time, interpolated_amplitudes, color='purple', linestyle='-.', label='Interpolated Signal')
                ax.legend()
                st.pyplot(fig)

            # create a dataframe with the original and recovered signals
            df = pd.DataFrame({'Time': time, 'Original Amplitude': amplitude, 'Recovered Amplitude': interpolated_amplitudes})


            # display the dataframes
            #st.write("Original and Recovered Signals Dataframe")
            #st.dataframe(df)
            fig2, ax2 = plt.subplots()
            ax2.plot(time, interpolated_amplitudes, color='purple', linestyle='-.', label='Reconstructed Signal')
            ax2.set_xlabel('Time')
            ax2.set_ylabel('Amplitude')
            ax2.set_title('Reconstructed Signal')
            ax2.legend() 
            if show_plot:
                st.pyplot(fig2)
                    # plot the difference between the original and reconstructed signals
            fig3, ax3 = plt.subplots()
            ax3.plot(time, amplitude - interpolated_amplitudes, color='orange', linestyle='--', label='Difference')
            ax3.set_xlabel('Time')
            ax3.set_ylabel('Amplitude')
            ax3.set_title('Difference between Original and Reconstructed Signals')
            ax3.legend()
            if show_plot:
                st.pyplot(fig3)


    else:
        st.write("Please upload a signal")
        # plot the reconstructed signal
   
# Disable warning message
st.set_option('deprecation.showPyplotGlobalUse', False)
