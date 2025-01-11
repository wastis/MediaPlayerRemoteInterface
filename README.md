# Multimedia Player Remote Interfaces for Kodi

This Kodi addon provides a MPRIS interface for better integration of Kodi into Linux desktops.

[Version 1.0.7](https://github.com/wastis/LinuxAddonRepo)

It forwards the desktop- and keyboard multimedia control events to Kodi and provides meta data back to the desktop for display in system tray controls.

![Cinnamon Sound Tray Icon](resources/media/kodi-cinnamon-applet-player-small.jpg)

## Installation

This addon is included into the [Linux Addon Repository](https://github.com/wastis/LinuxAddonRepo). It is recommended to use the repository for the installation of the addon. This will ease version upgrades. 

## Flatpak
If Kodi had been installed from flatpak, additional access rights have to be granted to the the Kodi sandbox for the addon to work correctly.

	flatpak override --user --own-name=org.mpris.MediaPlayer2.kodi tv.kodi.Kodi

## Testing via command line

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
