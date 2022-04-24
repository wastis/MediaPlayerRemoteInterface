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

import asyncio

from dbussy import DBUS
import ravel

from threading import Thread
from log import log
from handle import handle

from mp2 import MediaPlayer2
from mp2player import MediaPlayer2Player

class Mpris():
	def __init__(self):
		self.loop = None
		self.th = None
		self.mp2p = None
		self.last_item = None

	async def poll_info(self):
		while True:
			item = self.mp2p.get_basic_item()
			if self.last_item != item:
				self.last_item = item
				self.send_metadata()
				self.invalidate_seek(None)
			await asyncio.sleep(1)

	def run(self):
		log("setup event loop")

		mpris_bus_name = "org.mpris.MediaPlayer2.kodi"

		self.loop = asyncio.new_event_loop()
		self.loop.create_task(self.poll_info())

		bus = ravel.session_bus()

		self.mp2 = MediaPlayer2(bus)
		self.mp2p = MediaPlayer2Player(bus)

		bus.attach_asyncio(self.loop)
		bus.request_name\
			(
			bus_name = mpris_bus_name,
			flags = DBUS.NAME_FLAG_ALLOW_REPLACEMENT\
				| DBUS.NAME_FLAG_REPLACE_EXISTING
			)
		bus.register \
		  (
			path = "/",
			fallback = True,
			interface = self.mp2
		  )

		bus.register \
		  (
			path = "/",
			fallback = True,
			interface = self.mp2p
		  )

		log("start event loop")
		while True:
			try:
				self.loop.run_forever()
			except Exception as e:
				handle(e)
			else:
				break

		bus.unregister \
		  (
			path = "/",
			interface = self.mp2
		  )
		bus.unregister \
		  (
			path = "/",
			interface = self.mp2p
		  )

		bus.release_name(bus_name = mpris_bus_name)
		log("loop is running: {}".format(self.loop.is_running()))

	def stop(self):
		log("on stop loop is running: {}".format(self.loop.is_running()))
		self.loop.call_soon_threadsafe(self.loop.stop)
		self.th.join()

	def start(self):
		self.th = Thread(target = self.run)
		self.th.start()

	def invalidate_seek(self, data):
		if self.mp2p is not None:
			self.mp2p.invalidate_seek(data)

	def send_playback_status(self,status):
		if self.mp2p is not None:
			self.mp2p.send_playback_status(status)

	def send_metadata(self):
		if self.mp2p is not None:
			self.mp2p.send_metadata()
