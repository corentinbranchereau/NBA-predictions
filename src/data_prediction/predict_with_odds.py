from keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle


def main():
    ##LOADING DATA
    csv_data = "bin/5/games2019_with_odds.csv"
    df=pd.read_csv(csv_data,header=0, sep=';')
    y = df.pop('win')
    home_odd = df.pop('home_odd')
    visitor_odd = df.pop('visitor_odd')
    X = df

    ##LOADING MODELS
    k_near = pickle.load(open("model/k-nearest_5.model", 'rb'))
    l_regression = pickle.load(open("model/logisitic-regression_5.model", 'rb'))
    n_bayes = pickle.load(open("model/naive_bayes_5.model", 'rb'))
    svm = pickle.load(open("model/svm_5.model", 'rb'))
    n_network = load_model("model/neural-network_5_bis.h5")
    n_network.compile(optimizer='adam',loss='binary_crossentropy', metrics=['accuracy'])

    

    summ = 0
    
    for index, row in X.iterrows():
        
        a = predict_from_model(k_near,[row])
        b = predict_from_model(l_regression,[row])
        c = predict_from_model(svm,[row])
        d = predict_from_model(n_bayes,[row])
        e = predict_from_model(n_network,np.array([row]))[0]

        
        if(e >= 0.7) & (a+b+c+d >=2):
            summ -= 1
            if(y[index] == 1):
                summ += home_odd[index]
        if(e < 0.3) & (a+b+c+d <=2):
            summ -= 1
            if(y[index] == 0):
                summ += visitor_odd[index]
        print(summ)
    print("final: ",summ)





def predict_from_model(model, data):
    result = model.predict(data) 
    return result[0]


def odds_from_sklearn(model, data):
    loaded_model = pickle.load(open(model, 'rb'))
    df=pd.read_csv(data,header=0, sep=';')
    y = df.pop('win')
    home_odd = df.pop('home_odd')
    visitor_odd = df.pop('visitor_odd')
    X = df
    summ = 0
    for index, row in X.iterrows():
        result = loaded_model.score([row], [y[index]])
        summ -= 1
        if(result == 1):
            if(y[index] ==1):
                summ += home_odd[index]
            else:
                summ += visitor_odd[index]

        # print(result)
    
    return summ

def odds_from_neural_net(model,data):
    model = load_model(model)
    df=pd.read_csv(data,header=0, sep=';')
    y = df.pop('win')
    home_odd = df.pop('home_odd')
    visitor_odd = df.pop('visitor_odd')
    X = df

    model.compile(optimizer='adam',loss='binary_crossentropy', metrics=['accuracy'])  

    summ = 0 
    for index, row in X.iterrows():
        print(index)
        result = model.predict(np.array([row])) 
        print(result, y[index])
        if(result>= 0.9) | (result <0.1):
            summ -= 1
        if(result >= 0.9):
            if(y[index] == 1):
                summ += home_odd[index]
        if(result < 0.1):
            if(y[index] == 0):
                summ += visitor_odd[index]
    return summ




main()

