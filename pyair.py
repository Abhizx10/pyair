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
def getLatestEpisodeUrl(rssFeed,id):
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
    if(not(id == "11")):
      title = title.find_next('title')
    print("\nEpisode Title :",title.find_next('title').contents[0])

    return(tag.get('url',None))

'''
Function to handle media player selection
'''
def play(id):
  isFound = False
  radio = False
  with open('links.txt') as f:
      for line in f:
          if line.startswith(id):
              link = line.split()
              url = link[2]
              #print("#Debug url :"+url)
              isFound = True
              if(link[3]=='r'):
                radio = True
              else:
                url = getLatestEpisodeUrl(url,id)
                #print("#Debug  podcast link  :"+url)
  if(not(isFound)):
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
        print('01.  Studio Brussel')
        print('02.  BBC Radio One')
        print('03.  Tunein Today\'s Hits')
        print('04.  All Songs Considered Podcast')
        print('05.  Desert Island Discs')
        print('06.  Song Exploder')
        print('\nCategory: Curosity -\n')
        print('10.  Reply All')
        print('11.  Freakonomics')
        print('12.  Planet Money')
        print('13.  Radiolab')
        print('14.  99 Percent Invisible')
        print('15.  Revisionist History')
        print('\nCategory: Current Affairs - \n')
        print('16.  Up First')
        print('17.  NPR News Now')
        id = input("\nPress number to play : ")
        play(id)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    mainMenu()
