import keras
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


def main():
    # the data, split between train and test sets
    df=pd.read_csv("bin/5/games2016.csv",header=0, sep=';')
    y = df.pop('win')
    X = df
    epoch = 30

    mean = 0
    for i in range(0,20):
    # if(True):
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
        # print(i)
        history = train_model_dataset_4(X_train, y_train, X_test, y_test, epoch)
        history_df = pd.DataFrame(history.history)
        mean += history_df['val_accuracy'][epoch-1] 
        print("val_accuracy: ", history_df['val_accuracy'][epoch-1] )
        # use Pandas native plot method
        # history_df.loc[1:, ['loss', 'val_loss']].plot()
    print("mean accuracy: ", mean/20)

    # plt.show()


def clean_dataset(dataset):

# demonstrate data normalization with sklearn
    # create scaler
    scaler = MinMaxScaler()
    # fit scaler on data
    scaler.fit(dataset)
    # apply transform
    normalized = scaler.transform(dataset)
    # inverse transform
    # inverse = scaler.inverse_transform(normalized)
    # print(normalized)
    return normalized

#model that best fits 2nd data scrapping. 
def train_model_dataset_2(X_train, Y_train, X_test, Y_test, epoch = 10):

    model = tf.keras.models.Sequential()  # a basic feed-forward model
    # model.add(tf.keras.layers.BatchNormalization())
   
    model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
    # model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
    model.add(tf.keras.layers.Dropout(rate=0.1))
    model.add(tf.keras.layers.Dense(16, activation=tf.nn.relu))
    # model.add(tf.keras.layers.Dropout(rate=0.05))
    # model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))  # our output layer. 10 units for 10 classes. Softmax for probability distribution

    model.compile(optimizer='adam',  # Good default optimizer to start with
                loss='binary_crossentropy',  # how will we calculate our "error." Neural network aims to minimize loss.
                metrics=['accuracy'])  # what to track

    history = model.fit(X_train, Y_train,validation_data=(X_test, Y_test), epochs=epoch, batch_size=60)  # train the model
    model.save("model/model.h5")
    return history

#model that best  fits 3rd data scrapping 
def train_model_dataset_3(X_train, Y_train, X_test, Y_test, epoch = 10):

    model = tf.keras.models.Sequential()  # a basic feed-forward model
    # model.add(tf.keras.layers.BatchNormalization())
   
    model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
    # model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
    model.add(tf.keras.layers.Dropout(rate=0.2))
    model.add(tf.keras.layers.Dense(30, activation=tf.nn.relu))
    # model.add(tf.keras.layers.Dropout(rate=0.05))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))  # our output layer. 10 units for 10 classes. Softmax for probability distribution

    model.compile(optimizer='adam',  # Good default optimizer to start with
                loss='binary_crossentropy',  # how will we calculate our "error." Neural network aims to minimize loss.
                metrics=['accuracy'])  # what to track

    history = model.fit(X_train, Y_train,validation_data=(X_test, Y_test), epochs=epoch, batch_size=120, verbose=False)  # train the model
    history_df = pd.DataFrame(history.history)
    model.save("model/model.h5")

    return history

#model that best  fits 4th data scrapping 
def train_model_dataset_4(X_train, Y_train, X_test, Y_test, epoch = 30):

    model = tf.keras.models.Sequential()  # a basic feed-forward model
    # model.add(tf.keras.layers.BatchNormalization())
   
    model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
    # model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
    model.add(tf.keras.layers.Dropout(rate=0.05))
    model.add(tf.keras.layers.Dense(30, activation=tf.nn.relu))
    # model.add(tf.keras.layers.Dropout(rate=0.05))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))  # our output layer. 10 units for 10 classes. Softmax for probability distribution

    model.compile(optimizer='adam',  # Good default optimizer to start with
                loss='binary_crossentropy',  # how will we calculate our "error." Neural network aims to minimize loss.
                metrics=['accuracy'])  # what to track

    history = model.fit(X_train, Y_train,validation_data=(X_test, Y_test), epochs=epoch, batch_size=70, verbose=False)  # train the model
    model.save("model/neural-network_5.h5")
    return history

    

main()