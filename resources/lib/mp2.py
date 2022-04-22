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

@ravel.interface(ravel.INTERFACE.SERVER, name = "org.mpris.MediaPlayer2")
class MediaPlayer2 :
	__slots__ = ("bus",)

	def __init__(self, bus) :
		self.bus = bus

	@ravel.method \
	  (
		name = "Quit",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Quit(self) :
		pass

	@ravel.method \
	  (
		name = "Raise",
		in_signature = "",
		out_signature = "",
	  )
	def handle_Raise(self) :
		pass

	@ravel.propgetter \
	  (
		name = "Identity",
		type = dbus.BasicType(dbus.TYPE.STRING),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_Identity(self) :
		return "Kodi Media Player"

	@ravel.propgetter \
	  (
		name = "DesktopEntry",
		type = dbus.BasicType(dbus.TYPE.STRING),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_DesktopEntry(self) :
		return "kodi"

	@ravel.propgetter \
	  (
		name = "SupportedMimeTypes",
		type = dbus.ArrayType(dbus.BasicType(dbus.TYPE.STRING)),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_SupportedMimeTypes(self) :
		return [""]

	@ravel.propgetter \
	  (
		name = "SupportedUriSchemes",
		type = dbus.ArrayType(dbus.BasicType(dbus.TYPE.STRING)),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_SupportedUriSchemes(self) :
		return [""]

	@ravel.propgetter \
	  (
		name = "HasTrackList",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_HasTrackList(self) :
		return False

	@ravel.propgetter \
	  (
		name = "CanQuit",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanQuit(self) :
		return False

	@ravel.propgetter \
	  (
		name = "CanSetFullscreen",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanSetFullscreen(self) :
		return False

	@ravel.propgetter \
	  (
		name = "Fullscreen",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_Fullscreen(self) :
		return False

	@ravel.propgetter \
	  (
		name = "CanRaise",
		type = dbus.BasicType(dbus.TYPE.BOOLEAN),
		change_notification = dbus.Introspection\
		.PROP_CHANGE_NOTIFICATION.NEW_VALUE,
	  )
	def get_CanRaise(self) :
		return False
