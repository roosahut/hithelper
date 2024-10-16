import pandas as pd
import csv
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
file_name = 'backend/data/lyrics_to_top_100_songs.csv'

# IT IS ASSUMED THIS FILE IS RAN FROM PROJECT ROOT DIRECTORY (HITHELPER)

def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        rows = [row for row in reader]
    columns = rows[0]
    return pd.DataFrame(rows[1:], columns=columns)

def clean_lyrics(lyrics):
    '''This function removes languages and contributors from lyrics.'''
    if lyrics is not None:
        start = lyrics.find('Lyrics')
        if start != -1:
            cleaned_lyrics = lyrics[start:]
        else:
            cleaned_lyrics = lyrics
    else:
        cleaned_lyrics = ""
    return cleaned_lyrics

def stem_lyrics(data):
    '''This function stems the lyrics'''
    ps = PorterStemmer()
    data['Lyrics'] = data['Lyrics'].apply(lambda x: ' '.join([ps.stem(word) for word in str(x).split()]))

def remove_stop_words(data):
    '''This function removes stopwords from lyrics'''
    stop_words = set(stopwords.words('english'))
    with open('backend/data/stopwords.txt') as f:
        custom_stopwords = set(f.read().split('\n'))
    all_stopwords = stop_words.union(custom_stopwords)
    data['Lyrics'] = data['Lyrics'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in all_stopwords]))

def downcase_lyrics(data):
    '''This function downcases lyrics'''
    data['Lyrics'] = data['Lyrics'].str.lower()

def remove_punctuation(data):
    '''This function removes punctuation and numbers from lyrics'''
    data['Lyrics'] = data['Lyrics'].str.replace(r'[^\w\s]+', '', regex=True)
    data['Lyrics'] = data['Lyrics'].str.replace(r'\d+', '', regex=True)

data = load_data(file_name)

data = data.dropna(subset=['Lyrics'])

data['Lyrics'] = data['Lyrics'].apply(clean_lyrics)
downcase_lyrics(data)
remove_punctuation(data)
remove_stop_words(data)
stem_lyrics(data)

output_file = 'backend/data/preprocessed_lyrics.csv'
data.to_csv(output_file, index=False)
