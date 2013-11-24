import wikipedia
import requests
import re
import os, os.path
import codecs

def logo_guess(team):
    p = wikipedia.page(wikipedia.search("%s" % team)[0])
    print "found page %s" % p.title

    filepage = re.findall('<table[^\n].*?infobox.*?a href="(/wiki/File.*?)"', p.html(), re.S)[0]
    imagepage = "http://en.wikipedia.org" + filepage
    r = requests.get(imagepage)
    fullimage = re.findall(r'fullImageLink.*?href="(.*?)".*?/div', r.content, re.S)[0]

    image = 'http:' + fullimage
    return (p.title, image)

def download(image_url, image_name):
    cmd = "wget %s -O '%s' > /dev/null 2>&1 &" % (image_url, image_name)
    print cmd
    os.system(cmd)

def get(team):
    #if we already have it, bail
    for extension in ["svg", "png"]:
        filename = "wikicrests/%s.%s" % (team, extension)
        if os.path.isfile(filename):
            print "found %s already" % team
            return

    page, logo_file = logo_guess(team)

    extension = re.split('\.', logo_file)[-1]
    filename = "wikicrests/%s.%s" % (team, extension)
    download(logo_file, filename)

if __name__=="__main__":
    import csv

    with codecs.open("wikinames.txt", 'r', 'utf8') as f:
        for team in f:
            team = team.strip()
            print team
            get(team)
