import os
import zmq
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

# mood to genre mapping
# anything in [] is a genre from spotify
mood_genres = {
    # moods
    "happy": ["pop", "dance pop", "indie pop"],
    "sad": ["sad", "acoustic", "piano"],
    "chill": ["lo-fi", "chillhop", "ambient"],
    "romantic": ["r-n-b", "soul", "soft rock"],
    "angry": ["metal", "punk", "hardcore"],
    "motivated": ["edm", "big room", "house"],
    "nostalgic": ["80s", "90s", "classic rock"],
    "melancholy": ["indie", "dream pop", "bedroom pop"],
    "peaceful": ["ambient", "new age", "instrumental"],
    "energetic": ["edm", "workout", "dance pop"],

    # activities
    "workout": ["edm", "house", "trap"],
    "study": ["lo-fi", "ambient", "instrumental"],
    "sleep": ["sleep", "ambient", "white noise"],
    "driving": ["rock", "alt rock", "indie rock"],
    "party": ["pop", "club", "house"],
    "cooking": ["indie pop", "folk", "chill"],
    "cleaning": ["dance pop", "pop", "house"],
    "running": ["edm", "drum and bass", "techno"],
    "studying": ["lo-fi", "ambient", "piano"],
    "gaming": ["synthwave", "dark synth", "trap beats"]
}

# Playlist generator
def get_by_mood(mood):
    genres = mood_genres.get(mood, ["pop"])
    unique_tracks = {}

    for genre in genres:
        query = f'genre:"{genre}"'
        print(f"Querying Spotify with: {query}")

        results = sp.search(q=query, type="track", limit=10)

        for item in results["tracks"]["items"]:
            key = f"{item['name'].lower()}_{item['artists'][0]['name'].lower()}"

            if key not in unique_tracks:
                unique_tracks[key] = {
                    "name": item["name"],
                    "artist": item["artists"][0]["name"],
                    "album": item["album"]["name"],
                    "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                    "url": item["external_urls"]["spotify"]
                }

    return list(unique_tracks.values())

def get_song_info(song, artist):
    results = sp.search(q=f'track:"{song}" artist:"{artist}"', type="track", limit=1)
    
    if not results["tracks"]["items"]:
            return {"error": "Song not found in Spotify database"}
    
    item = results["tracks"]["items"][0]
    artist_info = sp.artist(item["artists"][0]["id"])

    return [{
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "genres": artist_info["genres"],
            "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
        }]      

# ZeroMQ setup
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Service running..")

while True:
    message = socket.recv_json()
    type = message.get("type")

    if type == "mood":
        mood = message.get("mood")
        print(f"Received request for mood: {mood}")
        playlist = get_by_mood(mood)
    elif type == "song":
        song = message.get("song")
        artist = message.get("artist")
        print(f"Received request for song: {song} by {artist}")
        playlist = get_song_info(song,artist)

    socket.send_json({"playlist": playlist})
