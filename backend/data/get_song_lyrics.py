import os
from dotenv import load_dotenv
import lyricsgenius
import csv
from typing import List


load_dotenv()
genius_token = os.getenv('GENIUS_TOKEN')

class Song:
    """
        Initializes a Song object.

        Args:
            rank (int): The rank of the song.
            title (str): The title of the song.
            artist (str): The artist of the song.
            lyrics (str, optional): The lyrics of the song. Defaults to an empty string.
            genre (list, optional): The genre(s) of the song. Defaults to an empty list.
    """
    def __init__(self, rank: int, title: str, artist: str, lyrics: str = "", genre: list=[]):
        self.rank = rank
        self.title = title
        self.artist = artist
        self.lyrics = lyrics
        self.genre = genre


def read_songs_from_csv() -> List[Song]:
    """
    Reads songs from a CSV file and returns a list of Song objects.

    Returns:
        List[Song]: A list of Song objects.
    """
    songs = []
    with open("./backend/data/top_100_songs.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            song = Song(rank=int(row['Rank']), title=row['Title'], artist=row['Artist'])
            songs.append(song)
    return songs

def get_song_lyrics_from_genius(songs: List[Song]):
    """
    Fetches lyrics and genres for a list of songs from the Genius API.

    Args:
        songs (List[Song]): A list of Song objects.
    """
    genius = lyricsgenius.Genius(genius_token)
    for song in songs:
        song_data = genius.search_song(song.title, song.artist)
        if song_data:
            song.lyrics = song_data.lyrics
            song.genre = get_song_genre(song_data.id)
        else:
            print("song data not found for song ", song.title, song.artist)

def get_song_genre(song_id: int) -> str:
    public_api = lyricsgenius.PublicAPI()
    song = public_api.song(song_id)['song']
    genres = [tag['name'] for tag in song['tags']]
    print(genres)
    return genres if genres else "Unknown"


def write_songs_to_csv(songs: List[Song]):
    with open("./backend/data/lyrics_to_top_100_songs.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "Title", "Artist", "Genre", "Lyrics"])
        for song in songs:
            writer.writerow([song.rank, song.title, song.artist, song.genre, song.lyrics])

top_songs = read_songs_from_csv()
get_song_lyrics_from_genius(top_songs)
write_songs_to_csv(top_songs)