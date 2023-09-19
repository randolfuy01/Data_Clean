import numpy as np
import pandas as pd
import string
import re

lyrical_data = pd.read_csv('drake_data.csv')

# Dropping the items as we do not need them within the dataframe
to_drop = ['album', 'lyrics_url', 'track_views']
lyrical_data.drop(labels=to_drop, axis=1, inplace=True)
# Now we have dataframe consisting of just names of the songs and the lyrics

# Cleaning the lyrics data
lyrical_data['lyrics'] = lyrical_data['lyrics'].str.lower()
lyrical_data['lyrics'] = lyrical_data['lyrics'].str.replace(r'[^a-zA-Z0-9 ]', ' ', regex=True)
lyrical_data.to_csv('drake_data_cleaned.csv')

