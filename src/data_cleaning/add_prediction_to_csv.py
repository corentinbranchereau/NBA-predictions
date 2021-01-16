from keras.models import load_model
import keras.backend as K
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

def main():
    ##LOADING DATA
    bin_path = str("8")
    csv_data = "bin/7/games16:18.csv"
    df=pd.read_csv(csv_data,header=0, sep=';')
    y = df.pop('win')
    home_odd = df.pop('home_odd')
    visitor_odd = df.pop('visitor_odd')
    X = df

    ##LOADING MODELS
    k_near = pickle.load(open("model/"+bin_path+"/k-nearest.model", 'rb'))
    l_regression = pickle.load(open("model/"+bin_path+"/logisitic-regression.model", 'rb'))
    n_bayes = pickle.load(open("model/"+bin_path+"/naive_bayes.model", 'rb'))
    svm = pickle.load(open("model/"+bin_path+"/svm.model", 'rb'))
    n_network = load_model("model/"+bin_path+"/neural-network.h5")
   
    

    summ = 0
    games = 0
    a = []
    b = []
    c = []
    d = []
    e = []
    for index, row in X.iterrows():
        
        a.append( predict_from_model(k_near,[row])[0])
        b.append( predict_from_model(l_regression,[row])[0])
        c.append( predict_from_model(svm,[row])[0])
        d.append( predict_from_model(n_bayes,[row])[0])
        e.append( predict_from_model(n_network,np.array([row]))[0][0])
      
        if(e[index] >0.5) :
            summ -= 1
            games +=1
            if(y[index] == 1):
                summ += home_odd[index]
        if(e[index] <= 0.5) :
            summ -= 1
            games += 1
            if(y[index] == 0):
                summ += visitor_odd[index]
        print(summ)
        print(index)

    print("final: ",summ, "games : ", games)

    df['k-near_pred'] = a  
    df['l-regression_pred'] = b
    df['svm_pred'] = c
    df['n-bayes_pred'] = d
    df['n-network_pred'] = e
    df['home_odd'] = home_odd
    df['visitor_odd'] = visitor_odd
    df['win'] = y
    df.drop(df.columns[0], axis=1)
    df.to_csv('games16:18_with-preds.csv',sep=';')

def predict_from_model(model, data):
    result = model.predict(data) 
    return result


main()