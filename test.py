import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Generating playlist")
socket.send_json({"type": "mood","mood": "happy"})
response = socket.recv_json()
for i, track in enumerate(response["playlist"], start=1):
    print(f"{i}. {track['name']} by {track['artist']} ({track['album']})")
    if track["image"]:
      print(f"   Album Artwork: {track['image']}")
    print(f"   Spotify URL: {track['url']}\n")


print("Looking up song")
socket.send_json({"type": "song","song": "Stars", "artist" : "PinkPantheress"})
response = socket.recv_json()
track = response["playlist"][0]
print(f"{track['name']} by {track['artist']} ({track['album']})")
genre_list = ','.join(track['genres'])
print(f"Genre: {genre_list}")
if track["image"]:
  print(f"Album Artwork: {track['image']}")