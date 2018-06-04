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
      print("Playing Audio Track, press Ctlr + C to stop")
      input("")
  except KeyboardInterrupt:
      print("Stopping audio track")
      p.stop()
      sys.exit()

play()
