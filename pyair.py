'''
Python script to play internet radio station in VLC
'''
import vlc
import sys

def play():
  url = 'http://icecast.vrtcdn.be/stubru-high.mp3'
  p = vlc.MediaPlayer(url)
  p.play()

  try:
    while True:
      print("Playing radio station, press Ctlr + C to stop")
      input("")
  except KeyboardInterrupt:
      print("Stopped playing radio station")
      p.stop()
      sys.exit()

play()
