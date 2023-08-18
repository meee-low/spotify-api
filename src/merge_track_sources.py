import random
from collections import Counter, defaultdict
from utils import replace_playlist
from globals import BASE_URL, DEFAULT_HEADERS
from classes import Playlist, Track
import personal
import logging

log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(filename='mylogs.log', level='DEBUG', format=log_format)

def indices(lst:list, element) -> list[int]:
    """Returns the indices in which the `element` appears in the list `lst`."""
    return [idx for idx, value in enumerate(lst) if value == element]

def values_at_indices(lst:list, indices:list[int]) -> list:
    """Returns the values of the list `lst` at the given `indices`."""
    return [value for idx, value in enumerate(lst) if idx in indices]

def blocks_of_duration(tracks:list[Track],
                       block_duration:int|float,
                       number_of_blocks:int) -> list[list[Track]]:
    random.shuffle(tracks)
    blocks:list[list[Track]] = []
    for i in range(number_of_blocks):
        current_block_duration = 0
        current_block = []
        for track in tracks:
            if track.adjusted_duration + current_block_duration <= block_duration[i]:
                current_block.append(track)
                current_block_duration += track.adjusted_duration
                tracks.remove(track)
        blocks.append(current_block)
    return blocks

def build_blocks(playlists:list[Playlist],
                 block_durations:list[int|float] | int|float) -> list[Track]:
    if type(block_durations) == int or type(block_durations) == float:
        # optionally, allow for all blocks to have the same size
        block_durations = [block_durations] * len(playlists)

    # Prepare:
    # Create blocks for the same playlists in bulk, to reduce repeated tracks.
    counter = Counter(playlists)
    prepared_blocks:dict[Playlist, list[list[Track]]] = {}
    for pl, number_of_occurences in counter.items():
        # If the same playlist (`key`) appears n (`value`) times in `playlists`,
        # create n blocks of the proper duration.
        pl_indices = indices(playlists, pl)
        durations = values_at_indices(block_durations, pl_indices)
        blocks = blocks_of_duration(pl.tracks, durations, number_of_occurences)
        prepared_blocks[pl] = blocks

    # Make the blocks
    result_tracks:list[Track] = [] # returned
    block_tracker = defaultdict(int) # stores the index of the current block for the playlists
    for pl in playlists:
        block_idx = block_tracker[pl]
        current_block = prepared_blocks[pl][block_idx]
        result_tracks.extend(current_block)
        block_tracker[pl] += 1
    return result_tracks

def tracks_to_uris(tracks:list[Track]) -> list[str]:
    """Converts the tracks to their URIs.

    Args:
        tracks (list[Track]): The list of tracks.

    Returns:
        list[str]: The list of URIs.
    """
    return [track.uri for track in tracks]

def pick_from_playlists(lists_of_playlists:list[list[Playlist]], index_order:list[int]) -> list[Playlist]:
    """Randomly picks playlists out of the lists of playlists. \
        Sorts the dealt results according to the order in `index_order`

    Args:
        lists_of_playlists (list[list[Playlist]]): A list of collections of playlists.
        index_order (list[int]): The order of the playlists.

    Returns:
        list[Playlist]: The picked playlists in order.
    """
    result = []
    for idx in index_order:
        collection = lists_of_playlists[idx]
        playlist_picked = random.choice(collection) # pick a random playlist
        result.append(playlist_picked)

    return result

def load_playlists_from_string_of_urls(string:str) -> list[Playlist]:
    urls = string.split("\n")
    playlists = [Playlist(url) for url in urls]
    return playlists


COLLECTIONS = {"familiar playlists": load_playlists_from_string_of_urls(personal.FAMILIAR_PLAYLISTS_URLS),
               "discover playlists": load_playlists_from_string_of_urls(personal.DISCOVER_PLAYLISTS_URLS),
               "new_podcasts_playlists": load_playlists_from_string_of_urls("https://open.spotify.com/playlist/4R2PqHSETBHXu1ysr5JEXQ?si=4f4a74da231a4004")}

def list_playlists():
    for c in COLLECTIONS:
        print(c)
        for pl in COLLECTIONS[c]:
            print(pl)
        print("\n")

def update_playlist():
    pl_lst = [COLLECTIONS["new_podcasts_playlists"], COLLECTIONS["familiar playlists"], COLLECTIONS["discover playlists"]]

    pls = pick_from_playlists(pl_lst, [0, 1, 0, 2, 0, 1, 0, 2, 0])

    print([pl.name for pl in pls])

    logging.info([pl.name for pl in pls])

    new_tracklist = build_blocks(pls, 50)

    print([t.name for t in new_tracklist])
    new_tracklist_uris = tracks_to_uris(new_tracklist)
    pl_id = "7qh7F3MKhr6PS5Kgxaqzn9" # real playlist
    # pl_id = "3RY7uWRMNCNQXmeQ2NCT11" # test
    replace_playlist(pl_id, new_tracklist_uris, {"limit":50}, DEFAULT_HEADERS)

def main():
    update_playlist()

if __name__ == "__main__":
    main()