'''
Python script to play internet radio station and podcasts in VLC
'''

import sys
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import vlc

'''
Function to scrap the latest podcast url and title
'''
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

'''
Function to handle media player selection
'''
def play(id):
  radio = False
  if id =='1':
      url = 'http://icecast.vrtcdn.be/stubru-high.mp3'
      radio = True
  elif id == '2':
      url = 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_q'
      radio = True
  elif id =='3':
      url = 'http://rfcmedia.streamguys1.com/MusicPulse.mp3'
      radio = True
  elif id == '4':
      rssFeed = 'https://www.npr.org/rss/podcast.php?id=510019'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='10':
      rssFeed = 'http://feeds.gimletmedia.com/hearreplyall'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='11':
      rssFeed = 'http://feeds.feedburner.com/freakonomicsradio'
      url = getLatestEpisodeUrl(rssFeed,"F")
  elif id =='12':
      rssFeed = 'https://www.npr.org/rss/podcast.php?id=510289'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='15':
      rssFeed = 'https://feeds.megaphone.fm/revisionisthistory'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='5':
      rssFeed = 'https://podcasts.files.bbci.co.uk/b006qnmr.rss'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='13':
      rssFeed = 'http://feeds.wnyc.org/radiolab'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='14':
      rssFeed = 'http://feeds.99percentinvisible.org/99percentinvisible'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='16':
      rssFeed = 'https://www.npr.org/rss/podcast.php?id=510318'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id =='6':
      rssFeed = 'http://feed.songexploder.net/SongExploder'
      url = getLatestEpisodeUrl(rssFeed,"R")
  elif id == '17':
      rssFeed = 'https://www.npr.org/rss/podcast.php?id=500005'
      url = getLatestEpisodeUrl(rssFeed,"R")

  else:
    print('\nInvalid Input!\n')
    mainMenu()
  if(not(radio)):
    choice = input("\nDo you want to play this episode?(y/n): ")
    if(choice =='n'):
      mainMenu()
  p = vlc.MediaPlayer(url)
  p.play()

  try:
    while True:
      print("\nPlaying Audio Track, press p to pause, c to continue, m to go back to main menu and Ctlr + C to stop\n")
      i = input("")
      if i=='p':
        p.pause()
      elif i=='c':
        p.play()
      elif i == 'm':
        p.stop()
        mainMenu()
  except KeyboardInterrupt:
      print("Stopped playing the streaming station")
      p.stop()
      sys.exit()
    
'''
Display the main menu
'''
def mainMenu():
    try:
        print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~ Welcome to your media streaming ~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Enter the number to play the stream')
        print('\nCategory: Music -\n')
        print('1.  Studio Brussel')
        print('2.  BBC Radio One')
        print('3.  Tunein Today\'s Hits')
        print('4.  All Songs Considered Podcast')
        print('5.  Desert Island Discs')
        print('6.  Song Exploder')
        print('\nCategory: Curosity -\n')
        print('10.  Reply All')
        print('11.  Freakonomics')
        print('12.  Planet Money')
        print('13.  Radiolab')
        print('14.  99 Percent Invisible')
        print('15.  Revisionist History Podcast')
        print('\nCategory: Current Affairs - \n')
        print('16.  Up First')
        print('17.  NPR News Now')
        id = input("\nPress number to play : ")
        play(id)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    mainMenu()
