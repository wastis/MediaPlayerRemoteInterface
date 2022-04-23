#	This file is part of Media Player Remote Interface for Kodi.
#
#	Copyright (C) 2022 wastis
#
#	https://github.com/wastis/MediaPlayerRemoteInterface
#
#	Media Player Remote Interface is free software; you can redistribute it and/or modify
#	it under the terms of the GNU Lesser General Public License as published
#	by the Free Software Foundation; either version 3 of the License,
#	or (at your option) any later version.
#

import xbmc
from log import log
from mpris import Mpris

class MpriMonitor( xbmc.Monitor ):
	def __init__( self ):
		#strat process
		xbmc.Monitor.__init__( self )
		log("start monitor")

		self.mpr = Mpris()
		self.mpr.start()

		self.wait_abort()

		self.mpr.stop()
		log("end monitor")

	def wait_abort(self):
		while not self.abortRequested():
			if self.waitForAbort( 10 ):
				break

	def onNotification( self, sender, method, data ):
		log(f"{sender} {method} {data}")

		if method in ["Player.OnResume","Player.OnAVStart"]:
			self.mpr.send_playback_status("Playing")

		if method in ["Player.OnPause"]:
			self.mpr.send_playback_status("Paused")

		if method in ["Player.OnStop","System.OnQuit"]:
			self.mpr.send_playback_status("Stopped")

		if method == "Player.OnSeek":
			self.mpr.invalidate_seek(data)
