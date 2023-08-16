import urllib
def get_M3u(url):
    from .m3u8player import getm3u8playlist
    mlist = getm3u8playlist(url)
    return mlist
