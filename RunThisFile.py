from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np

# make data set
dataset = np.loadtxt("pima-indians-diabetes.csv", delimiter=",")
X = dataset[:,0:8]
Y = dataset[:,8]

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

for num in range(1,6) :
    # load weights into  model
    model.load_weights("model.h5")
    print("Loaded model from disk")

    # compile and run the model
    model.compile(loss='binary_crossentropy', optimizer='adagrad', metrics=['accuracy'])
    model.fit(X, Y, epochs=500, batch_size=50)

    # save weights to the file thing
    model.save_weights("model.h5")

    print("Saved weights to model.h5")
    print("End of run " + str(num))
