from keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle


def predict_from_sklearn(model, data):
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

def predict_from_neural_net(model,data):
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
        #history = model.predict(X)
        # i = 0
        # correct = 0
        # sure = 0
        # mistaken_sure = 0
        # incorrect = 0
        # diff = 0
        # for h in history:
        #     if(h[0] < 0.5) & (y[i] == 0):
        #         correct +=1
        #         if(h[0] < 0.2):
        #             sure +=1
        #     if(h[0] >= 0.5) & (y[i] == 1):
        #         correct +=1
        #         if(h[0] > 0.8):
        #             sure +=1
        #     else:
        #         diff += abs(h[0] -0.5)
        #         incorrect +=1
        #         if(h[0] <0.2) | (h[0] > 0.8):
        #             mistaken_sure +=1
        #     i +=1
    # print(correct/(correct + incorrect), sure/(sure + mistaken_sure), sure, diff/incorrect)
    # return (correct/(correct + incorrect))


csv_data = "games2019.csv"
nn = predict_from_neural_net("model/neural-network_5_bis.h5", csv_data)
# lr = predict_from_sklearn("model/logisitic-regression_5.model", csv_data)
# nb = predict_from_sklearn("model/naive_bayes_5.model", csv_data)
# kn = predict_from_sklearn("model/k-nearest_5.model", csv_data)
# svm = predict_from_sklearn("model/svm_5.model", csv_data)

print("neural network: ", nn)
# print("logistic regression: ", lr)
# print("naive bayes: ", nb)
# print("k nearest: ", kn)
# print("svm: ", svm)

