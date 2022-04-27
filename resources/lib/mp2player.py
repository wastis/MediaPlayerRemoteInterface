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

import json

import dbussy as dbus
import ravel

from kodiif import KodiInfo

@ravel.interface \
	(
	ravel.INTERFACE.SERVER,
	name = "org.mpris.MediaPlayer2.Player"
	)
class MediaPlayer2Player :
	__slots__ = ("bus",)

	def __init__(self, bus) :
		self.bus = bus

	def send_prop_change(self, prop,  valtype, value):
		self.bus.send_signal \
		  (
			path = "/org/mpris/MediaPlayer2",
			interface = "org.freedesktop.DBus.Properties",
			name = "PropertiesChanged",
			args = ['org.mpris.MediaPlayer2.Player',
				{prop: (valtype, value)},
				[]]
		  )

	@ravel.method \
	  (
		name = "Previous",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Previous(self) :
		KodiInfo.SendKey("prev_track")

	@ravel.method \
	  (
		name = "Next",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Next(self) :
		KodiInfo.SendKey("next_track")

	@ravel.method \
	  (
		name = "Stop",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Stop(self) :
		KodiInfo.SendKey("stop")

	@ravel.method \
	  (
		name = "Play",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Play(self) :
		KodiInfo.SendKey("play_pause")

	@ravel.method \
	  (
		name = "Pause",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Pause(self) :
		KodiInfo.SendKey("pause")

	@ravel.method \
	  (
		name = "PlayPause",
		in_signature = "",
		out_signature = "",
	  )
	def handle_PlayPause(self) :
		KodiInfo.SendKey("play_pause")

	@ravel.method \
	  (
		name = "Seek",
		in_signature = [dbus.BasicType(dbus.TYPE.INT64)],
		out_signature = "",
		arg_keys = ["offset"],
	  )
	def handle_Seek(self, offset) :
		KodiInfo.PlaySeek(offset)

	@ravel.method \
	  (
		name = "OpenUri",
		in_signature = [dbus.BasicType(dbus.TYPE.STRING)],
		out_signature = "",
		arg_keys = ["uri"],
	  )
	def handle_OpenUri(self, uri) :
		KodiInfo.PlayOpen(uri)

	@ravel.method \
	  (
		name = "SetPosition",
		in_signature = \
			[
			dbus.BasicType(dbus.TYPE.OBJECT_PATH),
			dbus.BasicType(dbus.TYPE.INT64)
			],
		out_signature = "",
		arg_keys = ["track_id","position"],
	  )
	def handle_SetPosition(self, track_id, position) :
		if KodiInfo.PlayPosition(track_id, position) is not None:
			self.send_prop_change('Position','x', position)

	@ravel.propgetter \
	  (
		name = "Metadata",
		type = dbus.DictType\
			(
			dbus.BasicType(dbus.TYPE.STRING),dbus.VariantType()
			),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_Metadata(self) :
		return KodiInfo.GetMediaInfo()

	@ravel.propgetter \
	  (
		name = "PlaybackStatus",
		type = dbus.BasicType(dbus.TYPE.STRING),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_PlaybackStatus(self) :
		return KodiInfo.PlayStatus()

	@ravel.propgetter \
	  (
		name = "LoopStatus",
		type = dbus.BasicType(dbus.TYPE.STRING),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_LoopStatus(self) :
		return KodiInfo.PlayGetRepeat()

	@ravel.propsetter \
	  (
		name = "LoopStatus",
		type = dbus.BasicType(dbus.TYPE.STRING),
		value_keyword = "new_value",
	  )
	def set_LoopStatus(self, new_value) :
		KodiInfo.PlaySetRepeat(new_value)

	@ravel.propgetter \
	  (
		name = "Volume",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_Volume(self) :
		return KodiInfo.GetVolume()

	@ravel.propsetter \
	  (
		name = "Volume",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		value_keyword = "new_value",
	  )
	def set_Volume(self, new_value) :
		KodiInfo.SetVolume(new_value)

	@ravel.propgetter \
	  (
		name = "Shuffle",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_Shuffle(self) :
		return KodiInfo.PlayGetShuffle()

	@ravel.propsetter \
	  (
		name = "Shuffle",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		value_keyword = "new_value",
	  )
	def set_Shuffle(self, new_value) :
		KodiInfo.PlaySetShuffle(new_value)

	@ravel.propgetter \
	  (
		name = "Rate",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_Rate(self) :
		return 1.0

	@ravel.propsetter \
	  (
		name = "Rate",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		value_keyword = "new_value",
	  )
	def set_Rate(self, new_value) :
		pass

	@ravel.propgetter \
	  (
		name = "MinimumRate",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_MinimumRate(self) :
		return 0.032

	@ravel.propsetter \
	  (
		name = "MinimumRate",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		value_keyword = "new_value",
	  )
	def set_MinimumRate(self, new_value) :
		pass

	@ravel.propgetter \
	  (
		name = "MaximumRate",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_MaximumRate(self) :
		return 32.0

	@ravel.propsetter \
	  (
		name = "MaximumRate",
		type = dbus.BasicType(dbus.TYPE.DOUBLE),
		value_keyword = "new_value",
	  )
	def set_MaximumRate(self, new_value) :
		pass

	@ravel.propgetter \
	  (
		name = "CanControl",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanControl(self) :
		return True

	@ravel.propgetter \
	  (
		name = "CanPlay",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanPlay(self) :
		return True

	@ravel.propgetter \
	  (
		name = "CanPause",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanPause(self) :
		return True

	@ravel.propgetter \
	  (
		name = "CanSeek",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanSeek(self) :
		return True

	@ravel.propgetter \
	  (
		name = "CanGoNext",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanGoNext(self) :
		return True

	@ravel.propgetter \
	  (
		name = "CanGoPrevious",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanGoPrevious(self) :
		return True

	@ravel.propgetter \
	  (
		name = "Position",
		type = dbus.BasicType(dbus.TYPE.INT64),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_Position(self) :
		return KodiInfo.PlayGetPosition()

	#
	#	signals
	#

	@ravel.signal \
		(
		name = "Seeked",
		in_signature = \
			[
			dbus.BasicType(dbus.TYPE.INT64)
			],
		)
	def send_Seeked(self, pos) :
		self.bus.send_signal \
		  (
			path = "/org/mpris/MediaPlayer2",
			interface = "org.mpris.MediaPlayer2.Player",
			name = "Seeked",
			args = [pos]
		  )

	#
	#	handle messages from Kodi
	#

	def invalidate_seek(self, data = None):
		if data is None:
			self.send_Seeked(KodiInfo.PlayGetPosition())
		else:
			data = json.loads(data)

			item = KodiInfo.get_tag(data,["item","id"])
			if item is None:
				item = "{:x}".format(abs(hash(KodiInfo.get_tag(data,["item","title"]).strip())))

			playerid = 	KodiInfo.get_tag(data,["player","playerid"])

			if KodiInfo.is_playing_item(playerid, item):
				seekt = KodiInfo.get_tag(data,["player","time"])
				if seekt is None: return
				self.send_Seeked(KodiInfo.time_to_micro(seekt))

	def send_playback_status(self, status) :
		self.send_prop_change('PlaybackStatus','s', status)

	def send_metadata(self, data = None) :
		if data is None:
			data = KodiInfo.GetMediaInfo()
		self.send_prop_change('Metadata','a{sv}', data)

	@staticmethod
	def get_basic_item():
		return KodiInfo.GetBasicItem()
