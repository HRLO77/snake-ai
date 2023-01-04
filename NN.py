# applies a neural network to q-table
# reset cmd
# python -c "import pickle;f=open('qtable.pickle', 'wb');pickle.dump({}, f);f.close()"
from keras.models import load_model
from keras import Sequential, layers, losses, optimizers, callbacks, metrics
import numpy as np
from matplotlib import pyplot as plt
import pickle as pk
print('Unpickling data...')
with open('./qtable.pickle', 'rb') as f:data=pk.load(f)
print('Processing...')

x = np.array([[*i[:2]] + np.array(i[2], dtype=np.int8).flatten().tolist() for i in data.keys()], dtype=np.int16)
y = np.array([np.argmax(i) for i in data.values()], dtype=np.int16)


NN = Sequential(
    (
        layers.InputLayer(input_shape=(x.shape[1:])),
        layers.Dense(64, activation='relu',),
        layers.Dense(len((set(y))), activation='softmax')
    ), name='snake-NN'
    
)
print('Compiling...')
NN.compile('adamax', losses.SparseCategoricalCrossentropy(True), jit_compile=True, metrics=['acc', ], )
history: callbacks.History = NN.fit(x, y, epochs=50)
NN.save(f'./{NN.name}')
loss = history.history['loss']
accuracy = history.history['acc']
plt.title('Neural Network training')
plt.xlabel('Epoch')
plt.ylabel('Performace')
plt.plot(loss, color='red')
plt.plot(accuracy, color='green')
plt.show()