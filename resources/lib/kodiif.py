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
import os
import json

class KodiInfo():
	@classmethod
	def get_info(cls,rpc):
		rpc["jsonrpc"]="2.0"
		rpc["id"]=1
		rpc = str(rpc).replace("'",'"')
		x = xbmc.executeJSONRPC(rpc)
		return json.loads(x)

	@classmethod
	def post(cls,rpc):
		return cls.get_info(rpc)

	@staticmethod
	def get_result(result, path, default = None):
		path = ["result"] + path

		for element in path:
			if element not in result:
				return default
			result = result[element]
		return result

	@classmethod
	def GetSpeed(cls, playerid):
		result = cls.get_info({
			"method":"Player.GetProperties",
			"params": {"playerid":playerid, "properties": ["speed"]}
			})

		return cls.get_result( result,["speed"],0)

	@classmethod
	def GetActivePlayers(cls):
		result = cls.get_info({
			"method":"Player.GetActivePlayers"
			})

		if "result" in result and len(result["result"]) > 0:
			return result["result"][0]

	@classmethod
	def GetItem(cls,player_id):
		result = cls.get_info({
			"method":"Player.GetItem",
			"params":{ "playerid":player_id }
			})

		return cls.get_result( result,["item"],{})

	@staticmethod
	def clear_file_name(filename):
		result = filename\
		.replace('%2f','/')\
		.replace('%3a',':')\
		.replace('%20',' ')\
		.replace("image://","")

		if result[0] == "/":
			result = "file://" + result

		if result[-1]== "/":
			result = result[:-1]

		return result

	@classmethod
	def GetAudioDetails(cls,songid):
		result = {}
		tmp = cls.get_info({
			"method":"AudioLibrary.GetSongDetails",
			"params": {
				"songid": songid,
				"properties": ["title","album","duration","art"]
				}
			})

		info = cls.get_result( tmp,["songdetails"])

		if info is None:
			return {}

		art = cls.get_result( tmp,["songdetails","art",'album.thumb'])

		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		result['xesam:title'] = ('s',info['title'])
		result['xesam:album'] = ('s',info['album'])
		result['mpris:length'] = ('x',info['duration'] * 1000)
		return result

	@classmethod
	def GetTvShowDetails(cls,tvid):
		if tvid < 0:
			return ""

		tmp = cls.get_info({
			"method":"VideoLibrary.GetTVShowDetails",
			"params": { "tvshowid": tvid, "properties": ["title"] }
			})

		return cls.get_result(tmp,["tvshowdetails","title"],"")

	@classmethod
	def GetEpisodeDetails(cls,epiid):
		result = {}
		tmp = cls.get_info({
			"method":"VideoLibrary.GetEpisodeDetails",
			"params": {
				"episodeid": epiid,
				"properties": ["tvshowid","title","art"]
				}
			})

		info = cls.get_result( tmp,["episodedetails"])

		if info is None:
			return {}

		art = cls.get_result( tmp,["episodedetails","art",'season.poster'])
		if art is None:
			art = cls.get_result( tmp,["episodedetails","art",'tvshow.poster'])
		if art is None:
			art = cls.get_result( tmp,["episodedetails","art",'thumb'])

		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		result['xesam:title'] = ('s',info['title'])
		result['xesam:album'] = \
			('s',cls.GetTvShowDetails(info['tvshowid']))

		return result

	@classmethod
	def GetMovieDetails(cls,movieid):
		result = {}
		tmp = cls.get_info({
			"method":"VideoLibrary.GetMovieDetails",
			"params": {
				"movieid": movieid,
				"properties": ["title","art"]
				}
			})

		info = cls.get_result( tmp,["moviedetails"])

		if info is None:
			return {}

		art = cls.get_result( tmp,["moviedetails","art",'landscape'])
		if art is None:
			art = cls.get_result( tmp,["moviedetails","art",'poster'])

		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		result['xesam:title'] = ('s',info['title'])
		return result

	@staticmethod
	def find_broadcast(broadcasts, bcid):
		for broadcast in broadcasts:
			if broadcast["broadcastid"]== bcid:
				return broadcast["title"]

		return None

	@classmethod
	def GetChannelDetails(cls,channelid):
		result = {}
		tmp = cls.get_info({
			"method":"PVR.GetChannelDetails",
			"params": {
				"channelid": channelid,
				"properties": ["channel","broadcastnow"]
			}
		})

		info = cls.get_result( tmp,["channeldetails"])
		bcid = cls.get_result( tmp,["channeldetails",'broadcastnow','broadcastid'])

		if info is not None:
			result['xesam:title'] = ('s',info['label'])

		if bcid is None:
			return result

		tmp = cls.get_info({
			"method":"PVR.GetBroadcasts",
			"params": {
				"channelid": channelid,
				"properties": ["title"]
				}
			})

		title = cls.find_broadcast\
			(
			cls.get_result( tmp,['broadcasts'],[]),
			bcid
			)

		if title is None:
			return result

		if 'xesam:title' in result:
			result['xesam:album'] = result['xesam:title']
		result['xesam:title'] = ("s", title)

		return result

	@classmethod
	def GetTotalTime(cls, playerid):
		result = cls.get_info({
		"method":"Player.GetProperties",
		"params": {
			"playerid": playerid,
			"properties": ["totaltime"]
			}})

		ttime = cls.get_result(result,["totaltime"])
		if ttime is None:
			return 0

		totaltime = int(ttime["milliseconds"])\
			+ int(ttime["seconds"]) * 1000\
			+ int(ttime["minutes"]) * 60000\
			+ int(ttime["hours"]) * 3600000

		return totaltime * 1000

	@classmethod
	def GetMediaInfo(cls):
		result = {}

		player = cls.GetActivePlayers()
		if not player:
			return {}

		item = cls.GetItem(player["playerid"])

		if player["type"]== 'audio':
			if "id" in item:
				result = cls.GetAudioDetails(item["id"])
			else:
				result['xesam:title'] = ('s',item['label'])

		elif player["type"]== 'video':
			if "id" not in item or item["type"]=="unknown":
				result['xesam:title'] = ('s',item['label'])
			elif item["type"]=="episode":
				result = cls.GetEpisodeDetails(item["id"])
			elif item["type"]=="movie":
				result = cls.GetMovieDetails(item["id"])
			elif item["type"]=="channel":
				result = cls.GetChannelDetails(item["id"])
			else:
				result['xesam:title'] = ('s',item['label'])

		result["mpris:length"] = ('x', cls.GetTotalTime(player["playerid"]))

		return result

	@classmethod
	def PlayPause(cls):
		player = cls.GetActivePlayers()
		if player:
			cls.post({
				"method": "Player.PlayPause",
				"params": {"playerid": player['playerid'] }
				})

	@classmethod
	def PlayOnlyPlay(cls):
		player = cls.GetActivePlayers()
		if player and cls.GetSpeed(player['playerid']) == 0:
			cls.post({
			"method": "Player.PlayPause",
			"params": { "playerid": player['playerid'] }
			})

	@classmethod
	def PlayOnlyPause(cls):
		player = cls.GetActivePlayers()
		if player and cls.GetSpeed(player['playerid']) != 0:
			cls.post({
			"method": "Player.PlayPause",
			"params": {
				"playerid": player['playerid'] }
			})

	@classmethod
	def PlayStop(cls):
		player = cls.GetActivePlayers()
		if player:
			cls.post({
				"method": "Player.Stop",
				"params": {
				"playerid": player['playerid']
				}
				})

	@classmethod
	def PlayStatus(cls):
		player = cls.GetActivePlayers()
		if not player: return "Stopped"
		if cls.GetSpeed(player['playerid']) == 0: return "Paused"
		return "Playing"

	@classmethod
	def PlayGoTo(cls,direction):
		player = cls.GetActivePlayers()
		if player:
			cls.post({
				"method": "Player.GoTo",
				"params": {
					"playerid": player['playerid'],
					"to":direction
					}})

	@classmethod
	def PlayOpen(cls,filename):
		if filename.startswith("file://"):
			filename = filename[7:]\
			.replace("%20"," ")\
			.replace('%2f','/')

			if os.path.isfile(filename):
				cls.post({
					"method": "Player.Open",
					"params": {
						"item":{
							"file":filename
							}}})

	@classmethod
	def PlaySetShuffle(cls,toggle):
		player = cls.GetActivePlayers()
		if not player: return False

		result = cls.get_info({
			"method":"Player.GetProperties",
			"params": {
				"playerid": player['playerid'],
				"properties": ["shuffled"]
				}})

		current = cls.get_result(result,["shuffled"])

		if current is None:
			return

		if current == toggle:
			return

		cls.post({
			"method": "Player.SetShuffle",
			"params": {
				"playerid": player['playerid'],
				"shuffle": "toggle"
				}})

	@classmethod
	def PlayGetShuffle(cls):
		player = cls.GetActivePlayers()
		if not player: return False

		result = cls.get_info({
			"method":"Player.GetProperties",
			"params": {
				"playerid": player['playerid'],
				"properties": ["shuffled"]
				}})

		return cls.get_result(result,["shuffled"],False)

	@classmethod
	def PlayGetRepeat(cls):
		player = cls.GetActivePlayers()
		if not player: return "None"

		result = cls.get_info({
			"method":"Player.GetProperties",
			"params": {
				"playerid": player['playerid'],
				"properties": ["repeat"]
				}})

		repeat = cls.get_result(result,["repeat"])

		if repeat is None:
			return "None"

		return ["None","Track","Playlist"]\
			[["off","one","all"].index(result["result"]["repeat"])]

	@classmethod
	def PlaySetRepeat(cls,val):
		player = cls.GetActivePlayers()
		if not player: return False

		value = ["off","one","all"]\
		[["None","Track","Playlist"].index(val)]

		cls.post({
			"method": "Player.SetRepeat",
			"params": {
				"playerid": player['playerid'],
				"repeat": value
				}})

	@classmethod
	def PlayGetPosition(cls):
		player = cls.GetActivePlayers()
		if not player: return False

		result = cls.get_info({
			"method":"Player.GetProperties",
			"params": {
				"playerid": player['playerid'],
				"properties": ["time"]
				}})

		ptime = cls.get_result(result,["time"])

		if ptime is None:
			return 0

		playtime = int(ptime["milliseconds"])\
			+ int(ptime["seconds"]) * 1000\
			+ int(ptime["minutes"]) * 60000\
			+ int(ptime["hours"]) * 3600000

		return playtime * 1000

	@classmethod
	def PlaySeek(cls,seek):
		player = cls.GetActivePlayers()
		if not player: return False

		seek = round(seek / 1000000)

		cls.post({
			"method": "Player.Seek",
			"params": {
				"playerid": player['playerid'],
				"value": {"seconds": seek }
				}})

	@classmethod
	def GetVolume(cls):
		result = cls.get_info({
			"method":"Application.GetProperties",
			"params": {"properties": ["volume"]}
			})

		vol = cls.get_result(result,["volume"])

		if vol is None:
			return 0

		return float(vol) / 100

	@classmethod
	def SetVolume(cls, vol):
		vol = min( max( int(vol * 100), 0) , 100)
		cls.post({
			"method": "Application.SetVolume",
			"params": { "volume": vol }
			})
