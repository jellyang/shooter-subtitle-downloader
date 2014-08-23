#-------------------------------------------------------------------------------
# Name		: shooter subtitle downloader
# Purpose	: download chinese subtitle from shooter website
# Created	: Kevin
# Copyright	: (c) xiangshuai.github.com
#-------------------------------------------------------------------------------
import os
import hashlib
import sys
import math
try:
	import urllib.request, urllib.parse
	pyVer = 3
except ImportError:
	import urllib2
	pyVer = 2
	
def get_hash(name):
    L = list()
    with open(name, 'rb') as f:
        e = 4096
        f.seek(0, os.SEEK_END)
        size = f.tell()
        
        # first 4k
        start = min(size, 4096)
        end = min(start+e, size)
        f.seek(int(start))
        data = f.read(int(end - start))
        digest = hashlib.md5(data).hexdigest()
        L.append(digest)
        
        # second 4k
        start = math.floor(size/3 * 2)
        end = min(start+e, size)
        f.seek(int(start))
        data = f.read(int(end - start))
        digest = hashlib.md5(data).hexdigest()
        L.append(digest)
        
        # third 4k
        start = math.floor(size/3)
        end = min(start+e, size)
        f.seek(int(start))
        data = f.read(int(end - start))
        digest = hashlib.md5(data).hexdigest()
        L.append(digest)
        
        # fourth 4k
        start = max(0, size - 8192)
        end = min(start+e, size)
        f.seek(int(start))
        data = f.read(int(end - start))
        digest = hashlib.md5(data).hexdigest()
        L.append(digest)
        
    return L

def sub_downloader(path):

    hash = get_hash(path)
    name = path.split('\\')[-1]
    replace = [".avi",".mp4",".mkv",".mpg",".mpeg",".mov",".rm",".vob",".wmv",".flv",".3gp"]
    for content in replace:
        path = path.replace(content,"")
    if not os.path.exists(path+".srt"):

        headers = { 'User-Agent' : 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)' }
		
        # step 1. find subtitle list
        filehash = hash[0]+'%3B'+hash[1]+'%3B'+hash[2]+'%3B'+hash[3]
        url = 'http://www.shooter.cn/api/subapi.php?filehash='+filehash+'&format=json&pathinfo='+name
        if pyVer == 3:
            req = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(req).read()
        else:
            req = urllib2.Request(url, '', headers)
            response = urllib2.urlopen(req).read()
        
        # step 2. get first subtitle from subtitle list
        url = eval(response)[0]['Files'][0]['Link'].replace('\u0026', '&')
		
        if pyVer == 3:
            req = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(req).read()
        else:
            req = urllib2.Request(url, '', headers)
            response = urllib2.urlopen(req).read()
        with open (path+".srt","wb") as subtitle:
            subtitle.write(response)

path = sys.argv[1]
#path = 'E:\\ipv6\\Divergent.2014.RETAIL.1080p.WEB-DL.H264.AC3-EVO\\Divergent.2014.RETAIL.1080p.WEB-DL.H264.AC3-EVO.mkv'
sub_downloader(path)
