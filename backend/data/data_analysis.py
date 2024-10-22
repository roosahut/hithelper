import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import json

genres = [
  'Pop', 'Alternative', 'Country', 'Rap', 'Rock', 'Folk', 'R&B', 'Soul', 'Electronic', 'Dance'
]

def organize_lyrics_by_genre(data):
  """Organize the lyrics based on genre."""
  genre_lyrics = {}
  for genre in genres:
    genre_lyrics[genre] = ' '.join(data[data['Genre'].apply(lambda x: genre in eval(x))]['Lyrics'])
  return genre_lyrics

def get_most_common_words_json(data):
  """Create a json where genres have their lyric words ranked by how common the word is."""
  genre_word_values = {}

  for genre, lyrics in data.items():
    words = lyrics.split()
    word_counter = Counter(words)
    most_common = word_counter.most_common(50)
    genre_word_values[genre] = [{'text': word, 'value': count} for word, count in most_common]

  with open('most_common_words_by_genre.json', 'w') as common_words_file:
    json.dump(genre_word_values, common_words_file, indent=2)


def get_tfidf_values_json(data):
  """Create a json where genres have their lyric words ranked by TF/IDF vectorization."""
  tfidf_vectorizer = TfidfVectorizer(max_features=50)
  genre_tfidf_values = {}

  for genre, lyrics in data.items():
    tfidf_matrix = tfidf_vectorizer.fit_transform([lyrics])
    words = tfidf_vectorizer.get_feature_names()
    tfidf_scores = tfidf_matrix.toarray().flatten()

    word_list_for_genre = [{'text': word, 'value': score} for word, score in zip(words, tfidf_scores)]
    word_list_for_genre = sorted(word_list_for_genre, key=lambda x: x['value'], reverse=True)
    genre_tfidf_values[genre] = word_list_for_genre
  
  with open('tfidf_words_by_genre.json', 'w') as tfidf_file:
    json.dump(genre_tfidf_values, tfidf_file, indent=2)


data = pd.read_csv('backend/data/preprocessed_lyrics.csv')
genre_data = organize_lyrics_by_genre(data)

get_most_common_words_json(genre_data)
get_tfidf_values_json(genre_data)