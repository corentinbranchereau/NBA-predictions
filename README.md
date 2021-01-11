# NBA Predictions

This project aims to build a betting model that earns money. I used Python (Keras, Tensorflow, Scikit learn, Pandas, Numpy), to create the pipeline and the models. 
The system works in real time: you can see the day to day prediction, and the current balance on (my website)[http://deep-learning.corentinbranchereau.com/]

## Results 

Finaly, after weeks of data cleaning and a couple of different deep learning models, I found a combination that seems to work quite well. I built three different models : a  Sequential Neural Network, a Support Vector Machine, and a Naive Bayes model, that take as input the stats from past games, and as an output the probability that the home team is going to win. 
I trained this model with data from seasons 2015-2016 and 2016-2017. 

Then,  I created a second Neural Network, that take as input the predictions from the first models, and the odds for each game. 
I trained this neural network with data from the season 2017-2018. (this season needs to be different that the first ones, to test the prediction on new data). 

The system only bets on games where the confidence percentage is higher than 95% (about 10% of the games). Lower confidence percentage are not that accurate.

I tested this second neural network with data from season 2018-2019, and 2019-2020. 
#### for 2018-2019 the total return on investment was -0.2% (i bet around 100€, and ended the season with 99.8€)
#### for 2019-2020 the total return on investment was +2.6% (I bet around 100€, and ended the season with 102.6€)


The results could probably be improved with more data from past years, also by giving a weight to data according to the number of past games...
In the future, I also want to try to predict game results by predicting how many points each player is going to score in a game.


## Thought Process and Notes

I first scrapped NBA data from 2016 until today, from the website [Basketball-Reference](basketball-reference.com), and saved everything into a MongoDB database. 


3 different type of stats were used:

## 1
stats of each team in previous games (nb_win, nb_loose, avg_points)
for each of this stat, we reduce the amount of data by doing final_stat = home_stat - visitor_stat.
A positive stat means the home team has the lead, whereas a negative stat means the visitor team has the lead

## 2
stats of previous games between the two teams:
according to the correlation, this stat does not seem to be very useful
(previous avg points and previous avg diff needs to be dropped)

## 3
For every player stat, we do the average on the team players who are starting the game.
We do the same thing on the players who are not starting (might be relevant to test if some players are injured)
finally, we concatenate by doing final_stat = home_stat - visitor_stat

relevant stats (correlation score with winning): 
elo_score: 0.33
h-v-5_bpm : 0.29
h-v_avg_diff : 0.27
h-v_win_avg : 0.27
h-v_nb_win : 0.26
h-v-5_plus_minus : 0.23
h-v-5_ast : 0.21
h-v-5_pts : 0.21
h-v-5_stl : 0.19
h-v-5_stl_pct : 
h-v-5_ast_pct
h-v-5_fg
h-v-bench_plus_minus : 0.17
h-v-5_fg3
h-v-5_trb_pct
h-v-5_ts_pct
h-v-5_efg_pct
h-v-5_ft
h-v-5_fg3a : 0.16
h-v-5_fg_pct
h-v-5_drb
h-v_avg_points
h-v-5_fta
h-v-5_trb
h-v-5_fga : 0.15


# Results(NN) (Average on 100 different models): 

2017 - toutes les données: 0.625
2016 - toutes les données: 0.660
2016 + 2017 - toutes les données: 0.645

2016 + 2017 - nettoyés : 0.640 (we cleaned all the fields were the corelation was negative)


We can see that cleaning the columns that are not relevant does not improve the prediction. This is probably because the Neural
Network already assigns very low weight to those columns, so deleting them does not really change anything. 


# Cleaned data results : 
  
neural network:  0.5662317121391854 : 0.7694235588972431 307
logistic regression:  0.6726479146459747
naive bayes:  0.646944713870029
k nearest:  0.6862269641125122
svm:  0.6813773035887488

# not cleaned data results : 

neural network:  0.6017777777777777 : 0.7911479944674965 572 
logistic regression:  0.6711930164888458
naive bayes:  0.6542192046556741
k nearest:  0.6799224054316197
svm:  0.6585838991270611

The neural network seems to do better with uncleaned data, unless the other models, who benefit from having less columns
