from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import pickle

df=pd.read_csv("bin/5/games2016.csv",header=0, sep=';')
y = df.pop('win')
X = df
mean = 0
nb_repetition = 100
for i in range(0,nb_repetition):
    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
    #Create a Gaussian Classifier
    model = KNeighborsClassifier(n_neighbors=7)

    #Train the model using the training sets
    model.fit(X_train, y_train)

    #Predict the response for test dataset
    y_pred = model.predict(X_test)
    pickle.dump(model, open('model/k-nearest_5.model', 'wb'))

    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    mean += metrics.accuracy_score(y_test, y_pred)
print('mean accuracy: ', mean/nb_repetition)