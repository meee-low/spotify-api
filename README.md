# Automatic Daily Playlist Creator for Spotify

Grabs tracks and podcast episodes from various sources and merges them in a single playlist. The goal is to approximate a radio station, with different themed blocks.

## How to use:

Since you need Spotify API access and private credentials like client ID, this is not very easy to run, so this repo is mostly for my personal use and showcasing. If you really want to run it, you will need to create your own `personal.py` and `secret_keys.py` files.

- `personal.py` has your playlist links and your user ID.
- `secret_keys.py` has your credentials (SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)

To run it daily, like I do, create a batch or bash script that runs the `daily.py` script every day.

All of these should be in the `/src/` folder.


## Dependencies:

This uses Spotipy only for authorization, since it was much easier to handle that with that package.

## Goals:

- Approximate a radio station, with different "blocks" of spoken discussions (podcasts) and music following certain themes (blocks of music from the same playlist).
- Not have to think about what I want to listen to in my commute while still having plenty of variety every day (single playlist, modified daily).
- Learn, experiment and showcase my skills with dealing with raw API calls and data.

In future, I may expand this to a full-blown GUI web-hosted application. That would be a much bigger project, so I would have to judge the public desire for it. Ideally Spotify would have a feature like this natively (they have something like this but it's terrible).
