import keras.backend as K
import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import Input
from keras.models import Sequential, Model 
from keras.layers import BatchNormalization, Dropout, Dense
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def main():
    X, y, outcome = get_data()
    epoch = 20

    repetition = 30
    mean = 0
    for i in range(0,repetition):
        print(i)
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
        model = get_model(54, 3, 30, 0.6, 0.0)
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
                epochs=epoch, batch_size=50, callbacks=[EarlyStopping(patience=25),ModelCheckpoint('model/betting_1/odds_loss2.h5',save_best_only=True)], verbose=False)

        history_df = pd.DataFrame(history.history)
        print("val_accuracy: ", history_df['val_loss'][epoch -1] )
        mean += history_df['val_loss'][epoch -1]
        # history_df.loc[1:, ['loss', 'val_loss']].plot()
    print("mean = ", mean/repetition)
    # plt.show()
    # print('Training Loss : {}\nValidation Loss : {}'.format(model.evaluate(X_train, y_train), model.evaluate(X_test, y_test)))



def get_data():
    data=pd.read_csv("bin/7/games2018_with-preds.csv",header=0, sep=';')
    X = data.values[:,:-1]
    y = data.values[:, -1]
    y_full = np.zeros((X.shape[0], 5))
    for i, y_i in enumerate(y):
        if y_i == 1:
            y_full[i, 0] = 1.0
        if y_i == 0:
            y_full[i, 1] = 1.0
        
        y_full[i, 3] = X[i, -2] # ADD ODDS OF HOME TEAM
        y_full[i, 4] = X[i, -1] # ADD ODDS OF AWAY TEAM

    return X, y_full, y



def odds_loss(y_true, y_pred):

    home_win = y_true[:, 0:1]
    visitor_win = y_true[:, 1:2]
    no_bet = y_true[:, 2:3]
    odds_a = y_true[:, 3:4]
    odds_b = y_true[:, 4:5]

    gain_loss_vector = K.concatenate([
      home_win * (odds_a - 1) + (1 - home_win) * -1,
      visitor_win * (odds_b - 1) + (1 - visitor_win) * -1,
      K.zeros_like(odds_a)
    ], axis=1)

    return -1 * K.mean(K.sum(gain_loss_vector * y_pred, axis=1))


def get_model(input_dim, output_dim, base=1000, multiplier=0.25, p=0.2):
    inputs = Input(shape=(input_dim,))
    l = BatchNormalization()(inputs)
    # l = Dropout(p)(l)
    n = base
    l = Dense(n, activation='relu')(l)
    l = BatchNormalization()(l)
    l = Dropout(p)(l)
    n = int(n * multiplier)
    l = Dense(n, activation='relu')(l)
    l = BatchNormalization()(l)
    # l = Dropout(p)(l)
    n = int(n * multiplier)
    l = Dense(n)(l)
    outputs = Dense(output_dim, activation='softmax')(l)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='Nadam', loss=odds_loss)
    return model


main()