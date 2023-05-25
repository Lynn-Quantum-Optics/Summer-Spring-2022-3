import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import numpy as np
from numpy import mean, loadtxt, std, argmax 
# load dataset
dataframe = pandas.read_csv("all_w_20000_labels.csv", header=None)
dataset = dataframe.values
X = dataset[:,0:12].astype(float)
Y = dataset[:,12]
# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

# define baseline model
def baseline_model():
 # create model
 model = Sequential()
 model.add(Dense(24, input_dim=12, activation='relu'))
 model.add(Dense(3, activation='softmax'))
 # Compile model
 model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
 return model
 
estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5) #can set verbose=0
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

# Accuracy after 2 batches is 0.53-0.54

# # serialize model to JSON
# model = baseline_model()
# model_json = model.to_json()
# with open("model_labels.json", "w") as json_file:
#     json_file.write(model_json)
# # serialize weights to HDF5
# model.save_weights("model_labels.h5")
# print("Saved model to disk")