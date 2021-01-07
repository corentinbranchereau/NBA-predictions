from pymongo import MongoClient
import datetime
import os

class DB_Access:
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
            
            game['home_win_probability'] = 1/(1 + pow(10., -(game['home_elo_before_game'] - game['visitor_elo_before_game'])/400))
            
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
                # {'stats.reason' : { "$ne":"Did Not Play"}},
                # {'stats.reason' : { "$ne":"Did Not Dress"}},
                {'stats.reason' : { "$exists":"true"}}
            ]
        })
        return list(players)

    def get_players_stats_before_game(self, team_id, game_date, game_id ):
        #todo: only match player that are lined up for the game
        players = list(self.table_player_stats.find({
            "game_id":game_id,
            "team_id":team_id,
            
        }).sort('stats.started', -1))
        players_id = []
        for player in players:
            players_id.append(player['player_id'])

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
                        "game.date" : { "$lt" : game_date},
                        "player_id" : { "$in" : players_id}
                         
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
                        "mp":{  
                            "$cond": [ { "$gte": [ "$stats.mp", 0 ] }, "$stats.mp", 0.0]
                        },
                        "started":{  
                            "$cond": [ { "$gte": [ "$stats.started", 0 ] }, "$stats.started", 0.0]
                        },
                        "fg":{  
                            "$cond": [ { "$gte": [ "$stats.fg", 0 ] }, "$stats.fg", 0.0]
                        },
                        "DidNotPlay": {  
                            "$cond": [ {"$ifNull": ['$stats.reason', 0]}, 1.0, 0.0]
                        },
                        "fga": {  
                            "$cond": [ { "$gte": [ "$stats.fga", 0 ] }, "$stats.fga", 0.0]
                        },
                 
                        "fg_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fg_pct", 0 ] }, "$stats.fg_pct", 0.0]
                        },
                        
                        "fg3":{  
                            "$cond": [ { "$gte": [ "$stats.fg3", 0 ] }, "$stats.fg3", 0.0]
                        },
                    
                        "fg3a":{  
                            "$cond": [ { "$gte": [ "$stats.fg3a", 0 ] }, "$stats.fg3a", 0.0]
                        },

                        "fg3_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fg3_pct", 0 ] }, "$stats.fg3_pct", 0.0]
                        },

                        "ft":{  
                            "$cond": [ { "$gte": [ "$stats.ft", 0 ] }, "$stats.ft", 0.0]
                        },

                        "fta":{  
                            "$cond": [ { "$gte": [ "$stats.fta", 0 ] }, "$stats.fta", 0.0]
                        },

                        "ft_pct":{  
                            "$cond": [ { "$gte": [ "$stats.ft_pct", 0 ] }, "$stats.ft_pct", 0.0]
                        },

                        "orb":{  
                            "$cond": [ { "$gte": [ "$stats.orb", 0 ] }, "$stats.orb", 0.0]
                        },

                        "drb":{  
                            "$cond": [ { "$gte": [ "$stats.drb", 0 ] }, "$stats.drb", 0.0]
                        },

                        "trb":{  
                            "$cond": [ { "$gte": [ "$stats.trb", 0 ] }, "$stats.trb", 0.0]
                        },

                        "ast":{  
                            "$cond": [ { "$gte": [ "$stats.ast", 0 ] }, "$stats.ast", 0.0]
                        },

                        "stl":{  
                            "$cond": [ { "$gte": [ "$stats.stl", 0 ] }, "$stats.stl", 0.0]
                        },

                        "blk":{  
                            "$cond": [ { "$gte": [ "$stats.blk", 0 ] }, "$stats.blk", 0.0]
                        },

                        "tov":{  
                            "$cond": [ { "$gte": [ "$stats.tov", 0 ] }, "$stats.tov", 0.0]
                        },

                        "pf":{  
                            "$cond": [ { "$gte": [ "$stats.pf", 0 ] }, "$stats.pf", 0.0]
                        },

                        "pts":{  
                            "$cond": [ { "$gte": [ "$stats.pts", 0 ] }, "$stats.pts", 0.0]
                        },

                        "plus_minus": {"$convert":
                                {
                                    "input": "$stats.plus_minus",
                                    "to": "double",
                                    "onError": 0,  
                                    "onNull":0    
                                }

                             },

                        "ts_pct":{  
                            "$cond": [ { "$gte": [ "$stats.ts_pct", 0 ] }, "$stats.ts_pct", 0.0]
                        },

                        "efg_pct":{  
                            "$cond": [ { "$gte": [ "$stats.efg_pct", 0 ] }, "$stats.efg_pct", 0.0]
                        },

                        "fg3a_per_fga_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fg3a_per_fga_pct", 0 ] }, "$stats.fg3a_per_fga_pct", 0.0]
                        },

                        "fta_per_fga_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fta_per_fga_pct", 0 ] }, "$stats.fta_per_fga_pct", 0.0]
                        },

                        "orb_pct":{  
                            "$cond": [ { "$gte": [ "$stats.orb_pct", 0 ] }, "$stats.orb_pct", 0.0]
                        },

                        "drb_pct":{  
                            "$cond": [ { "$gte": [ "$stats.drb_pct", 0 ] }, "$stats.drb_pct", 0.0]
                        },

                        "trb_pct":{  
                            "$cond": [ { "$gte": [ "$stats.trb_pct", 0 ] }, "$stats.trb_pct", 0.0]
                        },

                        "ast_pct":{  
                            "$cond": [ { "$gte": [ "$stats.ast_pct", 0 ] }, "$stats.ast_pct", 0.0]
                        },

                        "stl_pct":{  
                            "$cond": [ { "$gte": [ "$stats.stl_pct", 0 ] }, "$stats.stl_pct", 0.0]
                        },

                        "blk_pct":{  
                            "$cond": [ { "$gte": [ "$stats.blk_pct", 0 ] }, "$stats.blk_pct", 0.0]
                        },

                        "tov_pct":{  
                            "$cond": [ { "$gte": [ "$stats.tov_pct", 0 ] }, "$stats.tov_pct", 0.0]
                        },

                        "usg_pct":{  
                            "$cond": [ { "$gte": [ "$stats.usg_pct", 0 ] }, "$stats.usg_pct", 0.0]
                        },

                        "off_rtg":{  
                            "$cond": [ { "$gte": [ "$stats.off_pct", 0 ] }, "$stats.off_pct", 0.0]
                        },

                        "def_rtg":{  
                            "$cond": [ { "$gte": [ "$stats.def_rtg", 0 ] }, "$stats.def_rtg", 0.0]
                        },

                        "bpm": {
                            "$convert":
                                {
                                    "input": "$stats.bpm",
                                    "to": "double",
                                    "onError": 0,  
                                    "onNull":0    
                                }
                            }
                    }         
                },
                {
                    "$group":
                    {
                        "_id" : "$player_name",

                        "player_id" : {"$first": "$player_id"},

                        "games_total":  {'$sum':'$total'},

                        "games_not_played" : {"$sum":"$DidNotPlay"},

                        "mp" :  {"$avg":"$mp"},

                        "started" :  {"$avg":"$started"},

                        "fg" :  {"$avg":"$fg"},

                        "fga": {"$avg":"$fga"},
                 
                        "fg_pct":{"$avg":"$fg_pct"},
                        
                        "fg3":{"$avg":"$fg3"},
                    
                        "fg3a":{"$avg":"$fg3a"},

                        "fg3_pct":{"$avg":"$fg3_pct"},

                        "ft":{"$avg":"$ft"},

                        "fta":{"$avg":"$fta"},

                        # "ft_pct":{"$avg":"$ft_pct"},

                        "orb":{"$avg":"$orb"},

                        "drb":{"$avg":"$drb"},

                        "trb":{"$avg":"$trb"},

                        "ast":{"$avg":"$ast"},

                        "stl":{"$avg":"$stl"},

                        "blk":{"$avg":"$blk"},

                        "tov":{"$avg":"$tov"},

                        "pf":{"$avg":"$pf"},

                        "pts":{"$avg":"$pts"},

                        "plus_minus":{"$avg":"$plus_minus"},

                        "ts_pct":{"$avg":"$ts_pct"},

                        "efg_pct":{"$avg":"$efg_pct"},

                        "fg3a_per_fga_pct":{"$avg":"$fg3a_per_fga_pct"},

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
                    
                }
                
        ])
        players_stats = list(items)

        for item in players_stats:
            for player in players:
                if(item['player_id'] == player['player_id']):
                    item['starting'] = player['stats']['started']
        newlist = sorted(players_stats, key=lambda k: k['starting'], reverse=True) 
        return list(newlist)

    ## Moyenne des stats (victoire, défaite, points) de tous les matchs de l'équipe ayant eu lieu avant game_date
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
            aggregate.pop('nb_win')
            aggregate.pop('nb_loose')
            aggregate.pop('nb_game')
            return aggregate
        else:
            return None
        
    def get_players_stats_aggregate_before_game(self, team_id, game_date, game_id):
        players = self.get_players_stats_before_game( team_id, game_date, game_id )
        injured = self.get_players_injured(team_id, game_id)
        for player in players:
            player['injured'] = 0
            for p in injured:
                if(p['player_id'] == player['player_id']):
                    player['injured'] = 1
            player.pop('_id',None)
            player.pop('player_id',None)
            player.pop('starting',None)
     
        return players


 ####
 #
 #  TRY NEW AGGREGATION 
 #
 #
 #####

    def get_players_grades(self, team_id, game_date, game_id ):
        
        players = list(self.table_player_stats.find({
            "game_id":game_id,
            "team_id":team_id,
            
        }).sort('stats.started', -1))
        players_id = []
        for player in players:
            players_id.append(player['player_id'])

        time_delta = datetime.timedelta(20)
        minimum_date = game_date - time_delta

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
                        "player_id" : { "$in" : players_id},
                        "$and" : [
                            { "game.date": { "$lt" : game_date}},
                            { "game.date": { "$gt" : minimum_date}}
                        ],
                         
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
                        "mp":{  
                            "$cond": [ { "$gte": [ "$stats.mp", 0 ] }, "$stats.mp", 0.0]
                        },
                        "started":{  
                            "$cond": [ { "$gte": [ "$stats.started", 0 ] }, "$stats.started", 0.0]
                        },
                        "fg":{  
                            "$cond": [ { "$gte": [ "$stats.fg", 0 ] }, "$stats.fg", 0.0]
                        },
                        "DidNotPlay": {  
                            "$cond": [ {"$ifNull": ['$stats.reason', 0]}, 1.0, 0.0]
                        },
                        "fga": {  
                            "$cond": [ { "$gte": [ "$stats.fga", 0 ] }, "$stats.fga", 0.0]
                        },
                 
                        "fg_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fg_pct", 0 ] }, "$stats.fg_pct", 0.0]
                        },
                        
                        "fg3":{  
                            "$cond": [ { "$gte": [ "$stats.fg3", 0 ] }, "$stats.fg3", 0.0]
                        },
                    
                        "fg3a":{  
                            "$cond": [ { "$gte": [ "$stats.fg3a", 0 ] }, "$stats.fg3a", 0.0]
                        },

                        "fg3_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fg3_pct", 0 ] }, "$stats.fg3_pct", 0.0]
                        },

                        "ft":{  
                            "$cond": [ { "$gte": [ "$stats.ft", 0 ] }, "$stats.ft", 0.0]
                        },

                        "fta":{  
                            "$cond": [ { "$gte": [ "$stats.fta", 0 ] }, "$stats.fta", 0.0]
                        },

                        "ft_pct":{  
                            "$cond": [ { "$gte": [ "$stats.ft_pct", 0 ] }, "$stats.ft_pct", 0.0]
                        },

                        "orb":{  
                            "$cond": [ { "$gte": [ "$stats.orb", 0 ] }, "$stats.orb", 0.0]
                        },

                        "drb":{  
                            "$cond": [ { "$gte": [ "$stats.drb", 0 ] }, "$stats.drb", 0.0]
                        },

                        "trb":{  
                            "$cond": [ { "$gte": [ "$stats.trb", 0 ] }, "$stats.trb", 0.0]
                        },

                        "ast":{  
                            "$cond": [ { "$gte": [ "$stats.ast", 0 ] }, "$stats.ast", 0.0]
                        },

                        "stl":{  
                            "$cond": [ { "$gte": [ "$stats.stl", 0 ] }, "$stats.stl", 0.0]
                        },

                        "blk":{  
                            "$cond": [ { "$gte": [ "$stats.blk", 0 ] }, "$stats.blk", 0.0]
                        },

                        "tov":{  
                            "$cond": [ { "$gte": [ "$stats.tov", 0 ] }, "$stats.tov", 0.0]
                        },

                        "pf":{  
                            "$cond": [ { "$gte": [ "$stats.pf", 0 ] }, "$stats.pf", 0.0]
                        },

                        "pts":{  
                            "$cond": [ { "$gte": [ "$stats.pts", 0 ] }, "$stats.pts", 0.0]
                        },

                        "plus_minus": {"$convert":
                                {
                                    "input": "$stats.plus_minus",
                                    "to": "double",
                                    "onError": 0,  
                                    "onNull":0    
                                }

                             },

                        "ts_pct":{  
                            "$cond": [ { "$gte": [ "$stats.ts_pct", 0 ] }, "$stats.ts_pct", 0.0]
                        },

                        "efg_pct":{  
                            "$cond": [ { "$gte": [ "$stats.efg_pct", 0 ] }, "$stats.efg_pct", 0.0]
                        },

                        "fg3a_per_fga_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fg3a_per_fga_pct", 0 ] }, "$stats.fg3a_per_fga_pct", 0.0]
                        },

                        "fta_per_fga_pct":{  
                            "$cond": [ { "$gte": [ "$stats.fta_per_fga_pct", 0 ] }, "$stats.fta_per_fga_pct", 0.0]
                        },

                        "orb_pct":{  
                            "$cond": [ { "$gte": [ "$stats.orb_pct", 0 ] }, "$stats.orb_pct", 0.0]
                        },

                        "drb_pct":{  
                            "$cond": [ { "$gte": [ "$stats.drb_pct", 0 ] }, "$stats.drb_pct", 0.0]
                        },

                        "trb_pct":{  
                            "$cond": [ { "$gte": [ "$stats.trb_pct", 0 ] }, "$stats.trb_pct", 0.0]
                        },

                        "ast_pct":{  
                            "$cond": [ { "$gte": [ "$stats.ast_pct", 0 ] }, "$stats.ast_pct", 0.0]
                        },

                        "stl_pct":{  
                            "$cond": [ { "$gte": [ "$stats.stl_pct", 0 ] }, "$stats.stl_pct", 0.0]
                        },

                        "blk_pct":{  
                            "$cond": [ { "$gte": [ "$stats.blk_pct", 0 ] }, "$stats.blk_pct", 0.0]
                        },

                        "tov_pct":{  
                            "$cond": [ { "$gte": [ "$stats.tov_pct", 0 ] }, "$stats.tov_pct", 0.0]
                        },

                        "usg_pct":{  
                            "$cond": [ { "$gte": [ "$stats.usg_pct", 0 ] }, "$stats.usg_pct", 0.0]
                        },

                        "off_rtg":{  
                            "$cond": [ { "$gte": [ "$stats.off_pct", 0 ] }, "$stats.off_pct", 0.0]
                        },

                        "def_rtg":{  
                            "$cond": [ { "$gte": [ "$stats.def_rtg", 0 ] }, "$stats.def_rtg", 0.0]
                        },

                        "bpm": {
                            "$convert":
                                {
                                    "input": "$stats.bpm",
                                    "to": "double",
                                    "onError": 0,  
                                    "onNull":0    
                                }
                            }
                    }         
                },
                {
                    "$group":
                    {
                        "_id" : "$player_name",

                        "player_id" : {"$first": "$player_id"},

                        "games_total":  {'$sum':'$total'},

                        "games_not_played" : {"$sum":"$DidNotPlay"},

                        "mp" :  {"$avg":"$mp"},

                        "started" :  {"$avg":"$started"},

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

                        "blk":{"$avg":"$blk"},

                        "tov":{"$avg":"$tov"},

                        "pf":{"$avg":"$pf"},

                        "pts":{"$avg":"$pts"},

                        "plus_minus":{"$avg":"$plus_minus"},

                        "ts_pct":{"$avg":"$ts_pct"},

                        "efg_pct":{"$avg":"$efg_pct"},

                        "fg3a_per_fga_pct":{"$avg":"$fg3a_per_fga_pct"},

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
                    
                }
                
        ])
        players_stats = list(items)

        for item in players_stats:
            for player in players:
                if(item['player_id'] == player['player_id']):
                    item['starting'] = player['stats']['started']
        newlist = sorted(players_stats, key=lambda k: k['starting'], reverse=True) 
        return list(newlist)


    def get_players_grades_aggregate(self, team_id, game_date, game_id):
        players = self.get_players_grades( team_id, game_date, game_id )
        injured = self.get_players_injured(team_id, game_id)


        for player in players:
            # player['injured'] = 0.01
            # for p in injured:
            #     if(p['player_id'] == player['player_id']):
            #         player['injured'] = 0.99
            player.pop('_id',None)
            player.pop('player_id',None)
            player.pop('games_total',None)
            player.pop('games_not_played',None)
            # player.pop('starting',None)
            player.pop('started',None)
     
        top5_average = {
                        "mp" :0, "fg" :0,"fga":0, "fg_pct":0, "fg3":0,"fg3a":0,"fg3_pct":0,"ft":0,"fta":0,"ft_pct":0,"orb":0,"drb":0,"trb":0,"ast":0,"stl":0,"blk":0,"tov":0,"pf":0,"pts":0,"plus_minus":0,"ts_pct":0,"efg_pct":0,"fg3a_per_fga_pct":0,"fta_per_fga_pct":0,"orb_pct":0,"drb_pct":0,"trb_pct":0,"ast_pct":0,"stl_pct":0,"blk_pct":0,"tov_pct":0,"usg_pct":0,"off_rtg":0,"def_rtg":0,"bpm":0,
                  }
        top5_sum = {
                        "mp" :0, "fg" :0,"fga":0, "fg_pct":0, "fg3":0,"fg3a":0,"fg3_pct":0,"ft":0,"fta":0,"ft_pct":0,"orb":0,"drb":0,"trb":0,"ast":0,"stl":0,"blk":0,"tov":0,"pf":0,"pts":0,"plus_minus":0,"ts_pct":0,"efg_pct":0,"fg3a_per_fga_pct":0,"fta_per_fga_pct":0,"orb_pct":0,"drb_pct":0,"trb_pct":0,"ast_pct":0,"stl_pct":0,"blk_pct":0,"tov_pct":0,"usg_pct":0,"off_rtg":0,"def_rtg":0,"bpm":0,
                  }
        out_average = {
                        "mp" :0, "fg" :0,"fga":0, "fg_pct":0, "fg3":0,"fg3a":0,"fg3_pct":0,"ft":0,"fta":0,"ft_pct":0,"orb":0,"drb":0,"trb":0,"ast":0,"stl":0,"blk":0,"tov":0,"pf":0,"pts":0,"plus_minus":0,"ts_pct":0,"efg_pct":0,"fg3a_per_fga_pct":0,"fta_per_fga_pct":0,"orb_pct":0,"drb_pct":0,"trb_pct":0,"ast_pct":0,"stl_pct":0,"blk_pct":0,"tov_pct":0,"usg_pct":0,"off_rtg":0,"def_rtg":0,"bpm":0,
                  }
        out_sum = {
                        "mp" :0, "fg" :0,"fga":0, "fg_pct":0, "fg3":0,"fg3a":0,"fg3_pct":0,"ft":0,"fta":0,"ft_pct":0,"orb":0,"drb":0,"trb":0,"ast":0,"stl":0,"blk":0,"tov":0,"pf":0,"pts":0,"plus_minus":0,"ts_pct":0,"efg_pct":0,"fg3a_per_fga_pct":0,"fta_per_fga_pct":0,"orb_pct":0,"drb_pct":0,"trb_pct":0,"ast_pct":0,"stl_pct":0,"blk_pct":0,"tov_pct":0,"usg_pct":0,"off_rtg":0,"def_rtg":0,"bpm":0,
                  }

        for player in players:
            # print(player)
            if(player['starting'] == 1):
                player.pop("starting", None)
                for stat in player: 
                    if(player[stat] != None):
                        top5_average[stat] += player[stat]
                        top5_sum[stat] += 1

            else:
                player.pop("starting", None)
                for stat in player: 
                    if(player[stat] != None):
                        out_average[stat] += player[stat]
                        out_sum[stat] += 1
        if(players != None):
            for stat in top5_average:
                if(top5_sum[stat] != 0):
                    top5_average[stat] = top5_average[stat] / top5_sum[stat]
            
            for stat in out_average:
                if(out_sum[stat] != 0):
                    out_average[stat] = out_average[stat] / out_sum[stat]
        
        top5_average.pop('off_rtg', None)
        top5_average.pop('pf', None)
        top5_average.pop('tov_pct', None)
        top5_average.pop('orb', None)
        out_average.pop('ft', None)
        out_average.pop('fta', None)
        out_average.pop('drb', None)
        out_average.pop('tov', None)
        out_average.pop('trb', None)
        out_average.pop('fga', None)
        out_average.pop('pts', None)
        out_average.pop('fg', None)
        out_average.pop('orb', None)
        out_average.pop('mp', None)
        out_average.pop('ast', None)
        out_average.pop('drb_pct', None)
        out_average.pop('stl', None)
        out_average.pop('ast_pct', None)
        out_average.pop('pf', None)
        out_average.pop('fg3a', None)
        out_average.pop('usg_pct', None)
        out_average.pop('trb_pct', None)
        out_average.pop('blk', None)
        out_average.pop('fta_per_fga_pct', None)
        out_average.pop('orb_pct', None)
        out_average.pop('fg3', None)
        out_average.pop('bpm', None)
        out_average.pop('tov_pct', None)
        out_average.pop('stl_pct', None)
        out_average.pop('ft_pct', None)
        out_average.pop('orb_pct', None)
        
        

        return (top5_average, out_average)



    def get_same_game_previous_stats(self,game_date,home_nick,visitor_nick):
        games = self.table_game.find({
            '$or' :[
                {
                    "home_nick" : home_nick,
                    "visitor_nick" : visitor_nick,
                    "date" : {"$lt":game_date }
                },
                 {
                    "home_nick" : visitor_nick,
                    "visitor_nick" : home_nick,
                    "date" : {"$lt":game_date }
                },
            ]
        })
       
        aggregate = {
            'nb_game':0,
            'nb_win':0,
            'nb_loose':0,
            'avg_points':0,
            'avg_diff':0,
        }
        for game in games:
            if(game['home_nick'] == home_nick):
                aggregate['avg_points'] += game['home_pts']
                aggregate['avg_diff'] += game['home_pts'] - game['visitor_pts']

                if(game['home_pts']>game['visitor_pts']):
                    aggregate['nb_win'] += 1

                elif(game['home_pts']<game['visitor_pts']):
                    aggregate['nb_loose'] += 1
                    

            elif(game['visitor_nick'] == home_nick):
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
            aggregate['avg_diff'] = aggregate['avg_diff'] / (aggregate['nb_game'] * 40) # on normalise en considérant 40 comme le max de diff 
            aggregate['win_avg'] = aggregate['nb_win'] + 0.01 / aggregate['nb_game'] #(pas très grave si le max est en réalité supérieur)

            aggregate.pop('nb_game')
            aggregate.pop('nb_win')
            aggregate.pop('nb_loose')
            
        else:
            aggregate['avg_points'] = 100 
            aggregate['avg_diff'] = 0
            aggregate['win_avg'] = 0.5

            aggregate.pop('nb_game')
            aggregate.pop('nb_win')
            aggregate.pop('nb_loose')
        return aggregate
