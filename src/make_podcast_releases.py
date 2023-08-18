"""Makes the playlists of new, unplayed podcast releases.
"""
import requests
import datetime
from globals import BASE_URL, DEFAULT_HEADERS, PODCAST_NEW_RELEASES_PLAYLIST_ID
from utils import list_all_results, replace_playlist
from classes import Track
import logging

log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(filename='mylogs.log', level='DEBUG', format=log_format)


def load_podcasts():
    # LIST ALL SUBSCRIBED PODCASTS
    print("Loading my podcasts.")
    my_podcasts = list_all_results(BASE_URL + "/me/shows",
                                   params = {"limit": 50,},
                                   headers=DEFAULT_HEADERS)
    print("Podcasts loaded.")

    podcast_ids = [p['show']['id'] for p in my_podcasts]

    return podcast_ids

def find_most_recent_episodes(podcasts_ids, depth=2):
    # LIST THE MOST RECENT EPISODES FROM EACH OF THOSE PODCASTS
    print("Listing  podcast episodes.")
    most_recent_episodes = []
    for pod_id in podcasts_ids:
        pod_episodes_resp = requests.get(BASE_URL + f"/shows/{pod_id}/episodes",
                                         params={"limit":2},
                                         headers=DEFAULT_HEADERS)
        for ep in pod_episodes_resp.json()['items']:
            pod_ep = Track(ep)
            most_recent_episodes.append(pod_ep)
    print("Podcast episodes listed.")

    return most_recent_episodes

def filter_episodes(most_recent_episodes):
    # FILTER
    print("Filtering episodes.")
    # episodes_to_add = most_recent_episodes
    # # don't add episodes already listened
    # episodes_to_add = [ep for ep in episodes_to_add
    #                    if not ep.finished]
    # # don't add episodes that are too old
    # episodes_to_add = [ep for ep in episodes_to_add
    #                    if ep.age <= datetime.timedelta(days=16)]

    episodes_to_add = []
    for ep in most_recent_episodes:
        try:
            if ep.finished:
                # don't add episodes already listened
                continue
        except AttributeError:
            print(f"Couldn't determine if track was finished. No action done. This episode may be mistakenly added to the playlist. Episode: {ep}")
            pass
        try:
            if ep.age > datetime.timedelta(days=16):
                # don't add episodes that are too old
                continue
        except AttributeError:
            print(f"Couldn't find age for an episode. No action done. This episode may be mistakenly added to the playlist. Episode: {ep}")
            pass
        episodes_to_add.append(ep)

    print("Episodes filtered.")

    return episodes_to_add


def push_playlist(episodes_to_add):
    # ADD TO PLAYLIST
    episodes_to_add_sorted = sorted(episodes_to_add,
                                    key=lambda ep: ep.age)

    # First, clear the playlist:
    new_episodes_uris = [ep.uri for ep in episodes_to_add_sorted]

    replace_playlist(PODCAST_NEW_RELEASES_PLAYLIST_ID,
                     new_episodes_uris,
                     params={"limit": 50},
                     headers=DEFAULT_HEADERS)
    print("New episodes added.")
    print("Finished updating new podcast episodes playlist.")

def update_playlist():
    podcasts = load_podcasts()
    recent_episodes = find_most_recent_episodes(podcasts)
    filtered_episodes = filter_episodes(recent_episodes)
    push_playlist(filtered_episodes)
    episode_titles = (str(ep) for ep in filtered_episodes)
    logging.info(", ".join(episode_titles))

def main():
    update_playlist()

if __name__ == "__main__":
    main()