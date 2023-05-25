# Train model and make predictions
import numpy
import pandas
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.utils import np_utils
from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

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

def build_model():
    # create model
    model = Sequential()
    model.add(Dense(50, input_dim=12, init='normal', activation='relu'))
    model.add(Dense(30, activation= 'relu'))
    model.add(Dense(3, init='normal', activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def save_model(model):
    # saving model
    json_model = model.to_json()
    open('model_wclass_v2.json', 'w').write(json_model)
    # saving weights
    model.save_weights('model_wclass_v2.h5', overwrite=True)

def load_model():
    # loading model
    model = model_from_json(open('model_wclass_v2.json').read())
    model.load_weights('model_wclass_v2.h5')
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.3, random_state=seed)

# build
model = build_model()
model.fit(X_train, Y_train, nb_epoch=200, batch_size=5) # can set verbose=0

# save
save_model(model)

#Switch metrics: https://keras.io/api/metrics/accuracy_metrics/#:~:text=Accuracy%20class&text=This%20metric%20creates%20two%20local,None%20%2C%20weights%20default%20to%201.

# # load
# model = load_model()

# # predictions
# predictions = model.predict_classes(X_test, verbose=0)
# print(predictions)
# # reverse encoding
# for pred in predictions:
#     print(labels[pred])

