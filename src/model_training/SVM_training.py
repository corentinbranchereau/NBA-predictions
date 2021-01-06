from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import pickle


df=pd.read_csv("bin/6/games16-17-18.csv",header=0, sep=';')
y = df.pop('win')
X = df
mean = 0
nb_repetition = 10
for i in range(0,nb_repetition):
        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
        #Create a Gaussian Classifier
        model = svm.SVC(decision_function_shape='ovr')

        #Train the model using the training sets
        model.fit(X_train, y_train)

        #Predict the response for test dataset
        y_pred = model.predict(X_test)
        pickle.dump(model, open('model/6/svm.model', 'wb'))

        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
        mean += metrics.accuracy_score(y_test, y_pred)
print('mean accuracy: ', mean/nb_repetition)
