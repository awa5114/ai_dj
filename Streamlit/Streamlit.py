import streamlit as st

import numpy as np
import pandas as pd

st.markdown("""# DJ for dummies
## Paste the Youtube link of your song
XYZ test""")

df = pd.DataFrame({
          'first column': list(range(1, 11)),
          'second column': np.arange(10, 101, 10)
        })

# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 10, 3)

# and used in order to select the displayed lines
head_df = df.head(line_count)

head_df

# Procfile
#web: pip install . -U && ai_dj-run
#web: pip install . -U && Streamlit/Streamlit.py
#web: sh setup.sh && script/ai_dj-run