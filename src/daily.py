import make_podcast_releases
import merge_track_sources
import logging

log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(filename='mylogs.log', level='DEBUG', format=log_format)

def main():
    try:
        make_podcast_releases.update_playlist()
    except Exception as e:
        logging.error(e)

    try:
        merge_track_sources.update_playlist()
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()