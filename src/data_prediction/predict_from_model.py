from keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt

model = load_model('model.h5')
df=pd.read_csv("bin/5/games2017.csv",header=0, sep=';')
y = df.pop('win')
X = df


model.compile(optimizer='adam',  # Good default optimizer to start with
                loss='binary_crossentropy',  # how will we calculate our "error." Neural network aims to minimize loss.
                metrics=['accuracy'])  # what to track

history = model.predict(X)  # train the model

# history_df = pd.DataFrame(history.history)
        
# print("val_accuracy: ", history_df['val_accuracy'][epoch-1] )
#         # use Pandas native plot method
# history_df.loc[1:, ['loss', 'val_loss']].plot()
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
# plt.show()
  
mean = 0