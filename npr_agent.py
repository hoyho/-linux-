from xml.etree.ElementTree import parse, Element
import http.client
import xml.etree.ElementTree as ET
import requests
import re
import os
from threading import Timer
import time



new_media_base_url = "http://here2say.com:8001/media/"
NEW_FEED_URL = "http://here2say.com:8001/ted.xml"

#to keep itunes namespace,or it will lost when save to file
ET.register_namespace('<prefix>','https://www.npr.org/rss/')
ET.register_namespace('itunes','http://www.itunes.com/dtds/podcast-1.0.dtd')
ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}


#you may need to change here to debug
media_save_path = '/usr/share/nginx/html/media/'
#debug media_save_path ='/Users/xsky/Documents/workspace/project/'
xml_save_path = '/usr/share/nginx/html/'



def download_source_rss():
    """
    download source rss and return file name
    """
    conn = http.client.HTTPSConnection("www.npr.org")
    headers = {
        'cache-control': "no-cache",
        'postman-token': "6bab6f91-5945-40b4-47fb-6484309001db"
        }

    conn.request("GET", "/rss/podcast.php?id=510298", headers=headers)
    #conn.request("GET", "/ted.xml", headers=headers)
    res = conn.getresponse()
    data = res.read()
    rss = data.decode("utf-8")

    fName = 'source.xml'
    with open(fName, 'wt',encoding='utf8') as f:
        f.write(rss)
    return fName

def parse_head(xml_file='source.xml'):
    """
    change xml npr header info as my info
    """
    doc  = parse(xml_file)
    #root = doc.getroot()
    #print(root)
    title = doc.find('channel/title')
    title.text = "My TED Radio Hour"

    feed_url = doc.find('channel/itunes:new-feed-url',ns)
    if feed_url:
        feed_url.text = NEW_FEED_URL
    doc.write(xml_file, xml_declaration=True)



def parse_media_item(xml_file='source.xml'):
    """
    download media to local path (to server as media file by nginx)
    """
    doc  = parse(xml_file)
    #root = doc.getroot()
    count = 0
    for item in doc.iterfind('channel/item'):
        count += 1
        if count > 20:
            print("only cache for 20 items")
            break
        print("begin handle channel item \n")
        if item == None:
            print ("can not get channel item")
            return

        resource = item.find("enclosure")
        if resource == None:
            print("item don't have attribute enclosure,next \n")
            continue

        print(resource.attrib["url"] + '\n')

        pattern = re.compile(r'([\w|\d|\-]+\.mp3)')   #match file name
        rs = pattern.findall(resource.attrib["url"])

        if len(rs)<1:
            print("can not match any file name \n")
            continue
        file_name = rs[0]

        if not os.path.isdir(media_save_path):
            os.mkdir(media_save_path)

        full_path = media_save_path + file_name

        file_exist =False
        if os.path.isfile(full_path):
            print (full_path + " exist \n")
            file_exist= True

        print("new media file will be save as {0} \n".format(full_path))

        try:
            if not file_exist:
                print('try opening media url ...')
                r = requests.get(resource.attrib["url"])
                with open(full_path, 'wb') as f:
                    f.write(r.content)
        except Exception as ex:
            print("parse media item error \n")
            print(str(ex))
            continue

        resource.attrib["url"] = new_media_base_url + file_name
        new_xml_path = xml_save_path + 'ted.xml'
        doc.write(new_xml_path, xml_declaration=True)

def task():
    print (time.strftime("%Y-%m-%d %H:%M"))
    print("start task \n")
    f = download_source_rss()
    parse_head(f)
    parse_media_item(f)


if __name__ == "__main__":
    while True:
        task()
        time.sleep(60*60) #1 hours