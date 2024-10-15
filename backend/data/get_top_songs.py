import billboard
from pydantic import BaseModel
from typing import List
import csv

class Song(BaseModel):
    """
    A class used to represent a Song.

    Attributes:
        artist (str): The artist of the song.
        song_title (str): The title of the song.
        rank (int): The rank of the song on the chart.
    """
    artist: str
    song_title: str
    rank: int

def get_songs_from_billboard(): 
    """
    Fetches the top songs from the Billboard Hot 100 chart.

    This function retrieves the top songs from the Billboard Hot 100 chart
    and returns them as a list of Song objects.

    Returns:
        List[Song]: A list of Song objects representing the top songs on the Billboard Hot 100 chart.
    """
    top_songs = []
    chart = billboard.ChartData('hot-100', max_retries=10, timeout=25)
    for entry in chart:
        song = Song(
            artist=entry.artist,
            song_title=entry.title,
            rank=entry.rank
        )
        top_songs.append(song)
    return top_songs

def write_top_songs_to_file(top_songs: List[Song]):
    """
    Writes the top songs to a CSV file.

    This function takes a list of Song objects and writes their details to a CSV file.

    Args:
        top_songs (List[Song]): A list of Song objects to be written to the file.
        filename (str): The name of the file to write the songs to. Defaults to "./backend/data/top_100_songs.csv".
    """
    with open("./backend/data/top_100_songs.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "Title", "Artist"]) 
        for song in top_songs:
            writer.writerow([song.rank, song.song_title, song.artist])            
