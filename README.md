Spotify Genre Recommendation Microservice

This microservice returns Spotify song recommendations based on a requested genre and returns song information based on a requested song.
Client programs make a request with a type mood and a mood from a list of option (ex: "rock", "pop", "lo-fi") receives a list of tracks that match that genre. A program that makes a request with type song, a song name, an artist name receives information about the song.

How to Request Data
---------------
```
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#request a mood
socket.send_json({"type": "mood", "mood": "happy"})

#request a song
socket.send_json({"type": "song", "song": "Last Christmas", "artist": "Wham"})

```

Example Response
----------------
```
#request a mood

{
    'playlist': [
        {
            'name': 'No One Noticed',
            'artist': 'The Marías',
            'album': 'Submarine',
            'image': 'https://i.scdn.co/image/ab67616d0000b273b19ac38a59cddd80da3cedcb',
            'url': 'https://open.spotify.com/track/3siwsiaEoU4Kuuc9WKMUy5'
        }, ...
    ]
}

#request a song

{
    'playlist': [
        {
            'name': 'Stars',
            'artist': 'PinkPantheress',
            'album': 'Fancy That',
            'genres': ['bedroom pop'],
            'image': 'https://i.scdn.co/image/ab67616d0000b273dd4912edb4982f53a381b98e'
        }
    ]
}

```

How to Receive/Use the Data
-------------------------------

The microservice returns in JSON format through ZMQ

```
response = socket.recv_json()
for track in response["playlist"]:
    print(f"Song: {track['name']}\nArtist: {track['artist']}\nAlbum:{track['album']}\n")
```


UML Sequence Diagram
--------------------
![UML Diagram](https://github.com/user-attachments/assets/ec6bf509-1c9c-4b46-b260-ed91878fbee1)
