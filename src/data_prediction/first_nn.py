import keras
import numpy as np
import tensorflow as tf

num_classes = 10
input_shape = (28, 28, 1)

# the data, split between train and test sets
dataset=np.loadtxt("games2.csv",delimiter=";")
# split into input (X) and output (Y) variables
X_train=dataset[:500,0:1152]
Y_train=dataset[:500,1152]
X_test=dataset[500:,0:1152]
Y_test=dataset[500:,1152]



model = tf.keras.models.Sequential()  # a basic feed-forward model
# model.add(tf.keras.layers.Flatten())  # takes our 28x28 and makes it 1x784
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))  # a simple fully-connected layer, 128 units, relu activation
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))

model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))  # our output layer. 10 units for 10 classes. Softmax for probability distribution

model.compile(optimizer='adam',  # Good default optimizer to start with
              loss='binary_crossentropy',  # how will we calculate our "error." Neural network aims to minimize loss.
              metrics=['accuracy'])  # what to track

model.fit(X_train, Y_train, epochs=15)  # train the model

val_loss, val_acc = model.evaluate(X_test, Y_test)  # evaluate the out of sample data with model
print(val_loss)  # model's loss (error)
print(val_acc)  # model's accuracy
