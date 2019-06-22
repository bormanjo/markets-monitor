import feedparser

rss_feeds = {
    "WSJ Markets": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "WSJ World News": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "WSJ US Business": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml"
}


def get_rss_feed(feed_key, top_n=None):
    """
    Returns a RSS feed in markdown format
    :param feed_key: A key in the rss_feeds dictionary identifying the feed
    :return: A multiline string in markdown format
    """

    # Parse the rss feed
    feed = feedparser.parse(rss_feeds[feed_key])

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
