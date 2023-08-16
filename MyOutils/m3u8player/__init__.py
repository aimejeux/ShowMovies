# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts/script.module.main/lib/m3u8player/__init__.py
import m3u8
def readnet(url):
    try:
        import requests
        session = requests.Session()
        USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0'
        session.headers.update({'User-Agent': USER_AGENT})
        return session.get(url, verify=False).content
    except:
        #print 'download error'
        return
def getDirectM3U8Playlist(M3U8Url, checkExt = True, variantCheck = True, cookieParams = {}, checkContent = False, sortWithMaxBitrate = -1):
    if False:#checkExt and not M3U8Url.split('?', 1)[0].endswith('.m3u8'):
        return []
    else:
        retPlaylists = []
        data = readnet(M3U8Url)
        if data is None:
            return []
        if True:
            m3u8Obj = m3u8.inits(data, M3U8Url)
            #print 'm3u8Obj.is_variant',m3u8Obj.is_variant
            if m3u8Obj.is_variant:
                for playlist in m3u8Obj.playlists:
                    item = {}
                    if not variantCheck or playlist.absolute_uri.split('?')[-1].endswith('.m3u8'):
                        item['url'] = playlist.absolute_uri.replace('/\\\\','/').replace('\\','/').replace('tracks-v1a1/mono','index')
                        if 'dailymotion' in item['url'] and "#" in item['url']:
                           item['url']=item['url'].split("#")[0]
                        #print 'nnnnnnnnnnnnnnnnnnn1111111111111111111111111',item['url']
                    else:
                        item['url'] = playlist.absolute_uri.replace('/\\\\','/').replace('\\','/').replace('tracks-v1a1/mono','index')
                        if 'dailymotion' in item['url'] and "#" in item['url']:
                           item['url']=item['url'].split("#")[0]
                        #print 'nnnnnnnnnnnnnnnnnnn22222222222222222222222',item['url']
                    item['bitrate'] = playlist.stream_info.bandwidth
                    if None != playlist.stream_info.resolution:
                        item['with'] = playlist.stream_info.resolution[0]
                        item['heigth'] = playlist.stream_info.resolution[1]
                    else:
                        item['with'] = 0
                        item['heigth'] = 0
                    item['width'] = item['with']
                    item['height'] = item['heigth']
                    try:
                        tmpCodecs = playlist.stream_info.codecs.split(',')
                        codecs = []
                        for c in tmpCodecs[::-1]:
                            codecs.append(c.split('.')[0].strip())
                            item['codecs'] = ','.join(codecs)
                    except Exception:
                        item['codecs'] = None
                    item['name'] = 'bitrate: %s res: %dx%d %s' % (item['bitrate'],
                     item['width'],
                     item['height'],
                     item['codecs'])
                    retPlaylists.append(item)
                if sortWithMaxBitrate > -1:
                    def __getLinkQuality(itemLink):
                        try:
                            return int(itemLink['bitrate'])
                        except Exception:
                            return []
                    retPlaylists = CSelOneLink(retPlaylists, __getLinkQuality, sortWithMaxBitrate).getSortedLinks()
            else:
                if checkContent and 0 == len(m3u8Obj.segments):
                    return []
                item = {'name': 'm3u8',
                 'url': M3U8Url,
                 'codec': 'unknown',
                 'with': 0,
                 'heigth': 0,
                 'width': 0,
                 'height': 0,
                 'bitrate': 'unknown'}
                retPlaylists.append(item)
        else:
            pass
        return retPlaylists
        #return
def getm3u8playlist(url):
    list = []
    data = getDirectM3U8Playlist(url)
    if len(data) < 2:
        return list.append(('m3u8_0', url, 'img/play.png'))
    else:
        allres=[]
        for item in data:
            #print 'aime_jeux________________________________________________aime_jeux',item
            #print 'quality', item['heigth'], 'stream_url', item['url']
            #if item['heigth']==0 and name!="m3u8":
            if item['heigth']==0 and item['name']!="m3u8":
                continue
            if item['heigth'] in allres:
                continue
            allres.append(item['heigth'])
            list.append((item['heigth'], item['url'], 'img/play.png'))
        return list