from pymongo import MongoClient
import os



class AtlasDB:
    def __init__(self, year):
        self.client = MongoClient(os.environ["PREDICTIZ_CREDENTIALS"])
        dblist = self.client.list_database_names()
       
        db = self.client["season_" + year]
        self.table_team = db["team"]
        self.table_player = db["player"]
        self.table_game = db["game"]
        self.table_player_stats = db["playerStats"]
        print("Atlas MongoDB connected")


    def get_games(self):
        games = list(self.table_game.find({}))
        for game in games:
            if(game['home_pts'] > game['visitor_pts']):
                game['winner'] = 1
            else:
                game['winner'] = 0
        return games
    

    #team = home or visitor
    def get_team_previous_games(self, team_nick, date, limit=0):
        games = self.table_game.find({
            '$or' :[
                {
                    "home_nick" : team_nick,
                    "date" : {"$lt":date }
                },
                {
                    "visitor_nick":team_nick,
                    "date" : {"$lt":date }   
                }
            ]
        }).limit(limit)
        return games

    def get_team(self, team_nick):
        return self.table_team.find_one({'nick':team_nick})

    def get_players_injured(self,team_id,game_id):
        players = self.table_player_stats.find({
            'game_id' : game_id,
            'team_id' : team_id,
            '$and' : [
                {'stats.reason' : { "$ne":"Did Not Play"}},
                {'stats.reason' : { "$ne":"Did Not Dress"}},
                {'stats.reason' : { "$exists":"true"}}
            ]
        })
        return list(players)

    def get_players_stats_aggregate_before_game(self, team_id, game_date, limit=0):
        items = self.table_player_stats.aggregate(pipeline = [
              {
                    "$lookup":
                    {
                        "from": "game",
                        "localField": "game_id",
                        "foreignField": "_id",
                        "as": "game"
                    }
                }, 
                {
                    "$match":
                    {
                        "team_id" : team_id,
                        "game.date" : { "$lt" : game_date} 
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "player_id":1,
                        "game_id":1,
                        "game":1,
                        "team_id":1,
                        # "stats":1,
                        "player_name" : "$stats.name",
                        "total": {  
                            "$cond": [ { "$gte": [ 1, 0 ] }, 1, 0]
                        },
                        "fg":{  
                            "$cond": [ { "$gte": [ "$stats.fg", 0 ] }, "$stats.fg", 0.0]
                        },
                        "DidNotPlay": {  
                            "$cond": [ {"$ifNull": ['$stats.reason', 0]}, 1.0, 0.0]
                        },
                        "fga": "$stats.fga",
                 
                        "fg_pct":"$stats.fg_pct",
                        
                        "fg3":"$stats.fg3",
                    
                        "fg3a":"$stats.fg3a",

                        "fg3_pct":"$stats.fg3_pct",

                        "ft":"$stats.ft",

                        "fta":"$stats.fta",

                        "ft_pct":"$stats.ft_pct",

                        "orb":"$stats.orb",

                        "drb":"$stats.drb",

                        "trb":"$stats.trb",

                        "ast":"$stats.ast",

                        "stl":"$stats.stl",

                        "blk":"$stats.blk",

                        "tov":"$stats.tov",

                        "pf":"$stats.pf",

                        "pts":"$stats.pts",

                        "plus_minus":"$stats.plus_minus",

                        "ts_pct":"$stats.ts_pct",

                        "efg_pct":"$stats.efg_pct",

                        "fg3a_per_fga_pct":"$stats.fg3a_per_fga_pct",

                        "fta_per_fga_pct":"$stats.fta_per_fga_pct",

                        "orb_pct":"$stats.orb_pct",

                        "drb_pct":"$stats.drb_pct",

                        "trb_pct":"$stats.trb_pct",

                        "ast_pct":"$stats.ast_pct",

                        "stl_pct":"$stats.stl_pct",

                        "blk_pct":"$stats.blk_pct",

                        "tov_pct":"$stats.tov_pct",

                        "usg_pct":"$stats.usg_pct",

                        "off_rtg":"$stats.off_rtg",

                        "def_rtg":"$stats.def_rtg",

                        "bpm":"$stats.bpm",

                    }
                },
                {
                    "$group":
                    {
                        "_id" : "$player_name",

                        "games_total":  {'$sum':'$total'},

                        "games_not_played" : {"$sum":"$DidNotPlay"},

                        "fg" :  {"$avg":"$fg"},

                        "fga": {"$avg":"$fga"},
                 
                        "fg_pct":{"$avg":"$fg_pct"},
                        
                        "fg3":{"$avg":"$fg3"},
                    
                        "fg3a":{"$avg":"$fg3a"},

                        "fg3_pct":{"$avg":"$fg3_pct"},

                        "ft":{"$avg":"$ft"},

                        "fta":{"$avg":"$fta"},

                        "ft_pct":{"$avg":"$ft_pct"},

                        "orb":{"$avg":"$orb"},

                        "drb":{"$avg":"$drb"},

                        "trb":{"$avg":"$trb"},

                        "ast":{"$avg":"$ast"},

                        "stl":{"$avg":"$stl"},

                        "blk":{"$avg":"blk"},

                        "tov":{"$avg":"$tov"},

                        "pf":{"$avg":"pf"},

                        "pts":{"$avg":"$pts"},

                        "plus_minus":{"$avg":"$plus_minus"},

                        "ts_pct":{"$avg":"$ts_pct"},

                        "efg_pct":{"$avg":"$efg_pct"},

                        "fg3a_per_fga_pct":{"$avg":"$fga3_per_fga_pct"},

                        "fta_per_fga_pct":{"$avg":"$fta_per_fga_pct"},

                        "orb_pct":{"$avg":"$orb_pct"},

                        "drb_pct":{"$avg":"$drb_pct"},

                        "trb_pct":{"$avg":"$trb_pct"},

                        "ast_pct":{"$avg":"$ast_pct"},

                        "stl_pct":{"$avg":"$stl_pct"},

                        "blk_pct":{"$avg":"$blk_pct"},

                        "tov_pct":{"$avg":"$tov_pct"},

                        "usg_pct":{"$avg":"$usg_pct"},

                        "off_rtg":{"$avg":"$off_rtg"},

                        "def_rtg":{"$avg":"$def_rtg"},

                        "bpm":{"$avg":"$bpm"},
                    },
                    
                }, 
                
        ])

        return list(items)


    def get_team_stats_aggregate_before_game(self,team_nick,game_date):
        items = self.table_game.find(
             
                    {
                        "$or" :[
                            {"home_nick":team_nick},
                            {"visitor_nick":team_nick}
                            ],
                        "date" : { "$lt" : game_date} 
                    }
                
            )
        games = list(items)
        aggregate = {
            'nb_game':0,
            'nb_win':0,
            'nb_loose':0,
            'avg_points':0,
            'avg_diff':0,
        }
        for game in games:
            if(game['home_nick'] == team_nick):
                aggregate['avg_points'] += game['home_pts']
                aggregate['avg_diff'] += game['home_pts'] - game['visitor_pts']

                if(game['home_pts']>game['visitor_pts']):
                    aggregate['nb_win'] += 1

                elif(game['home_pts']<game['visitor_pts']):
                    aggregate['nb_loose'] += 1
                    

            elif(game['visitor_nick'] == team_nick):
                aggregate['avg_points'] += game['visitor_pts']
                aggregate['avg_diff'] += game['visitor_pts'] - game['home_pts']
                

                if(game['home_pts']<game['visitor_pts']):
                    aggregate['nb_win'] += 1

                elif(game['home_pts']>game['visitor_pts']):
                    aggregate['nb_loose']+= 1


            aggregate['nb_game'] += 1 
        #for end
        if(aggregate['nb_game'] > 0):
            aggregate['avg_points'] = aggregate['avg_points'] / aggregate['nb_game'] 
            aggregate['avg_diff'] = aggregate['avg_diff'] / aggregate['nb_game']
            aggregate['win_avg'] = aggregate['nb_win'] / aggregate['nb_game']
            return aggregate
        else:
            return None
        

#MAIN


def get_games_with_stats(db):
    print("getting games")
    games = db.get_games()
    f = open("games.csv", 'w')
    i = 0
    for game in games:
        print(i)
        i+=1
        home_stats = db.get_team_stats_aggregate_before_game(game['home_nick'], game['date'])
        visitor_stats = db.get_team_stats_aggregate_before_game(game['visitor_nick'], game['date'])
        if(home_stats is not None) & (visitor_stats is not None):
            # print(game, home_stats, visitor_stats)
            for h in home_stats:
                f.write( str(home_stats[h]) + ';')
                
            for h in visitor_stats:
                f.write( str(visitor_stats[h]) + ';')
            
            f.write( str(game['winner']) + '\n')


db = AtlasDB("2020")
get_games_with_stats(db)



