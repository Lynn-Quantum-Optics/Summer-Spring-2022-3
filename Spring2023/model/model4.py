# mlp for multi-output regression
import numpy as np
from numpy import mean, loadtxt, std, argmax
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

"""
This code is heavily based on Jason Brownless's tutorial linked below
https://machinelearningmastery.com/deep-learning-models-for-multi-output-regression/#:~:text=Multi%2Doutput%20regression%20is%20a,a%20prediction%20for%20new%20data.
"""

"""
using same architecture of CNN as Roik
"""

def r_squared(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

# # split the dataset into a training set and a validation set
# train_df, val_df = train_test_split(df, test_size=0.05)

def get_dataset(dataset):
    # split into input (X) and output (y) variables
    X = dataset[['W1 min', 'W2 min', 'W3 min','W4 min', 'W5 min', 'W6 max']]
    y = dataset.loc[:,'xy_yx detect':'xz_zx detect']
    return X, y

# get the model, in this case there n_inputs = 12, n_outputs = 3
def get_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(200, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(150, activation = 'relu'))
    model.add(Dense(n_outputs))
    model.compile(loss='mae', optimizer='adam')
    return model

"""
Using k-fold cross-validation is especially useful for smaller datasets, 
this is a pretty big dataset but this technique can still be pretty useful
"""
# evaluate a model using repeated k-fold cross-validation
def evaluate_model(X, y):
    results = list()
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    # define evaluation procedure
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # enumerate folds

    for train_idx, test_idx in cv.split(X):
        # prepare data
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        # define model
        model = get_model(n_inputs, n_outputs)
        # fit model
        model.fit(X_train, y_train, verbose=0, epochs=100)
        # evaluate model on test set
        mae = model.evaluate(X_test, y_test)
        # store result
        print('>%.3f' % mae)
        results.append(mae)
    return results


"""
The data files contains 10,000 randomly generated states 
with the values for W1-W6 min and max and whether or not 
it is detected by one of the triplet prime witnesses
"""

data_1 = 'all_states.csv'
data_2 = 'all_states_2.csv'
# data_3 = 'all_states_3.csv'

df1 = pd.read_csv(data_1)
df2 = pd.read_csv(data_2)
# df3 = pd.read_csv(data_3)
df = pd.concat([df1, df2])

#load dataset
X, y = get_dataset(df)
# evaluate model
# results = evaluate_model(X, y)
# # summarize performance
# print('MAE: %.3f (%.3f)' % (mean(results), std(results)))
# results on 50,000 dataset 
# MAE: 

# Compile model
model = get_model(6,3)
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error', r_squared])

# Fit the model
model.fit(X, y, epochs=150, batch_size=30)

# evaluate the model
scores = model.evaluate(X, y, verbose=0)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
print("%s: %.2f%%" % (model.metrics_names[2], scores[2]*100))
# mean squared error: 0.1031
# R^2: 0.3762

# serialize model to JSON
model_json = model.to_json()
with open("model4.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model4.h5")
print("Saved model to disk")