from keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt
import pickle


def predict_from_sklearn(model, data):
    loaded_model = pickle.load(open(model, 'rb'))
    df=pd.read_csv(data,header=0, sep=';')
    y = df.pop('win')
    # home_odd = df.pop('home_odd')
    # visitor_odd = df.pop('visitor_odd')
    X = df

    result = loaded_model.score(X, y)
       
    return result

def predict_from_neural_net(model,data):
    model = load_model(model)
    df=pd.read_csv(data,header=0, sep=';')
    y = df.pop('win')
    # home_odd = df.pop('home_odd')
    # visitor_odd = df.pop('visitor_odd')
    X = df

    model.compile(optimizer='adam',loss='binary_crossentropy', metrics=['accuracy'])  

    history = model.predict(X)

    i = 0
    correct = 0
    sure = 0
    mistaken_sure = 0
    incorrect = 0
    diff = 0
    for h in history:
            if(h[0] < 0.5) & (y[i] == 0):
                correct +=1
                if(h[0] < 0.2):
                    sure +=1
            if(h[0] >= 0.5) & (y[i] == 1):
                correct +=1
                if(h[0] > 0.8):
                    sure +=1
            else:
                diff += abs(h[0] -0.5)
                incorrect +=1
                if(h[0] <0.2) | (h[0] > 0.8):
                    mistaken_sure +=1
            i +=1
    print(correct/(correct + incorrect), sure/(sure + mistaken_sure), sure, diff/incorrect)
    return (correct/(correct + incorrect))

bin_path = "5"
csv_data = "bin/5/games16-17.csv"
nn = predict_from_neural_net("model/"+bin_path+"/neural-network.h5", csv_data)
lr = predict_from_sklearn("model/"+bin_path+"/logisitic-regression.model", csv_data)
nb = predict_from_sklearn("model/"+bin_path+"/naive_bayes.model", csv_data)
kn = predict_from_sklearn("model/"+bin_path+"/k-nearest.model", csv_data)
svm = predict_from_sklearn("model/"+bin_path+"/svm.model", csv_data)

print("neural network: ", nn)
print("logistic regression: ", lr)
print("naive bayes: ", nb)
print("k nearest: ", kn)
print("svm: ", svm)

