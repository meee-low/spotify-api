import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secret_keys import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import base64

_SCOPE = "user-library-read user-read-playback-position playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"

_auth_manager = None

_sp = None

AUTH_HEADERS = {}

def encode_64_bytes(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def refresh_auth_headers():
    global _auth_manager, _sp, AUTH_HEADERS
    _auth_manager = SpotifyOAuth(scope=_SCOPE,
                                 client_id=SPOTIPY_CLIENT_ID,
                                 client_secret=SPOTIPY_CLIENT_SECRET,
                                 redirect_uri=SPOTIPY_REDIRECT_URI)
    _sp = spotipy.Spotify(auth_manager=_auth_manager)

    AUTH_HEADERS = _sp._auth_headers()

refresh_auth_headers()