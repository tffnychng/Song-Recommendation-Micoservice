Spotify Genre Recommendation Microservice

This microservice returns Spotify song recommendations based on a requested genre.
Client programs make a request with a genre (ex: "rock", "pop", "lo-fi") and receives a list of tracks that match that genre.

Endpoint
--------

GET /recommendations

Returns a list of recommended tracks.

Query Parameter:
- genre (string): The desired music genre to generate with.


Example Request
---------------
```
import requests

response = requests.get(
    "http://localhost:5000/recommendations",
    params={"genre": "rock"}
)

print(response.json())
```

Example Response
----------------
```
{
  "genre": "rock",
  "tracks": [
    {
      "name": "Bohemian Rhapsody",
      "artist": "Queen",
      "image_url": "https://i.scdn.co/image/example",
      "spotify_url": "https://open.spotify.com/track/example"
    }
  ]
}
```

How to Receive/Use the Data
-------------------------------

The microservice returns in JSON format

```
import requests

def get_recommendations(genre):
    url = "http://localhost:5000/recommendations"
    response = requests.get(url, params={"genre": genre})
    data = response.json()

    for track in data["tracks"]:
        print(track["name"], "-", track["artist"])

    return data

get_recommendations("(genre)")
```

Communication Contract
----------------------

Client sends
GET /recommendations?genre=<genre> (like the above function call)

Microservice returns
```
{
  "genre": "<string>",
  "tracks": [
    {
      "name": "<string>",
      "artist": "<string>",
      "image_url": "<string or null>",
      "spotify_url": "<string>"
    }
  ]
}
```
