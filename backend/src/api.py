
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Genre(BaseModel):
    genre: str

class Lyrics(BaseModel):
    text: str

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/api/genre')
def get_genre_wordcloud(genre: Genre):
    pass

@app.post('/api/lyric_percentage')
def get_lyric_similarity_percentage(lyrics: Lyrics):
    pass


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)