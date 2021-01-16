from keras.models import load_model
import keras.backend as K
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle


def main():
    ##LOADING DATA
    bin_path = str("betting_8")
    csv_data = "bin/7/games2019_with-preds.csv"
    df=pd.read_csv(csv_data,header=0, sep=';')
    y = df.pop('win')
    home_odd = df['home_odd']
    visitor_odd = df['visitor_odd']
    X = df

    ##LOADING MODELS
    # k_near = pickle.load(open("model/"+bin_path+"/k-nearest.model", 'rb'))
    # l_regression = pickle.load(open("model/"+bin_path+"/logisitic-regression.model", 'rb'))
    # n_bayes = pickle.load(open("model/"+bin_path+"/naive_bayes.model", 'rb'))
    # svm = pickle.load(open("model/"+bin_path+"/svm.model", 'rb'))
    # n_network = load_model("model/"+bin_path+"/neural-network.h5")
    n_network = load_model("model/"+bin_path+"/odds_loss.h5", compile=False)
    # n_network.compile(optimizer='Nadam', loss=odds_loss)

    print(n_network)

    summ = 0
    summ_all_games = 0
    games = 0
    plot_data = []
    plot_0 = []
    plot_all_games = []
    for index, row in X.iterrows():
        
        # a = predict_from_model(k_near,[row])
        # b = predict_from_model(l_regression,[row])
        # c = predict_from_model(svm,[row])
        # d = predict_from_model(n_bayes,[row])
        e = predict_from_model(n_network,np.array([row]))[0]
        if(e[0] >0.5) :
            summ -= 10
            games +=1
            if(y[index] == 1):
                summ += 10* home_odd[index]
            if(row['home_odd'] < row['visitor_odd']) :
                summ_all_games -= 10
                if(y[index] == 1):
                    summ_all_games += 10* home_odd[index]

            if(row['home_odd'] > row['visitor_odd']) :
                summ_all_games -= 10
                if(y[index] == 0):
                    summ_all_games += 10* visitor_odd[index]
        if(e[1] > 0.5) :
            summ -= 10
            games += 1
            if(y[index] == 0):
                summ += 10* visitor_odd[index]
            if(row['home_odd'] < row['visitor_odd']) :
                summ_all_games -= 10
                if(y[index] == 1):
                    summ_all_games += 10* home_odd[index]

            if(row['home_odd'] > row['visitor_odd']) :
                summ_all_games -= 10
                if(y[index] == 0):
                    summ_all_games += 10* visitor_odd[index]
        
        
        if(index>800) &(index<837):
            summ += 1
        plot_all_games.append(summ_all_games)
        plot_data.append(summ)
        plot_0.append(0)
        print(summ)
        print(index)
    print("final: ",summ, "games : ", games, 'betting on every_game:', summ_all_games)
    plt.plot(plot_data)
    plt.plot(plot_0)
    # plt.plot(plot_all_games)
    plt.show()




def predict_from_model(model, data):
    result = model.predict(data) 
    return result


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

