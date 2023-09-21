import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import psycopg2
import sqlalchemy as db
from nltk.tokenize.treebank import TreebankWordDetokenizer

lyrical_data = pd.read_csv('drake_data.csv')

# Dropping the items as we do not need them within the dataframe

to_drop = ['album', 'lyrics_url', 'track_views']

lyrical_data.drop(labels=to_drop, axis=1, inplace=True)

# Now we have dataframe consisting of just names of the songs and the lyrics

lyrical_data['lyrics'] = lyrical_data['lyrics'].str.lower()

lyrical_data['lyrics'] = lyrical_data['lyrics'].str.replace(r'[^a-zA-Z0-9 ]', ' ', regex = True)

lyrical_data['lyrics'] = lyrical_data['lyrics'].replace(r'\s+', ' ', regex=True)

# lyrical_data['lyrics'].to_csv('before_tokenization.csv')

stop = stopwords.words('english')

lyrical_data['lyrics'] = lyrical_data.apply( lambda x : nltk.word_tokenize(str(x['lyrics'])), axis = 1)

lyrical_data['lyrics'] = lyrical_data['lyrics'].apply(lambda x: [item for item in x if item not in stop])

# lyrical_data['lyrics'].to_csv('after_tokenization.csv')

detokenizer = TreebankWordDetokenizer() 

lyrical_data['lyrics'] = lyrical_data['lyrics'].apply( lambda x : detokenizer.detokenize(x))

lyrical_data = lyrical_data.astype({'lyrics_title' : str, 'lyrics' : str})

print(lyrical_data['lyrics'])
# Importing into PostgreSQL
import sqlalchemy as db
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

alchemy_engine = db.create_engine('postgresql+psycopg2://postgres:dataEngineer01@localhost:5432/DrakeData')

db_connection = alchemy_engine.connect()

conn = psycopg2.connect(database = 'DrakeData', host = 'localhost', user = 'postgres', password = 'dataEngineer01')

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = conn.cursor()

cursor.execute('SELECT current_database()')

print(cursor.fetchone())

cursor.execute('DROP TABLE IF EXISTS Lyrics_Table')

cursor.execute(''' 
    CREATE TABLE Lyrics_Table (
               Lyrics_Title Text,
               Lyrics Text
    )
''')

lyrical_data.to_sql('lyrical_data', con= alchemy_engine, if_exists='replace', index=False)

conn.autocommit = True

command = ('''SELECT * from lyrical_data''')

cursor.execute(command)

print(cursor.fetchone())

conn.close()