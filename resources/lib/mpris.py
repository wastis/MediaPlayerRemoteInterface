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
from threading import Thread
import time

from dbussy import DBUS
from dbussy import DBusError

import ravel

from log import log
from handle import handle
from handle import infhandle

from mp2 import MediaPlayer2
from mp2player import MediaPlayer2Player

class Mpris():
	def __init__(self):
		self.loop = None
		self.th = None
		self.mp2 = None
		self.mp2p = None
		self.last_item = None
		self.owner = False

	async def poll_info(self):
		while True:
			try:
				item = self.mp2p.get_basic_item()
				if self.last_item != item:
					self.last_item = item
					self.send_metadata()
					self.invalidate_seek(None)
				await asyncio.sleep(1)
			except Exception as e:
				handle(e)

	def run(self):
		log("setup event loop")

		mpris_bus_name = "org.mpris.MediaPlayer2.kodi"

		try:
			bus = ravel.session_bus()
			if bus.request_name\
				(
				bus_name = mpris_bus_name,
				flags = DBUS.NAME_FLAG_DO_NOT_QUEUE
				) != DBUS.REQUEST_NAME_REPLY_PRIMARY_OWNER:
					return
		except DBusError as e:
			infhandle(e)
			log("cannot connect dbus")
			return

		self.loop = asyncio.new_event_loop()
		self.loop.create_task(self.poll_info())

		self.mp2 = MediaPlayer2(bus)
		self.mp2p = MediaPlayer2Player(bus)

		bus.attach_asyncio(self.loop)

		self.owner = True

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

		for task in \
			(lambda : asyncio.Task.all_tasks(bus.loop), lambda : asyncio.all_tasks(bus.loop)) \
				[hasattr(asyncio, "all_tasks")]():
			task.cancel()
			try :
				bus.loop.run_until_complete(task)
			except asyncio.CancelledError :
				pass

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
		if not self.owner:
			return
		log("on stop loop is running: {}".format(self.loop.is_running()))
		self.loop.call_soon_threadsafe(self.loop.stop)
		self.th.join()

	def start(self):
		self.th = Thread(target = self.run)
		self.th.start()
		time.sleep(0.1)
		return self.th.is_alive()

	def invalidate_seek(self, data):
		if self.mp2p is not None:
			self.mp2p.invalidate_seek(data)

	def send_playback_status(self,status):
		if self.mp2p is not None:
			self.mp2p.send_playback_status(status)

	def send_metadata(self):
		if self.mp2p is not None:
			self.mp2p.send_metadata()
