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
    f = open("games2020.csv", 'w')
    for game in games:
        print(indice)
        home_team = db.get_team(game['home_nick'])
        visitor_team = db.get_team(game['visitor_nick'])

        home_stats = db.get_team_stats_aggregate_before_game(game['home_nick'], game['date'])
        visitor_stats = db.get_team_stats_aggregate_before_game(game['visitor_nick'], game['date'])

        home_players = db.get_players_stats_aggregate_before_game(home_team['_id'], game['date'], game['_id'])
        visitor_players = db.get_players_stats_aggregate_before_game(visitor_team['_id'], game['date'], game['_id'])

        empty_player = {'games_total': 2, 'games_not_played': 0.0, 'mp': 11.333333333333332, 'started': 0.0, 'fg': 1.0, 'fga': 4.5, 'fg_pct': 0.25, 'fg3': 0.5, 'fg3a': 3.5, 'fg3_pct': 0.1665, 'ft': 0.0, 'fta': 1.0, 'orb': 0.0, 'drb': 0.5, 'trb': 0.5, 'ast': 0.0, 'stl': 0.0, 'blk': 0.5, 'tov': 0.0, 'pf': 2.0, 'pts': 2.5, 'plus_minus': -2.0, 'ts_pct': 0.277, 'efg_pct': 0.3335, 'fg3a_per_fga_pct': 0.8335, 'fta_per_fga_pct': 0.3335, 'orb_pct': 0.0, 'drb_pct': 4.7, 'trb_pct': 2.5, 'ast_pct': 0.0, 'stl_pct': 0.0, 'blk_pct': 3.1, 'tov_pct': 0.0, 'usg_pct': 18.6, 'off_rtg': 0.0, 'def_rtg': 109.0, 'bpm': -12.6, 'injured': 0}
        
        if(len(home_players) < 15):
            for i in range(0, 15-len(home_players)):
                home_players.append(empty_player)
        
        if(len(visitor_players) < 15):
            for j in range(0, 15-len(visitor_players)):
                visitor_players.append(empty_player)
                
        if(home_stats is not None) & (visitor_stats is not None) & (home_players is not None) & (visitor_players is not None):
            #Ecriture des entêtes
            if(indice == 0):
                for h in home_stats:
                    f.write( 'h_'+str(h) + ';')
                
              
                for h in visitor_stats:
                    f.write( 'v_'+str(h) + ';')
                
                hi=0
                for player in home_players:
                    hi +=1
                    for h in player:
                        f.write('h_'+str(h)+'_'+ str(hi) + ';')
                hi =0
                for player in visitor_players:
                    hi+=1
                    for h in player:
                        f.write('v_'+str(h)+'_'+ str(hi) + ';')
                f.write( "win" + '\n')
                
            # Ecriture des données
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
            indice += 1
            
    f.close()


def create_games_and_players_stats_csv_2(db,year):
    print("getting games")
    games = db.get_games()
    indice = 0
    f = open("games"+year+".csv", 'w')
    for game in games:
        print(indice)
        home_team = db.get_team(game['home_nick'])
        visitor_team = db.get_team(game['visitor_nick'])

        home_stats = db.get_team_stats_aggregate_before_game(game['home_nick'], game['date'])
        visitor_stats = db.get_team_stats_aggregate_before_game(game['visitor_nick'], game['date'])

        home_players = db.get_players_grades_aggregate(home_team['_id'], game['date'], game['_id'])
        visitor_players = db.get_players_grades_aggregate(visitor_team['_id'], game['date'], game['_id'])

        previous_games = db.get_same_game_previous_stats(game['date'],game['home_nick'], game['visitor_nick'])
        

        empty_player = {'pts': 0.0, 'plus_minus': 0.0, 'bpm': 0.0, 'injured': 1}

        if(len(home_players) < 15):
            for i in range(0, 15-len(home_players)):
                home_players.append(empty_player)
        
        if(len(visitor_players) < 15):
            for j in range(0, 15-len(visitor_players)):
                visitor_players.append(empty_player)
                
        if(home_stats is not None) & (visitor_stats is not None) & (home_players is not None) & (visitor_players is not None):
            #Ecriture des entêtes
            if(indice == 0):
                for h in home_stats:
                    f.write( 'h_'+str(h) + ';')
                
              
                for h in visitor_stats:
                    f.write( 'v_'+str(h) + ';')

                for h in previous_games:
                    f.write( 'v_'+str(h) + ';')
                
                hi=0
                for player in home_players:
                    hi +=1
                    for h in player:
                        f.write('h_'+str(h)+'_'+ str(hi) + ';')
                hi =0
                for player in visitor_players:
                    hi+=1
                    for h in player:
                        f.write('v_'+str(h)+'_'+ str(hi) + ';')
                f.write( "win" + '\n')
                
            # Ecriture des données
            for h in home_stats:
                if(home_stats[h] is None):
                    print(h,'home_stat')
                f.write( str(home_stats[h]) + ';')
                
            for h in visitor_stats:
                if(visitor_stats[h] is None):
                    print(h, 'visitor stat')
                f.write( str(visitor_stats[h]) + ';')
            
            for h in previous_games:
                f.write( str(previous_games[h]) + ';')
            
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
            indice += 1
            
    f.close()






year = "2020"
db = DB_Access(year)
# get_games_with_stats(db)
# games = db.get_games()
# team = db.get_team(games[10]['home_nick'])
# res = db.get_players_stats_before_game(team['_id'],games[10]['date'], games[10]['_id'] )
create_games_and_players_stats_csv_2(db,year)


