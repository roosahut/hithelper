import pandas as pd
from collections import Counter
import json

genres = [
  'Pop', 'Alternative', 'Country', 'Rap', 'Rock', 'Folk', 'R&B', 'Soul', 'Electronic', 'Dance'
]

def most_common_words(data):
  genre_words = {genre: Counter() for genre in genres}

  for genre in genres:
    genre_data = data[data['Genre'].apply(lambda x: genre in eval(x))]
    lyrics_for_genre = ' '.join(genre_data['Lyrics'])
    lyrics_for_genre = lyrics_for_genre.split()
    genre_words[genre] = Counter(lyrics_for_genre)

  most_common_words = {}
  for genre, counter in genre_words.items():
    most_common_words_for_genre = [{"text": word, "value": count} for word, count in counter.most_common(50)]
    most_common_words[genre] = most_common_words_for_genre

  json_final = json.dumps(most_common_words)
  print(json_final)

  with open('most_common_words_per_genre.json', 'w') as f:
    f.write(json_final)


def compute_tf_idf_vector(data):
  pass

data = pd.read_csv('backend/data/preprocessed_lyrics.csv')
most_common_words(data)