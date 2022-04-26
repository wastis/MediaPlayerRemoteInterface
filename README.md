# Multimedia Player Remote Interfaces for Kodi

This Kodi addon provides a MPRIS interface for better integration of Kodi into Linux desktops.

It forwards the desktop- and keyboard multimedia control events to Kodi and provides meta data back to the desktop for display in system tray controls.

![Cinnamon Sound Tray Icon](/resources/media/kodi-cinnamon-applet-player-small.jpg)


**Testing via command line**

For simple command line control of Kodi the tool playerctl can be used. 

The following example requires Kodi up and running and the Multimedia Player Remote Interface addon installed and enabled in Kodi. 

**Install playerctl**

	sudo apt install playerctl	

**Open a media file**

	playerctl -p kodi open /path/to/file.mp3

**Open a playlist**

	playerctl -p kodi open /path/to/file.m3u

**Next**

	playerctl -p kodi next

**Check if Multimedia Player Remote Interface is up and running**

	playerctl -l

kodi needs to be in the output

**Seek 10s backwards**

	playerctl -p kodi position 10-

*2022 wastis*