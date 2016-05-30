# Creates a JSON file containing full player stats for a given season

# USAGE: python fetch-agg-playerstats [season] [season-type] [ids (optional)]
# EXAMPLE: python fetch-agg-playerstats.py 2015-16 'Regular Season' '203092,203112'

import requests
import csv
import sys
import json


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


if len(sys.argv) < 3:
	print "ERROR: must provide the current season and season type as arguments"
	sys.exit(2)

else:
	request_url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=1&LeagueID=00&"
	season = sys.argv[1]
	# print(request_url + "Season=" + season);


	if sys.argv[3] is None:
		# get me all active players for the specified season
		url_allPlayers = (request_url + "Season=" + season) 		
		response = requests.get(url_allPlayers, headers=headers)
		response.raise_for_status()
		
		# get an array of ids for active players in the given season
		players = response.json()['resultSets'][0]['rowSet']
		ids = [players[i][0] for i in range(0, len(players))]
		# print(ids);
	else:
		ids = sys.argv[3].split(",")

	# get aggregate player stats 
	# http://stats.nba.com/stats/playerprofile?Season=2015-16&SeasonType=Regular%20Season&LeagueID=00&PlayerID=201939&GraphStartSeason=2015-16&GraphEndSeason=2015-16&GraphStat=PTS
	
	output = {}
	output['season'] = sys.argv[1]
	output['season-type'] = sys.argv[2]
	output['data'] = []

 
 	j = 0
	for i in ids:

		if(j < 5):

			# construct playerprofile request url

			player_request_url = 'http://stats.nba.com/stats/playerprofile?'
			season = sys.argv[1]
			season_type = sys.argv[2]
			league_id = "00"
			graph_start = sys.argv[1]
			graph_end = sys.argv[1]
			graph_stat = "PTS"

			url_player_profile = (player_request_url + 'PlayerID='+str(i) + "&SeasonType="+season_type + '&Season='+season + '&LeagueID='+league_id + '&GraphStartSeason='+graph_start + '&GraphEndSeason='+graph_end + '&GraphStat='+graph_stat)
			print('fetching... ' + url_player_profile + '\n');

			# make request and get season averages from response 

			player_response = requests.get(url_player_profile, headers=headers)
			player_response.raise_for_status()

			profile_stats = player_response.json()['resultSets'][0]['rowSet']

			player_obj = {}
			player_obj['player_id'] = i
			player_obj['player_name'] = profile_stats[0][1]
			player_obj['stats'] = profile_stats[0]

			output['data'].append(player_obj)


		j+=1

	# output json object to file 

	with open('../data-local/agg-playerstats/agg-playerstats_' + season + '.json', 'w') as outfile:
		json.dump(output, outfile)


















