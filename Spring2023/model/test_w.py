from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model, model_to_dot
import pydot
from keras import backend as K
import numpy
import os
import pandas as pd

# function from https://jmlb.github.io/ml/2017/03/20/CoeffDetermination_CustomMetric4Keras/
def r_squared(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

def get_dataset(df):
    # load the dataset
    dataset = df
    # split into input (X) and output (y) variables
    X = dataset.loc[:,'W1 min':'W6 max']
    X2 = dataset[['W1 min', 'W2 min', 'W3 min','W4 min', 'W5 min', 'W6 max']]
    y_1 = dataset.loc[:,'entangled':'xz_zx detect'] # for model 1
    y_2 = dataset.loc[:,'xy_yx detect':'xz_zx detect'] # for model 2
    return X, X2, y_1, y_2

def get_dataset_prob(dataset):
    # split into input (X) and output (y) variables
    X = dataset.loc[:,'HH probability':'LL probability']
    Y = dataset.loc[:,'xy_yx detect':'xz_zx detect']
    return X, Y

# //////////////////////////////EVALUATING MODELS////////////////////////////////////////////////////

# get test data
test_1 = 'test_states_1000.csv' 
test_df1 = pd.read_csv(test_1)
# test_df1 = test_df1.iloc[100:1000]

test_prob = 'all_prob_test.csv'
test_prob_df = pd.read_csv(test_prob)

test_w = 'all_w_test.csv'
test_w_df = pd.read_csv(test_w)

# test_2 = 'test_states_1000_2.csv'
# test_df2 = pd.read_csv(test_2)
# test_df2 = test_df2.iloc[100:1000]

# test_3 = 'test_states_1000_3.csv'
# test_df3 = pd.read_csv(test_3)
# test_df3 = test_df3.iloc[100:1000]

X, X2,y_1,y_2 = get_dataset(test_df1)
X_p, Y_p = get_dataset_prob(test_prob_df)
X_w, X2_w,y_1_w,y_2_w = get_dataset(test_w_df)
# X_2, X2_2, y_1_2, y_2_2 = get_dataset(test_df2)
# X_3, X2_3, y_1_3, y_2_3 = get_dataset(test_df3)


# #25,000 size
# # load json and create model
# json_file_10000 = open('model_60000.json', 'r')
# loaded_model_10000_json = json_file_10000.read()
# json_file_10000.close()
# loaded_model_10000 = model_from_json(loaded_model_10000_json)
# # load weights into new model
# loaded_model_10000.load_weights("model_60000.h5")
# print("Loaded model 60000 from disk")

# # evaluate loaded model on test data
# loaded_model_10000.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error', r_squared])

# score_7 = loaded_model_10000.evaluate(X, y_2)
# # score_7_2 = loaded_model_10000.evaluate(X_2, y_2_2)
# # score_7_3 = loaded_model3_v3.evaluate(X_3, y_2_3)

# print('\n\n\n for Model 60000 \n')
# print('For Test File 1 \n')
# print(score_7)
# print("%s: %.2f%%" % (loaded_model_10000.metrics_names[1], score_7[1]*100)) 
# print("%s: %.2f%%" % (loaded_model_10000.metrics_names[2], score_7[2]*100)) 

# model_w
json_file_10000 = open('model_prob.json', 'r')
loaded_model_10000_json = json_file_10000.read()
json_file_10000.close()
loaded_model_10000 = model_from_json(loaded_model_10000_json)
# load weights into new model
loaded_model_10000.load_weights("model_prob.h5")
print("Loaded model prob from disk")

# evaluate loaded model on test data
loaded_model_10000.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error', r_squared])

score_7 = loaded_model_10000.evaluate(X_p, Y_p)
# score_7_2 = loaded_model_10000.evaluate(X_2, y_2_2)
# score_7_3 = loaded_model3_v3.evaluate(X_3, y_2_3)

print('\n\n\n for Model Prob \n')
print('For Test File w \n')
print(score_7)
print("%s: %.2f%%" % (loaded_model_10000.metrics_names[1], score_7[1]*100)) 
print("%s: %.2f%%" % (loaded_model_10000.metrics_names[2], score_7[2]*100)) 


#///////////////////////////VISUALIZE MODELS//////////////////////////////
# model_to_dot(
#     loaded_model3_v3,
#     show_shapes=False,
#     show_dtype=False,
#     show_layer_names=True,
#     rankdir="TB",
#     expand_nested=False,
#     dpi=96,
#     subgraph=False,
#     layer_range=None,
#     show_layer_activations=False,
# )

# (graph, ) = pydot.graph_from_dot_file('model3v3.dot')
# graph.write_png('model3v3.png')
