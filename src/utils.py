import json
import requests
import base64
from globals import BASE_URL

def jprint(data):
    """Prints json data in an indented format."""
    try:
        data = data.json()
    except AttributeError:
        pass
    print(json.dumps(data, indent=2))

def feed_chunk(lst, chunk_size=50):
    """Generator that yields chunks of `lst` of size `chunk_size`."""
    i = 0
    while i < len(lst):
        yield lst[i:i+chunk_size]
        i += chunk_size

def get_all_results(endpoint, params, headers):
    """Generator that yields pages from a get request."""
    r = requests.get(endpoint, params=params, headers=headers)
    yield r.json()['items']
    endpoint = r.json()['next']
    while endpoint:
        r = requests.get(endpoint, headers=headers)
        yield r.json()['items']
        endpoint = r.json()['next']

def list_all_results(endpoint, params, headers):
    """Returns a list concatenating the items from all pages."""
    result = []
    for page in get_all_results(endpoint, params, headers):
        result.extend(page)
    return result

def clear_playlist(playlist_id, params, headers):
    """Removes all tracks from the playlist."""
    endpoint = BASE_URL + r"/playlists/{}/tracks"
    tracks_in_playlist = list_all_results(endpoint.format(playlist_id),
                                          params=params,
                                          headers=headers)

    tracks_in_playlist_uri = [{"uri": t['track']['uri']}
                              for t in tracks_in_playlist
                              if t is not None and t['track'] is not None]

    #TODO: some tracks get listed as None. Above is a work-around.

    for c in feed_chunk(tracks_in_playlist_uri, chunk_size=100):
        r = requests.delete(endpoint.format(playlist_id),
                            json={"tracks": c},
                            headers=headers)

def add_to_playlist(playlist_id, list_of_uris, headers):
    """Add tracks to playlist."""
    CHUNK_SIZE = 50
    endpoint = BASE_URL + r"/playlists/{}/tracks"
    for i, c in enumerate(feed_chunk(list_of_uris, chunk_size=CHUNK_SIZE)):
      position = i * CHUNK_SIZE
      r = requests.post(endpoint.format(playlist_id),
                        json={"uris": c, "position": position},
                        headers=headers)

def replace_playlist(playlist_id, list_of_uris, params, headers):
    """Removes all current tracks from the playlist and add the new tracks."""
    print("Clearing playlist.")
    clear_playlist(playlist_id, params, headers)
    print("Playlist cleared.")
    print("Adding new tracks to playlist.")
    add_to_playlist(playlist_id, list_of_uris, headers=headers)
    print("Tracks added to playlist.")
