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

import os
import json
import xbmc
import xbmcvfs

class KodiInfo():
	#
	#	helper functions
	#

	@staticmethod
	def time_to_micro(time_dict):
		return 1000\
			* (
			int(time_dict["milliseconds"])\
			+ int(time_dict["seconds"]) * 1000\
			+ int(time_dict["minutes"]) * 60000\
			+ int(time_dict["hours"]) * 3600000
			)

	@classmethod
	def clear_file_name(cls, filename):
		if not filename:
			return ""

		filename = cls.GetCachedTexture(filename)
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
	def kodi_json_rpc(cls,rpc):
		rpc["jsonrpc"]="2.0"
		rpc["id"]=1
		rpc = json.dumps(rpc)
		return json.loads(xbmc.executeJSONRPC(rpc))

	@staticmethod
	def get_tag(result, path, default = None):
		for element in path:
			if element not in result:
				return default
			result = result[element]
		return result

	@classmethod
	def get_result(cls, result, path, default = None):
		path = ["result"] + path
		return cls.get_tag(result,path,default)

	@classmethod
	def is_playing_item(cls, playerid, itemid):
		item = cls.kodi_json_rpc({
			"method":"Player.GetItem",
			"params":{
				"playerid":playerid
				}
			})

		title = cls.get_result(item,['item',"label"]).strip()

		try:
			return int(itemid) == cls.get_result(item,['item',"id"])
		except ValueError:
			return itemid == "{:x}".format(abs(hash(title)))

	#
	# ***********************************************************
	#

	@classmethod
	def GetSpeed(cls, playerid):
		result = cls.kodi_json_rpc({
			"method":"Player.GetProperties",
			"params": {"playerid":playerid, "properties": ["speed"]}
			})

		return cls.get_result( result,["speed"],0)

	@classmethod
	def GetActivePlayers(cls):
		result = cls.kodi_json_rpc({
			"method":"Player.GetActivePlayers"
			})

		if "result" in result and len(result["result"]) > 0:
			return result["result"][0]

	@classmethod
	def GetItem(cls,player_id):
		result = cls.kodi_json_rpc({
			"method":"Player.GetItem",
			"params":{\
				"playerid":player_id,
				"properties": ["title","showtitle","album","duration","art","artist","genre","year","thumbnail","channel", "season", "episode","director"]
				}
			})

		return cls.get_result( result,["item"],{})

	@classmethod
	def GetBasicItem(cls):
		player = cls.GetActivePlayers()
		if not player:
			return None

		result = cls.kodi_json_rpc({
			"method":"Player.GetItem",
			"params":{\
				"playerid":player["playerid"]
				}
			})

		return str(cls.get_result(result,["item","label"]))

	@classmethod
	def GetCachedTexture(cls,item):
		result = cls.kodi_json_rpc({
			"method":"Textures.GetTextures",
			"params":{\
				"properties": ["url","cachedurl"],
				 "filter": {"field": "url", "operator": "is", "value": item}
				}
			})

		textures = cls.get_result(result,['textures'])

		if not textures:
			return item

		url = cls.get_tag(textures[0],['cachedurl'])

		if url is None:
			return item

		kodi_home = xbmcvfs.translatePath("special://home/")

		return kodi_home + "userdata/Thumbnails/" + url

	@classmethod
	def GetAudioDetails(cls,item):
		result = {}

		art = cls.get_tag( item,["thumbnail"])
		if art is None:
			art = cls.get_tag( item,["art",'album.thumb'])

		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		if item['title']:
			result['xesam:title'] = ('s',item['title'])
		if item['album']:
			result['xesam:album'] = ('s',item['album'])
		if item['artist']:
			result['xesam:artist'] = ('as',item['artist'])
		if item['genre']:
			result['xesam:genre'] = ('as',item['genre'])
		if item['year']:
			result['xesam:contentCreated'] = ('s',"{}".format(item['year']))
		return result

	@classmethod
	def GetEpisodeDetails(cls,item):
		result = {}

		art = cls.get_tag( item,["art",'season.poster'])
		if art is None:
			art = cls.get_tag( item,["art",'tvshow.poster'])
		if art is None:
			art = cls.get_tag( item,["art",'thumb'])

		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		if item['title']:
			result['xesam:title'] = ('s',item['title'])
		else:
			result['xesam:title'] = ('s',item['label'])

		info =""
		if item['year']:
			result['xesam:contentCreated'] = ('s',"{}".format(item['year']))
			info ="{} ".format(item['year'])

		if item['showtitle']:
			if info:
				info = info + " - "
			info = info + "{}  ".format(item['showtitle'])

		if item['director']:
			if info:
				info = info + " - "
			info = info + ",".join(item['director'])

		if item['genre']:
			result['xesam:genre'] = ('as',item['genre'])

		if info:
			info = info + " - {:02d}x{:02d}".format(item['season'], item['episode'])
		else:
			info = "{:02d}x{:02d}".format(item['season'], item['episode'])

		result['xesam:artist'] = ('s',info)

		return result

	@classmethod
	def GetMovieDetails(cls,item):
		result = {}

		art = cls.get_tag( item,["art",'landscape'])
		if art is None:
			art = cls.get_tag( item,["art",'poster'])

		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		if item['title']:
			result['xesam:title'] = ('s',item['title'])
		else:
			result['xesam:title'] = ('s',item['label'])

		info =""
		if item['year']:
			result['xesam:contentCreated'] = ('s',"{}".format(item['year']))
			info = "{} ".format(item['year'])

		if item['director']:
			if info:
				info = info + " - "
			info = info + ",".join(item['director'])

		if item['genre']:
			result['xesam:genre'] = ('as',item['genre'])

		if info:
			result['xesam:artist'] = ('s',info)

		return result

	@staticmethod
	def find_broadcast(broadcasts, bcid):
		for broadcast in broadcasts:
			if broadcast["broadcastid"]== bcid:
				return broadcast["title"]

		return None

	@classmethod
	def GetChannelDetails(cls,item):
		result = {}

		if item['title']:
			result['xesam:title'] = ("s", item['title'])
		else:
			result['xesam:title'] = ('s', item['label'])

		result['xesam:artist'] = ('s', item['channel'])

		art = cls.get_tag( item,["art",'thumb'])
		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		return result

	@classmethod
	def GetTotalTime(cls, playerid):
		result = cls.kodi_json_rpc({
		"method":"Player.GetProperties",
		"params": {
			"playerid": playerid,
			"properties": ["totaltime"]
			}})

		ttime = cls.get_result(result,["totaltime"])
		if ttime is None:
			return 0

		return cls.time_to_micro(ttime)

	@classmethod
	def GetDefaultDetails(cls,item):
		result = {}
		art = cls.get_tag( item,["art",'thumb'])
		if art is None:
			art = cls.get_tag( item,["thumbnail"])
		if art is not None:
			result['mpris:artUrl'] = ('s',cls.clear_file_name(art))

		title = cls.get_tag( item,["title"])
		if title is None or title == "":
			title = cls.get_tag( item,["label"])

		if title is not None:
			result['xesam:title'] = ('s',title)

		return result

	@classmethod
	def GetMediaInfo(cls):
		result = {}

		player = cls.GetActivePlayers()
		if not player:
			return {}

		item = cls.GetItem(player["playerid"])
		if player["type"]== 'audio':
			result = cls.GetAudioDetails(item)

		elif player["type"]== 'video':
			if "id" not in item or item["type"]=="unknown":
				result = cls.GetDefaultDetails(item)
			elif item["type"]=="episode":
				result = cls.GetEpisodeDetails(item)
			elif item["type"]=="movie":
				result = cls.GetMovieDetails(item)
			elif item["type"]=="channel":
				result = cls.GetChannelDetails(item)
			else:
				result['xesam:title'] = ('s',item['label'])

		if 'xesam:title' not in result:
			result['xesam:title'] = ('s', item['label'])

		if "id" in item:
			result["mpris:trackid"] = ('s', '/org/mpris/MediaPlayer2/Player/{}'.format(item["id"]))
		else:
			result["mpris:trackid"] = ('s', '/org/mpris/MediaPlayer2/Player/{:x}'.format(abs(hash(item["label"].strip()))))

		legth = cls.GetTotalTime(player["playerid"])
		if legth:
			result["mpris:length"] = ('x', legth)

		return result

	#
	#	player control
	#

	@classmethod
	def PlayOpen(cls,filename):
		if filename.startswith("file://"):
			filename = filename[7:]\
			.replace("%20"," ")\
			.replace('%2f','/')

			if os.path.isfile(filename):
				cls.kodi_json_rpc({
					"method": "Player.Open",
					"params": {
						"item":{
							"file":filename
							}}})

	@classmethod
	def PlayPause(cls):
		player = cls.GetActivePlayers()
		if player:
			cls.kodi_json_rpc({
				"method": "Player.PlayPause",
				"params": {"playerid": player['playerid'] }
				})

	@classmethod
	def PlayOnlyPlay(cls):
		player = cls.GetActivePlayers()
		if player and cls.GetSpeed(player['playerid']) == 0:
			cls.kodi_json_rpc({
			"method": "Player.PlayPause",
			"params": { "playerid": player['playerid'] }
			})

	@classmethod
	def PlayOnlyPause(cls):
		player = cls.GetActivePlayers()
		if player and cls.GetSpeed(player['playerid']) != 0:
			cls.kodi_json_rpc({
			"method": "Player.PlayPause",
			"params": {
				"playerid": player['playerid'] }
			})

	@classmethod
	def PlayStop(cls):
		player = cls.GetActivePlayers()
		if player:
			cls.kodi_json_rpc({
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

	#
	#	previouse - next functions
	#

	@staticmethod
	def find_episode(episodes, eid):
		nr = 0
		for epidetails in episodes:
			if epidetails["episodeid"] == eid:
				return nr
			nr += 1
		return None

	@classmethod
	def EpisodeGoTo(cls, item, direction):
		episodes = cls.get_result(
				cls.kodi_json_rpc({
				"method":"VideoLibrary.GetEpisodes",
				"params":{\
					"tvshowid":item["tvshowid"],
					"season":item["season"],
					"properties": ["title"]
					}
				}),
				["episodes"]
				)

		eid = cls.find_episode(episodes,item["id"])

		if direction == "previous":
			eid = max(0,eid-1)
		else:
			eid = min(len(episodes) -1 ,eid+1)

		newepi = episodes[eid]["episodeid"]

		cls.kodi_json_rpc({
				"method":"player.open",
				"params":{\
					"item":{"episodeid":newepi},
					}
				})

	@classmethod
	def PlayListGoTo(cls, playerid, direction):
		props = cls.kodi_json_rpc({
				"method":"Player.GetProperties",
				"params": {"playerid":playerid, "properties": ["playlistid","position"]}
			})

		pos = cls.get_result(props,['position'])

		playlist = cls.get_result\
			(
				cls.kodi_json_rpc({
					"method":"Playlist.GetItems",
					"params": {"playlistid":cls.get_result(props,['playlistid']),
					"properties": ["title"]}
				}),
				["items"]
			)

		if direction == "previous":
			pos = max(0,pos-1)
		else:
			pos = min(len(playlist) -1 ,pos+1)

		cls.kodi_json_rpc({
			"method": "Player.GoTo",
			"params": {
				"playerid": playerid,
				"to":pos
				}})

	@classmethod
	def PlayGoTo(cls,direction):
		player = cls.GetActivePlayers()
		if not player:
			return

		item =  cls.get_result(cls.kodi_json_rpc({
			"method":"Player.GetItem",
			"params":{\
				"playerid":player["playerid"],
				"properties": ["tvshowid","season", "episode"]
				}
			}),
			["item"])

		if item["type"]== "episode":
			cls.EpisodeGoTo(item,direction)
		else:
			cls.PlayListGoTo(player["playerid"],direction)

	@classmethod
	def PlaySetShuffle(cls,toggle):
		player = cls.GetActivePlayers()
		if not player: return False

		result = cls.kodi_json_rpc({
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

		cls.kodi_json_rpc({
			"method": "Player.SetShuffle",
			"params": {
				"playerid": player['playerid'],
				"shuffle": "toggle"
				}})

	@classmethod
	def PlayGetShuffle(cls):
		player = cls.GetActivePlayers()
		if not player: return False

		result = cls.kodi_json_rpc({
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

		result = cls.kodi_json_rpc({
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

		cls.kodi_json_rpc({
			"method": "Player.SetRepeat",
			"params": {
				"playerid": player['playerid'],
				"repeat": value
				}})

	@classmethod
	def get_current_position(cls, playerid):
		result = cls.kodi_json_rpc({
			"method":"Player.GetProperties",
			"params": {
				"playerid":playerid,
				"properties": ["time"]
				}})

		ptime = cls.get_result(result,["time"])

		if ptime is None:
			return 0

		return cls.time_to_micro(ptime)

	@classmethod
	def PlayGetPosition(cls):
		player = cls.GetActivePlayers()
		if not player: return False

		return cls.get_current_position(player['playerid'])

	@classmethod
	def player_seek(cls,playerid,seek):
		seek = round(seek / 1000000)

		cls.kodi_json_rpc({
			"method": "Player.Seek",
			"params": {
				"playerid": playerid,
				"value": {"seconds": seek }
				}})

	@classmethod
	def PlaySeek(cls,seek):
		player = cls.GetActivePlayers()
		if not player: return False

		cls.player_seek(player['playerid'],seek)

	@classmethod
	def PlayPosition(cls, track_id, position):
		player = cls.GetActivePlayers()
		if not player: return False

		if not cls.is_playing_item(player["playerid"], track_id[31:]):
			return None

		cur_pos = cls.get_current_position(player["playerid"])
		seek = (position - cur_pos)
		cls.player_seek(player['playerid'],seek)

		return cls.get_current_position(player["playerid"])

	@classmethod
	def GetVolume(cls):
		result = cls.kodi_json_rpc({
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
		cls.kodi_json_rpc({
			"method": "Application.SetVolume",
			"params": { "volume": vol }
			})

	@classmethod
	def ButtonStatus(cls):
		player = cls.GetActivePlayers()
		if not player:
			return {"CanGoNext":False,"CanGoPrevious":False,"CanPlay":False,"CanPause":False,"CanSeek":True}
		else:
			cannext = False
			canprev = False

			props = cls.kodi_json_rpc({
					"method":"Player.GetProperties",
					"params": {
						"playerid": player['playerid'],
						"properties": ["canseek","canchangespeed"]
						}})

			#canseek =  cls.get_result(props, ["canseek"])
			canpause =  cls.get_result(props, ["canchangespeed"])

			itype =  cls.get_result\
				(
					cls.kodi_json_rpc({
					"method":"Player.GetItem",
					"params":{\
						"playerid":player["playerid"]
						}
					}),
					["item","type"]
				)

			if itype == 'episode':
				cannext = True
				canprev = True
			else:
				plistid = cls.get_result\
					(
						cls.kodi_json_rpc({
							"method":"Player.GetProperties",
							"params": {"playerid":player["playerid"], "properties": ["playlistid"]}
						}),
					["playlistid"]
				)

				playlist = cls.get_result\
				(
					cls.kodi_json_rpc({
						"method":"Playlist.GetItems",
						"params": {"playlistid":plistid,
						"properties": ["title"]}
					}),
					["items"]
				)

				if len(playlist) > 1:
					cannext = True
					canprev = True

			return {"CanGoNext":cannext,"CanGoPrevious":canprev,"CanPlay":True,"CanPause":canpause,"CanSeek":True}
