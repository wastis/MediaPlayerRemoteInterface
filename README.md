# Multimedia Player Remote Interfaces for Kodi

MPRIS implementation for Kodi. 

This service addon enables the control of Kodi from desktop controls and keyboard multimedia keys.  

Such controls can be the system tray Media Controls in Ubuntu, for example.

#### Testing

For simple command line control of Kodi playerctl can be used. 

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