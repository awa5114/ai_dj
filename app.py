from numpy.lib.shape_base import _make_along_axis_idx
import streamlit as st

#import from gcp bucket
import youtube_dl
import audioread
import numpy as np
import pandas as pd

mix = '/Users/willemsickinghe/Downloads/Lonely (Original Mix).mp3'

st.markdown("""# DJ for dummies
## Paste the Youtube link of your song
XYZ test""")

df = pd.DataFrame({
          'first column': list(range(1, 11)),
          'second column': np.arange(10, 101, 10)
        })

#line_count = st.slider('Select a line count', 1, 10, 3)
# and used in order to select the displayed lines
#head_df = df.head(line_count)

#head_df

import streamlit as st

st.audio(mix, format='audio/wav', start_time=0)

audio_file = open(mix, 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/wav')

# Procfile
#web: pip install . -U && ai_dj-run
#web: pip install . -U && Streamlit/Streamlit.py
#web: sh setup.sh && script/ai_dj-run