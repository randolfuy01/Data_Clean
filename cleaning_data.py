import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
lyrical_data = pd.read_csv('drake_data.csv')

# Dropping the items as we do not need them within the dataframe
to_drop = ['album', 'lyrics_url', 'track_views']
lyrical_data.drop(labels=to_drop, axis=1, inplace=True)
# Now we have dataframe consisting of just names of the songs and the lyrics
lyrical_data['lyrics'] = lyrical_data['lyrics'].str.lower()

lyrical_data['lyrics'] = lyrical_data['lyrics'].str.replace(r'[^a-zA-Z0-9 ]', ' ', regex = True)

lyrical_data['lyrics'] = lyrical_data['lyrics'].replace(r'\s+', ' ', regex=True)

lyrical_data['lyrics'].to_csv('before_tokenization.csv')

stop = stopwords.words('english')

lyrical_data['lyrics'] = lyrical_data.apply( lambda x : nltk.word_tokenize(str(x['lyrics'])), axis = 1)

lyrical_data['lyrics'] = lyrical_data['lyrics'].apply(lambda x: [item for item in x if item not in stop])

lyrical_data['lyrics'].to_csv('after_tokenization.csv')