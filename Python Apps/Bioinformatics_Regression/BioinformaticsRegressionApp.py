# Import libraries
import numpy as np
import pandas as pd
import streamlit as st
import pickle
from rdkit import Chem
from rdkit.Chem import Descriptors

# Custom function: Simple Aromatic Proportion calculation from SMILES
def AromaticProportion(molecule):
    aromatic_atoms = sum(1 for i in range(molecule.GetNumAtoms()) if molecule.GetAtomWithIdx(i).GetIsAromatic())
    heavy_atoms = Descriptors.HeavyAtomCount(molecule)
    return aromatic_atoms / heavy_atoms if heavy_atoms > 0 else 0  # Avoid division by zero

def generate_descriptors(smiles_list):
    descriptors_list = []
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:  # Ensure molecule is valid
            descriptors = [
                Descriptors.MolLogP(mol),
                Descriptors.MolWt(mol),
                Descriptors.NumRotatableBonds(mol),
                AromaticProportion(mol)
            ]
            descriptors_list.append(descriptors)
    
    # Convert to DataFrame for easy manipulation and visualization
    column_names = ["MolLogP", "MolWt", "NumRotatableBonds", "AromaticProportion"]
    return pd.DataFrame(descriptors_list, columns=column_names)

# Page Title
st.write("""
# Molecular Solubility Prediction Web App

This app predicts the **Solubility (LogS)** values of molecules

Data obtained from the John S. Delaney. [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.
***
""")

# Input molecules (Side Panel)
st.sidebar.header('User Input Features')

# Read SMILES input
SMILES_input = "NCCCC\nCCC\nCN"
SMILES = st.sidebar.text_area("SMILES input", SMILES_input)
SMILES_list = SMILES.split('\n')

# Example SMILES molecules
st.sidebar.write("""
**Example SMILE Molecules:**

- Methane: `C`
- Ethane: `CC`
- Ethene (ethylene): `C=C`
- Ethyne (acetylene): `C#C`
- Dimethyl ether: `COC`
- Ethanol: `CCO`
- Acetaldehyde: `CC=O`
- Hydrogen Cyanide: `C#N`
- Cyanide anion: `[C-]#N`
""")

# Ensure there's at least one valid SMILES string
if not SMILES_list or not SMILES_list[0]:
    SMILES_list = ["C"]  # Adding a default molecule if input is empty

# Display input SMILES
st.header('Input SMILES')
st.write(SMILES_list)

# Compute molecular descriptors
st.header('Computed Molecular Descriptors')
descriptors_df = generate_descriptors(SMILES_list)
st.write(descriptors_df)

# Load pre-trained model
model_path = 'C:\\Users\\kathe\\Desktop\\Coding Projects\\Bioinformatics_Regression\\BioinformaticsModel.pkl'
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Predict solubility (LogS) values
st.header('Predicted LogS values')
predictions = model.predict(descriptors_df)
st.write(predictions)
