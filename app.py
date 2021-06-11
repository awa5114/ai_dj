import streamlit as st
import numpy as np
import pandas as pd
from ai_dj import params

#Don't forget to change the name.
mix = f'{params.TEMP_MIXED_FOLDER}/64_kygo_combined2.wav'

<<<<<<< HEAD
#line_count = st.slider('Select a line count', 1, 10, 3)
# and used in order to select the displayed lines
#head_df = df.head(line_count)
#head_df
=======
st.markdown("""# DJ for dummies""")
  
st.markdown("""## Paste the Youtube link of your song below""")
yt_link = st.text_input('', '' )

if st.button('Create'):
    print('button clicked!')
    st.write('I was clicked 🎉')
    st.write('Further clicks are not visible but are executed')
else:
    st.write('I was not clicked 😞')
>>>>>>> main

st.audio(mix, format='audio/wav', start_time=0)

audio_file = open(mix, 'rb')
audio_bytes = audio_file.read()
#st.audio(audio_bytes, format='audio/wav')

st.write('Enjoy the newly created song by ai_dj')
st.write('Thank you, come again')