import numpy as np
from matplotlib import pyplot as plt
def sigmoid(x):
    return 1 / (1 + np.exp(-1 * x))

def softmax(x):
    return(np.exp(x)/np.exp(x).sum())

def ReLU(x: np.ndarray):
    return np.maximum(0, x)
ALPHA = 0.25

def elu(x: np.ndarray):
    if x.any() < 0: return ALPHA * (np.exp(x) - 1)
    else: return x
    
class DenseLayer:
    """
    Layers of BP neural network
    """

    def __init__(
        self, units, activation=None, learning_rate=None, is_input_layer=False
    ):
        """
        common connected layer of bp network
        :param units: numbers of neural units
        :param activation: activation function
        :param learning_rate: learning rate for paras
        :param is_input_layer: whether it is input layer or not
        """
        self.units = units
        self.weight = None
        self.bias = None
        self.activation = activation
        if learning_rate is None:
            learning_rate = 0.3
        self.learn_rate = learning_rate
        self.is_input_layer = is_input_layer

    def initializer(self, back_units):
        self.weight = np.asmatrix(np.random.normal(0, 0.5, (self.units, back_units)))
        self.bias = np.asmatrix(np.random.normal(0, 0.5, self.units)).T
        if self.activation is None:
            self.activation = sigmoid

    def cal_gradient(self):
        # activation function may be sigmoid or linear
        if self.activation == sigmoid:
            gradient_mat = np.dot(self.output, (1 - self.output).T)
            gradient_activation = np.diag(np.diag(gradient_mat))
        else:
            gradient_activation = 1
        return gradient_activation

    def forward_propagation(self, xdata):
        self.xdata = xdata
        if self.is_input_layer:
            # input layer
            self.wx_plus_b = xdata
            self.output = xdata
            return xdata
        else:
            self.wx_plus_b = np.dot(self.weight, self.xdata) - self.bias
            self.output = self.activation(self.wx_plus_b)
            return self.output

    def back_propagation(self, gradient):
        gradient_activation = self.cal_gradient()  # i * i 维
        gradient = np.asmatrix(np.dot(gradient.T, gradient_activation))

        self._gradient_weight = np.asmatrix(self.xdata)
        self._gradient_bias = -1
        self._gradient_x = self.weight

        self.gradient_weight = np.dot(gradient.T, self._gradient_weight.T)
        self.gradient_bias = gradient * self._gradient_bias
        self.gradient = np.dot(gradient, self._gradient_x).T
        # upgrade: the Negative gradient direction
        self.weight = self.weight - self.learn_rate * self.gradient_weight
        self.bias = self.bias - self.learn_rate * self.gradient_bias.T
        # updates the weights and bias according to learning rate (0.3 if undefined)
        return self.gradient


class BPNN:
    """
    Back Propagation Neural Network model
    """

    def __init__(self, activation=elu):
        self.activation = activation
        self.layers = []
        self.train_huber = []
        self.fig_loss = plt.figure()
        self.ax_loss = self.fig_loss.add_subplot(1, 1, 1)

    def add_layer(self, layer):
        self.layers.append(layer)

    def build(self):
        for i, layer in enumerate(self.layers[:]):
            if i < 1:
                layer.is_input_layer = True
            else:
                layer.initializer(self.layers[i - 1].units)

    def summary(self):
        for i, layer in enumerate(self.layers[:]):
            print(f"------- layer {i} -------")
            print("weight.shape ", np.shape(layer.weight))
            print("bias.shape ", np.shape(layer.bias))

    def train(self, xdata, ydata, epochs, accuracy):
        self.epochs = epochs
        self.accuracy = accuracy

        self.ax_loss.hlines(self.accuracy, 0, self.epochs * 1.1)

        x_shape = np.shape(xdata)
        for _ in range(epochs):
            
            all_loss = 0
            for row in range(x_shape[0]):
                _xdata = np.asmatrix(xdata[row, :]).T
                _ydata = np.asmatrix(ydata[row, :]).T

                # forward propagation
                for layer in self.layers:
                    _xdata = layer.forward_propagation(_xdata)

                loss, gradient = self.cal_loss(_ydata, _xdata)

                # back propagation: the input_layer does not upgrade
                for layer in self.layers[:0:-1]:
                    gradient = layer.back_propagation(gradient)
            mae = loss
            self.train_huber.append(mae)
            self.plot_loss()
            print(f'Epoch {_} - loss: {mae} - alpha: {ALPHA}')
            if mae < self.accuracy:
                print("----达到精度----")
                return mae
    def cal_loss(self, ydata, xdata):
        # print(ydata, xdata)
        self.loss = np.mean(np.abs(xdata - ydata))
        self.loss_gradient = self.activation(xdata - ydata)
        # vector (shape is the same as _ydata.shape)
        return self.loss.tolist(), self.loss_gradient

    def plot_loss(self):
        if self.ax_loss.lines:
            self.ax_loss.lines.remove(self.ax_loss.lines[0])
        self.ax_loss.plot(self.train_huber, "r-")
        plt.ion()
        plt.xlabel("step")
        plt.ylabel("loss")
        plt.show()
        plt.pause(0.1)


    
def example():
    x = []
    y = []
    tosort = []
    for i in range(5):
        for i in range(4):
            tosort.append(i)
    import collections
    for i in range(10000):
        np.random.shuffle(tosort)
        x += [tosort[:5]]
        c = collections.Counter(tosort[:5])
        y += [[c.most_common()[0][0]]]
    
    x = np.array(x)
    y = np.asmatrix(y)
    model = BPNN(elu)
    for i in (5, 5, 5, 4):
        model.add_layer(DenseLayer(i, elu, 0.001))
    model.build()
    model.summary()
    model.train(xdata=x, ydata=y, epochs=100, accuracy=0.1)

example()