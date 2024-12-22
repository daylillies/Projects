# Import libraries
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import re  # Import regex module for validating sequence

# Page Title
image = Image.open('C:\\Users\\kathe\\Desktop\\Coding Projects\\DNA Count\\dna-logo.jpg')
st.image(image, use_container_width=True)

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
""")

# Default sequence input
example_sequence = "GAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGGATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGCTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

# Store sequence in session state if not already present
if 'sequence' not in st.session_state:
    st.session_state.sequence = example_sequence

# Input Text Box
st.header('Enter DNA sequence')

# Button to restore the example sequence
if st.button('Example Sequence'):
    st.session_state.sequence = example_sequence  # Resets to the example sequence

# Text area for input sequence, default value comes from session state
sequence = st.text_area("Sequence input", st.session_state.sequence, height=250)

# Button to clear the sequence
if st.button('Clear Sequence'):
    st.session_state.sequence = ''  # Clears the sequence input when button is clicked

# Button to submit the sequence for processing
if st.button('Submit Sequence'):
    # Update session state with the new sequence input from the text area
    st.session_state.sequence = sequence.strip()  # Remove leading/trailing whitespace

    # Ensure the sequence is not empty
    if not st.session_state.sequence:
        st.warning("Please enter a DNA sequence.")
        st.stop()

    # Check if the sequence contains only valid characters (A, T, G, C)
    if not re.match("^[ATGC]*$", st.session_state.sequence):
        st.error("Error: DNA sequence contains invalid characters. Only A, T, G, and C are allowed.")
        st.stop()

    st.write("""
    ***
    """)

    # Prints the input DNA sequence
    st.header('DNA Sequence')
    st.write(st.session_state.sequence)

    # DNA nucleotide count
    st.header('DNA Nucleotide Count')

    # 1. Print dictionary
    st.subheader('1. Print dictionary')
    def DNA_nucleotide_count(seq):
        # Check if the sequence is empty
        if not seq:
            st.warning("No sequence to process.")
            return {}
        
        d = dict([
            ('A', seq.count('A')),
            ('T', seq.count('T')),
            ('G', seq.count('G')),
            ('C', seq.count('C'))
        ])
        return d

    # Get nucleotide count
    X = DNA_nucleotide_count(st.session_state.sequence)

    # Check if X is empty or not
    if X:
        st.write(X)  # This should display the dictionary
    else:
        st.warning("No valid nucleotide counts.")

    ### 2. Print text
    st.subheader('2. Print text')
    st.write('There are  ' + str(X['A']) + ' adenine (A)')
    st.write('There are  ' + str(X['T']) + ' thymine (T)')
    st.write('There are  ' + str(X['G']) + ' guanine (G)')
    st.write('There are  ' + str(X['C']) + ' cytosine (C)')

    ### 3. Display DataFrame
    st.subheader('3. Display DataFrame')
    df = pd.DataFrame.from_dict(X, orient='index')
    df = df.rename({0: 'count'}, axis='columns')
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'nucleotide'})
    st.write(df)

    ### 4. Display Bar Chart using Altair
    st.subheader('4. Display Bar chart')
    p = alt.Chart(df).mark_bar().encode(
        x='nucleotide',
        y='count'
    )
    p = p.properties(
        width=alt.Step(80)  # controls width of bar.
    )
    st.write(p)
