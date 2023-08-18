import requests
import datetime
import re
import random
from functools import cached_property, lru_cache
from typing import Optional
from utils import list_all_results
from globals import DEFAULT_HEADERS, BASE_URL

class PodcastEpisode:
    PLAYBACK_RATE = 2.5

    def __init__(self, data):
        self.name = data["name"]
        self.id = data["id"]
        self.release_date = datetime.date.fromisoformat(data["release_date"])
        self.finished = data["resume_point"]['fully_played']
        self.duration_min = round(data["duration_ms"] / 1000 / 60, 2)

    def __repr__(self):
        return f"PodcastEpisode('id': {self.id}, 'name':{self.name}, 'release_date': {self.release_date}, \
'finished': {self.finished}, duration (minutes): {self.duration_min})"

    @property
    def uri(self):
        return f"spotify:episode:{self.id}"

    def age(self):
        return datetime.date.today() - self.release_date

    @property
    def adjusted_duration(self):
        return self.duration_min / self.PLAYBACK_RATE


class Track:
    def __init__(self, data):
        self.data = data
        self.name:str = data['name']
        self.id:str = data['id']
        self.uri:str = data['uri']
        self.duration_min:float = round(data['duration_ms'] / 1000 / 60, 2)
        self.type:str = data['type']

        if self.type == 'episode':
            try:
                self.release_date = datetime.date.fromisoformat(data["release_date"])
                self.age = datetime.date.today() - self.release_date
                self.finished:bool = self.data["resume_point"]['fully_played']
            except KeyError as e:
                print(f"Couldn't find all the data ({e}) for this Track (episode):")
                print(self.name)
        elif self.type == 'track':
            self.artists:str = [artist["name"] for artist in data['artists']]
            self.artist:str = self.artists[0]
            self.album:str = data['album']
        else:
            print("Idk what type this is.")

    def __repr__(self):
        return f"Track('name':{self.name})"

    @property
    def adjusted_duration(self) -> float:
        playback_rate = 2.5 if self.type == "episode" else 1
        return self.duration_min / playback_rate

class Playlist:
    def __init__(self, url):
        m = re.search(r'playlist\/(.{22})', url)
        if m:
            self.id = m.group(1)
        else:
            raise ValueError(f"Bad argument: {url}. Could not find uri in url.")

    @lru_cache(1)
    def list_all_tracks(self):
        endpoint = BASE_URL + f'/playlists/{self.id}/tracks'
        lst = list_all_results(endpoint=endpoint,
                               params={"limit":50},
                               headers=DEFAULT_HEADERS)
        lst = [item['track'] for item in lst]
        if lst is None or len(lst) == 0:
            raise ValueError(f"{self.id} is not a valid playlist. No tracks found.")
        return lst

    @cached_property
    def tracks(self) -> list[Track]:
        return [Track(track_data)
                for track_data in self.list_all_tracks()
                if track_data is not None]

    @cached_property
    def data(self):
        return requests.get(BASE_URL + f"/playlists/{self.id}",
                            headers=DEFAULT_HEADERS)\
                                .json()

    @property
    def name(self) -> str:
        return self.data['name']

    def random_tracks(self, number_of_tracks):
        return random.choices(self.tracks, k=number_of_tracks)

    def __hash__(self) -> int:
        return hash("Playlist " + self.id)

    def __str__(self):
        return f"Playlist({{'name':{self.name}, 'id':{self.id}}})"

    def __repr__(self):
        return str(self)

    @classmethod
    def from_id(cls, id):
        url = "/playlists/" + id
        return cls(url)


class TrackSource:
    def __init__(self, *subsources):
        self.subsources = subsources

    def random_subsource(self):
        return random.choice(self.subsources)

    def random_tracks_from_random_subsource(self, number_of_tracks):
        selected_subsource = self.select_random_subsource()

    @cached_property
    def tracks(self):
        ...


    def random_tracks(self, number_of_tracks):
        if number_of_tracks == 1:
            return [track]

        tracks = []
        for _ in range(number_of_tracks):
            subsource = self.random_subsource()
            track = subsource.random_tracks()
            tracks.append()
