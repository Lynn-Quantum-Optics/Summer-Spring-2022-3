from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense
import numpy as np

"""
w_val is a list of witness values with 12 entries
format: w_val = [w1_min, w1_max, w2_min, w2_max, 
                w3_min, w3_max, w4_min, w4_max, 
                w5_min, w5_max, w6_min, w6_max]
prints a list that has the format as follows 
pred_y = [xy_yx detect, yz_zy detect, xz_zx detect]
also prints statements that interpret list for you
"""

# TODO: CHANGE ACCORDINGLY TO WHICH MODEL PERFORMS THE BEST
# load json and create model
json_file = open('model3v3.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model3v3.h5")
print("Loaded model from disk")

def get_predictions(w_val):
    # make a prediction for new data
    newX = np.asarray([w_val])
    new_y = loaded_model.predict(newX)
    max_idx = np.argmax(new_y, axis=1)
    pred_y = new_y #round to the nearest int to get boolean values
    print('\n\n Predicted: %s' % new_y[0], '\n\n')

    if pred_y[0][max_idx] == 0:
        print('the state is probably not detectable by the prime witnesses')
        print('should do a full tomography')
    else:
        if max_idx == 0:
            print('most likely detected by the xy_yx triplet\n')
            print('make more measurements in the following bases:\n')
            print('DR', 'DL', 'AR', 'AL', 'RD', 'RA', 'LD', 'LA')
        elif max_idx == 1:
            print('most likely detected by the yz_zy triplet\n')
            print('make more measurements in the following bases:\n')
            print('RH', 'RV', 'LH', 'LV', 'HR', 'HL', 'VR', 'VL')
        else:
            print('most likely detected by the xz_zx triplet\n')
            print('make more measurements in the following bases:\n')
            print('DH', 'DV', 'AH', 'AV', 'HD', 'HA', 'VD', 'VA')