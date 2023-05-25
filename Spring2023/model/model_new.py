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
from tensorflow import keras
import tensorflow as tf

"""
This code is heavily based on Jason Brownless's tutorial linked below
https://machinelearningmastery.com/deep-learning-models-for-multi-output-regression/#:~:text=Multi%2Doutput%20regression%20is%20a,a%20prediction%20for%20new%20data.

Tutorial to create custom loss function: 
https://towardsdatascience.com/how-to-create-a-custom-loss-function-keras-3a89156ec69b 
https://cnvrg.io/keras-custom-loss-functions/

https://stackoverflow.com/questions/35146444/tensorflow-python-accessing-individual-elements-in-a-tensor 
https://www.tensorflow.org/guide/tensor
https://towardsdatascience.com/how-to-replace-values-by-index-in-a-tensor-with-tensorflow-2-0-510994fe6c5f 
https://neptune.ai/blog/keras-loss-functions
https://www.kdnuggets.com/2019/04/advanced-keras-constructing-complex-custom-losses-metrics.html
https://towardsdatascience.com/cross-entropy-loss-function-f38c4ec8643e
https://www.dlology.com/blog/how-to-multi-task-learning-with-missing-labels-in-keras/ 
https://blog.manash.io/multi-task-learning-in-keras-implementation-of-multi-task-classification-loss-f1d42da5c3f6 

"""

"""
using same architecture of CNN as Roik
"""

def r_squared(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

def witness_loss_fn(y_true, y_pred):
    # y_pred is a 1 by batch size tensor with all the predicted values for each state
    # y_true is a 3 by batch size tensor, with the three ground truth outputs per state
    """
    How to make this loss function differentiable?
    Currently, this loss function cannot have an associated gradient, can we use categorial cross entropy?
    """
    print(y_true)
    print(y_true.shape)
    print("before slice", y_pred)
    batchsize = y_true.shape[0]
    
    # making y_pred 1 output when evaluating loss
    y_pred = tf.slice(y_pred, [0, 0], [batchsize, 1])# 0
    print("after slice", y_pred)

    # for y_true, getting labels
    # label_1 = y_true.loc[:, 'label_1']
    label_1 = tf.slice(y_true, [0, 0], [batchsize, 1] )
    print("label_1 shape", label_1.shape)
    # label_2 = y_true.loc[:, 'label_2']
    label_2 = tf.slice(y_true, [0, 1], [batchsize, 1] )
    print("label_2 shape", label_2.shape)
    # label_3 = y_true[:, 'label_3']
    label_3 = tf.slice(y_true, [0, 2], [batchsize, 1] )
    print("label_3 shape", label_3.shape)

    losses = []
    for i in range(batchsize):
        # weighting losses
        if str(y_pred[i]) == str(label_1[i]):
            loss = [0]
        elif str(y_pred[i]) != "EMPTY" and str(y_pred[i]) == str(label_2[i]):
            loss = [0.5]
        elif str(y_pred[i]) != "EMPTY" and str(y_pred[i]) == str(label_3[i]):
            loss = [0.7]
        else:
            loss = 1
        losses += [[loss]]

    losses = np.array(losses)
    print(losses)
    print(losses.shape)
    losses = tf.convert_to_tensor(losses, dtype= tf.float32)
    # must return an array of losses
    print(losses)
    print("type losses", type(losses))
    return losses
    # labelL = [label_1, label_2, label_3]
    # https://keras.io/api/losses/
    

    # for a binary approach with no notion of "best" 
    # if y_true in labelL & (y_true != "EMPTY"):
    #    return True 
   


# # split the dataset into a training set and a validation set
# train_df, val_df = train_test_split(df, test_size=0.05)

def get_dataset(dataset):
    # split into input (X) and output (y) variables
    X = dataset.loc[:,'HH probability':'LL probability']
    y = dataset.loc[:,'label_1': 'label_3']
    return X, y

# get the model, in this case there n_inputs = 12, n_outputs = 3
def get_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(20, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(15, activation = 'relu'))
    model.add(Dense(n_outputs))
    opt = keras.optimizers.Adam(clipnorm=1.0)
    model.compile(loss='witness_loss_fn', optimizer=opt)
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


# """
# The data files contains 10,000 randomly generated states 
# with the values for W1-W6 min and max and whether or not 
# it is detected by one of the triplet prime witnesses
# """

data_1 = 'all_prob_20000_1.csv'


df = pd.read_csv(data_1)


#load dataset
X, y = get_dataset(df)
# evaluate model
# results = evaluate_model(X, y)
# # # summarize performance
# # print('MAE: %.3f (%.3f)' % (mean(results), std(results)))
# # results on 50,000 dataset 
# # MAE: 



# # Compile model
opt = keras.optimizers.Adam(clipnorm=1.0)
model = get_model(12,3)
model.compile(loss=witness_loss_fn, optimizer=opt, metrics=[witness_loss_fn])


# Fit the model
model.fit(X, y, epochs=150, batch_size=50)

# # evaluate the model
scores = model.evaluate(X, y, verbose=0)
# print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
# print("%s: %.2f%%" % (model.metrics_names[2], scores[2]*100))
# # mean squared error: 4.32%
# # R^2: 73.29%

# # serialize model to JSON
# model_json = model.to_json()
# with open("model_new.json", "w") as json_file:
#     json_file.write(model_json)
# # serialize weights to HDF5
# model.save_weights("model_new.h5")
# print("Saved model to disk")