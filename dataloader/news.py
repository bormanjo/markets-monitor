import feedparser
import datetime
import pathlib
import json
import os

rss_feeds = {
    "WSJ Markets": {
        "link": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "updated": None
    },
    "WSJ World News": {
        "link": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
        "updated": None
    },
    "WSJ US Business": {
        "link": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
        "updated": None
    }
}

CACHE_DIR = pathlib.Path("./dataloader/cache")

if not CACHE_DIR.exists():
    os.mkdir(CACHE_DIR)


def update_cache(feed_key):
    """Updates the RSS cache"""

    # Define cache file
    cache_file = CACHE_DIR / (feed_key + ".json")

    # Update
    feed = feedparser.parse(rss_feeds[feed_key]['link'])
    rss_feeds[feed_key]['updated'] = datetime.datetime.today()

    # Cache data
    with open(cache_file, "w") as file:
        json.dump(feed.entries, file)

    return feed.entries


def get_cache(feed_key):
    """Gets the cached data of the corresponding feed"""

    cache_file = CACHE_DIR / (feed_key + ".json")

    with open(cache_file, "r") as file:
        entries = json.load(file)

    return entries


def get_rss_feed(feed_key):
    """
    Returns a parsed feed object
    :param feed_key: A key in the rss_feeds dictionary identifying the feed
    :return:
    """

    if rss_feeds[feed_key]['updated'] is None:
        # Update Cache
        entries = update_cache(feed_key)
    elif (datetime.datetime.today() - rss_feeds[feed_key]['updated']).seconds > (60 * 5):
        # Update Cache
        entries = update_cache(feed_key)
    else:
        # Read Cache
        entries = get_cache(feed_key)

    return entries


def get_rss_feed_markdown(feed_key, top_n=None):
    """
    Returns a RSS feed in markdown format
    :param feed_key: A key in the rss_feeds dictionary identifying the feed
    :return: A multiline string in markdown format
    """

    # Parse the rss feed
    feed = get_rss_feed(feed_key)

    # Create the object output
    feed_str = ""
    hr = "\n---\n"      # Horizontal rule

    if top_n is None:
        top_n = len(feed.entries)
    elif not (isinstance(top_n, int) and top_n > 0):
        raise ValueError(f"'top_n' must be an integer value greater than 0. Received: '{top_n}'")

    feed_str += hr

    # Loop through entries
    for entry in feed.entries[:top_n]:
        feed_str += f"{entry['summary']} ([Link]({entry['link']}))\n" + hr

    return feed_str
