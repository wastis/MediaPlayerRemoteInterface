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

	def invalidate_play(self):
		self.bus.prop_changed \
			(
			path = "/org/mpris/MediaPlayer2",
			interface = "org.mpris.MediaPlayer2.Player",
			propname = "PlaybackStatus",
			proptype = 's',
			propvalue = KodiInfo.PlayStatus()
			)

	def invalidate_info(self):
		self.bus.prop_changed \
			(
			path = "/org/mpris/MediaPlayer2",
			interface = "org.mpris.MediaPlayer2.Player",
			propname = "Metadata",
			proptype = 'a{sv}',
			propvalue = KodiInfo.GetMediaInfo()
			)

	@ravel.method \
	  (
		name = "Previous",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Previous(self) :
		KodiInfo.PlayGoTo("previous")
		self.invalidate_info()

	@ravel.method \
	  (
		name = "Next",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Next(self) :
		KodiInfo.PlayGoTo("next")
		self.invalidate_info()

	@ravel.method \
	  (
		name = "Stop",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Stop(self) :
		KodiInfo.PlayStop()
		self.invalidate_play()

	@ravel.method \
	  (
		name = "Play",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Play(self) :
		KodiInfo.PlayOnlyPlay()
		self.invalidate_play()

	@ravel.method \
	  (
		name = "Pause",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Pause(self) :
		KodiInfo.PlayOnlyPause()
		self.invalidate_play()

	@ravel.method \
	  (
		name = "PlayPause",
		in_signature = "",
		out_signature = "",
	  )
	def handle_PlayPause(self) :
		KodiInfo.PlayPause()
		self.invalidate_play()

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
		pass

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
	def get_CanCanGoNext(self) :
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

	def send_Seeked(self, pos) :
		self.bus.send_signal \
		  (
			path = "/org/mpris/MediaPlayer2",
			interface = "org.mpris.MediaPlayer2.Player",
			name = "Seeked",
			args = [pos]
		  )
