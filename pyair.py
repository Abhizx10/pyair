'''
Python script to play internet radio station and podcasts in VLC
'''
import vlc
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

def getLatestEpisodeUrl(rssFeed,podcast):
  # Ignore SSL certificate errors
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE

  html = urlopen(rssFeed, context=ctx).read()
  soup = BeautifulSoup(html, "html.parser")

  tags = soup('enclosure')

  for tag in tags:
    # Look at the parts of a tag
    title = soup.find('title')
    if podcast == "R":
      title = title.find_next('title')
    print("\nEpisode Title :",title.find_next('title').contents[0])

    return(tag.get('url',None))

def play(id):
  if id =='1':
      url = 'http://icecast.vrtcdn.be/stubru-high.mp3'
  elif id =='2':
      rssFeed = 'http://feeds.gimletmedia.com/hearreplyall'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='3':
      rssFeed = 'http://feeds.feedburner.com/freakonomicsradio'
      url = getLatestEpisodeUrl(rssFeed,"F")
  elif id =='4':
    rssFeed = 'https://www.npr.org/rss/podcast.php?id=510289'
    url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='5':
    rssFeed = 'https://feeds.megaphone.fm/revisionisthistory'
    url = getLatestEpisodeUrl(rssFeed,"R")
  else:
    print('Invalid Input\n')
    sys.exit()

  p = vlc.MediaPlayer(url)
  p.play()

  try:
    while True:
      print("\nPlaying Audio Track,press p to pause, c to continue, Ctlr + C to stop\n")
      i = input("")
      if i=='p':
        p.pause()
      elif i=='c':
        p.play()
  except KeyboardInterrupt:
      print("Stopped playing the streaming station")
      p.stop()
      sys.exit()

if __name__ == '__main__':
    print('~~Welcome to your media streaming~~~')
    print('Enter the number to play the stream')
    print('1. Studio Brussel')
    print('2. Play the latest Reply All Podcast')
    print('3. Play the latest Freakonomics Podcast')
    print('4. Play the latest Planet Money Podcast')
    print('5. Play the latest Revisionist History Podcast')
    id = input("Press number to play : ")
    play(id)
