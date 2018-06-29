""" Python script to play internet radio station and podcasts in VLC """

import datetime
import time
import sys
import ssl
from urllib.request import urlopen

from bs4 import BeautifulSoup
import vlc


def get_latest_episode_url(rssFeed,id):
    """ Function to scrap the latest podcast url and title"""
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(rssFeed, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup('enclosure')

    for tag in tags:  # Look at the parts of a tag
        title = soup.find('title')
        if(not(id == "11")):
            title = title.find_next('title')
        break
    print("\nEpisode Title :",title.find_next('title').contents[0])

    return(tag.get('url',None))


def play(id):
    """ Function to handle media player selection """
    is_found = False                   # Is stream ID found?
    radio = False
    with open('links.txt') as f:
        for line in f:
            if line.startswith(id):
                link = line.split()
                url = link[2]
                is_found = True
                if(link[3]=='r'):
                  radio = True
                else:
                  url = get_latest_episode_url(url,id)
    if(not(is_found)):
        print('\nInvalid Input!\n')
        main_menu()

    if(not(radio)):
        choice = input("\nDo you want to play this episode?(y/n): ")
        if(choice =='n'):
            main_menu()
    player = vlc.MediaPlayer(url)
    player.play()

    try:
        while True:
            print("\nPlaying Audio Track...\n")
            print("~~Media Player Controls~~")
            print("p - Pause")
            print("c - Continue")
            print("s - Seek")
            print("i - Information about current track")
            print("m - Go back to main menu")
            print("w - Write track information to file")
            print("q - Quit")
            i = input("\nEnter Choice: ")
            if i=='p':
                player.pause()
                print("Current runtime percentage : ",round(player.get_position()*100,2),"%")
            elif i=='c':
                player.play()
            elif i == 'm':
                player.stop()
                main_menu()
            elif i == 's':
                player.pause()
                s = input("Enter seek position between 0 and 1.0 : ")
                player.set_position(float(s))
                player.play()
            elif i == 'i':
                media = player.get_media()
                print("\nCurrent playing track: "+str(media.get_meta(12)))
            elif i =='w':
                with open("Tracks_list.txt","a+") as f:
                    ts = time.time()
                    f.write(media.get_meta(12))
                    f.write(" | ")
                    f.write(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
                    f.write("\n")
                f.close()
                print("\nWritten current running track information to file..")
            elif i =='q':
                print("\nStopped playing the streaming station\n")
                player.stop()
                sys.exit()
    except KeyboardInterrupt:
        print("Stopped playing the streaming station")
        player.stop()
        sys.exit()


def main_menu():
    """ Display the main menu """
    try:
        print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~ Welcome to your media streaming ~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Enter the number to play the stream')
        print('\nCategory: Music + Radio -\n')
        print('01.  Studio Brussel')
        print('02.  BBC Radio One')
        print('03.  Tunein Today\'s Hits')
        print('04.  All Songs Considered Podcast')
        print('05.  Desert Island Discs')
        print('06.  Song Exploder')
        print('07.  De Afrekening')
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
    main_menu()
