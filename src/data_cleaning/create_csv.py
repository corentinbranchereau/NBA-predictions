from DB_Access import DB_Access


def create_games_stats_csv(db):
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

def create_games_and_players_stats_csv(db):
    print("getting games")
    games = db.get_games()
    indice = 0
    f = open("games.csv", 'w')
    for game in games:
        print(indice)
        indice += 1
        home_team = db.get_team(game['home_nick'])
        visitor_team = db.get_team(game['visitor_nick'])

        home_stats = db.get_team_stats_aggregate_before_game(game['home_nick'], game['date'])
        visitor_stats = db.get_team_stats_aggregate_before_game(game['visitor_nick'], game['date'])

        home_players = db.get_players_stats_aggregate_before_game(home_team['_id'], game['date'], game['_id'])
        visitor_players = db.get_players_stats_aggregate_before_game(visitor_team['_id'], game['date'], game['_id'])

        empty_player = {'games_total': 6, 'games_not_played': 2.0, 'mp': 14.818888888888889, 'started': 0.0, 'fg': 1.6833333333333333, 'fga': 3.316666666666667, 'fg_pct': 0.48158620689655174, 'fg3': 0.0, 'fg3a': 0.03333333333333333, 'fg3_pct': 0.0, 'ft': 0.6666666666666666, 'fta': 0.8166666666666667, 'ft_pct': 0.7319130434782608, 'orb': 0.6166666666666667, 'drb': 1.1666666666666667, 'trb': 1.7833333333333334, 'ast': 1.8333333333333333, 'stl': 0.48333333333333334, 'blk': 0.4, 'tov': 0.5833333333333334, 'pf': 1.1, 'pts': 4.033333333333333, 'plus_minus': 0.6833333333333333, 'ts_pct': 0.5344655172413793, 'efg_pct': 0.48158620689655174, 'fg3a_per_fga_pct': 0.0115, 'fta_per_fga_pct': 0.30786206896551727, 'orb_pct': 4.428333333333333, 'drb_pct': 8.03, 'trb_pct': 6.291666666666667, 'ast_pct': 15.043333333333333, 'stl_pct': 1.5266666666666666, 'blk_pct': 2.0349999999999997, 'tov_pct': 13.816949152542374, 'usg_pct': 11.671666666666665, 'off_rtg': 0.0, 'def_rtg': 109.03333333333333, 'bpm': -1.005}

   
        if(len(home_players) < 15):
            for i in range(0, 15-len(home_players)):
                home_players.append(empty_player)
        
        if(len(visitor_players) < 15):
            for j in range(0, 15-len(visitor_players)):
                visitor_players.append(empty_player)
                
        if(home_stats is not None) & (visitor_stats is not None) & (home_players is not None) & (visitor_players is not None):
            for h in home_stats:
                if(home_stats[h] is None):
                    print(h,'home_stat')
                f.write( str(home_stats[h]) + ';')
                
            for h in visitor_stats:
                if(visitor_stats[h] is None):
                    print(h, 'visitor stat')
                f.write( str(visitor_stats[h]) + ';')
            
            for player in home_players:
                for h in player:
                    if(player[h] is None):
                        print(h, 'player home')
                    f.write( str(player[h]) + ';')

            for player in visitor_players:
                for h in player:
                    if(player[h] is None):
                        print(h, 'visitor home')
                    f.write( str(player[h]) + ';')

            f.write( str(game['winner']) + '\n')
            


db = DB_Access("2019")
# get_games_with_stats(db)
# games = db.get_games()
# team = db.get_team(games[10]['home_nick'])
# res = db.get_players_stats_before_game(team['_id'],games[10]['date'], games[10]['_id'] )
create_games_and_players_stats_csv(db)


