from pymongo import MongoClient
import datetime
import os
import pandas as pd



date_year = 2019
client = MongoClient(os.environ["PREDICTIZ_CREDENTIALS"])
       
db = client["season_" + str(date_year)]
table_team = db["team"]
table_player = db["player"]
table_game = db["game"]
table_player_stats = db["playerStats"]
print("Atlas MongoDB connected")

team_dict = {
"NewOrleans":"NOP",
"Toronto": "TOR", 
"LALakers" : "LAL",
"LAClippers":"LAC",
"Indiana":"IND",
"Cleveland":"CLE",
"Orlando":"ORL",
"Chicago":"CHI",
"Charlotte":"CHO",
"Boston":"BOS",
"Philadelphia":"PHI",
"Memphis":"MEM",
"Miami":"MIA",
"Minnesota":"MIN",
"Brooklyn":"BRK",
"NewYork":"NYK",
"SanAntonio":"SAS",
"Washington":"WAS",
"Dallas":"DAL",
"OklahomaCity":"OKC",
"Utah":"UTA",
"Sacramento":"SAC",
"Phoenix":"PHO",
"Denver":"DEN",
"Portland":"POR",
"Atlanta":"ATL",
"Detroit":"DET",
"Milwaukee" :"MIL", 
"Houston":"HOU",
"GoldenState":"GSW",
}

data=pd.read_csv("bin/cotes/odds-19.csv",header=0, sep=';')
i = 0
for index, row in data.iterrows():
    if(row['ML'] < 0 ):
        row['ML'] = (1 - 100/row['ML'])
    else:
        row['ML'] = (1 + row['ML']/100)
    
    team = None
    date_month = int(str(row['Date'])[:-2])
    date_day = int(str(row['Date'])[-2:])
    if(date_month > 7):
        date = datetime.datetime(date_year -1, date_month, date_day)
    else:
        date = datetime.datetime(date_year, date_month, date_day)
        
    time_delta = datetime.timedelta(hours=5)
    min_date = date - time_delta
    max_date = date + time_delta

    if(row['VH'] == 'H'):
        team = table_game.update_one({
                "home_nick": team_dict[row['Team']],
                "$and" : [
                                { "date": { "$gte" : min_date}},
                                { "date": { "$lte" : max_date}}
                            ], 
                
            },
            {
                "$set":{
                    "home_odd":row['ML']
                }
            },upsert=False)
    else:
        team = table_game.update_one({
                "visitor_nick": team_dict[row['Team']],
                "$and" : [
                                { "date": { "$gte" : min_date}},
                                { "date": { "$lte" : max_date}}
                            ], 
                
            },
            {
                "$set":{
                    "visitor_odd":row['ML']
                }
            },upsert=False)
    print(i)
    i+=1

                
            
        
