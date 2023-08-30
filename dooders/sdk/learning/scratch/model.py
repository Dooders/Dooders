""" 
Modified code originally taken from "Neural Networks from Scratch" 
https://nnfs.io/
"""

import copy
import pickle
from typing import List

from dooders.sdk.learning.scratch.activation import (ACTIVATIONS,
                                                     Activation_Softmax)
from dooders.sdk.learning.scratch.eval import *
from dooders.sdk.learning.scratch.layer import *
from dooders.sdk.learning.scratch.loss import (
    LOSS, Activation_Softmax_Loss_CategoricalCrossentropy,
    Loss_CategoricalCrossentropy)
from dooders.sdk.learning.scratch.optimizer import *


class Model:
    """ 
    Model class for neural networks

    Attributes
    ----------
    layers : list
        List of network objects
    softmax_classifier_output : object
        Softmax classifier's output object
    loss : object
        Loss object
    optimizer : object
        Optimizer object
    accuracy : object
        Accuracy object
    input_layer : object
        Input layer object
    output_layer_activation : object
        Output layer activation object
    trainable_layers : list
        List of trainable layers

    Methods
    -------
    add(layer)
        Add objects to the model
    set(loss, optimizer, accuracy)
        Set loss, optimizer and accuracy
    finalize()
        Finalize the model
    train(X, y, epochs=1, print_every=1, validation_data=None)
        Train the model
    forward(X, training)
        Forward pass
    backward(output, y)
        Backward pass
    evaluate(X, y)
        Evaluate the model
    get_parameters()
        Get model parameters
    set_parameters(parameters)
        Set model parameters
    """

    def __init__(self) -> None:
        # Create a list of network objects
        self.layers = []
        # Softmax classifier's output object
        self.softmax_classifier_output = None

    def add(self, layer: object) -> None:
        """ 
        Add objects to the model

        Parameters
        ----------
        layer : object
            Object to add to the model
        """
        self.layers.append(layer)

    def set(self, *, loss: object, optimizer: object, accuracy: object) -> None:
        """ 
        Set loss, optimizer and accuracy

        """
        self.loss = loss
        self.optimizer = optimizer
        self.accuracy = accuracy

    def finalize(self) -> None:
        """ 
        Finalize the model
        """

        # Create and set the input layer
        self.input_layer = Layer_Input()

        # Count all the objects
        layer_count = len(self.layers)

        # Initialize a list containing trainable layers:
        self.trainable_layers = []

        # Iterate the objects
        for i in range(layer_count):

            # If it's the first layer,
            # the previous layer object is the input layer
            if i == 0:
                self.layers[i].prev = self.input_layer
                self.layers[i].next = self.layers[i+1]

            # All layers except for the first and the last
            elif i < layer_count - 1:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.layers[i+1]

            # The last layer - the next object is the loss
            # Also let's save aside the reference to the last object
            # whose output is the model's output
            else:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.loss
                self.output_layer_activation = self.layers[i]

            # If layer contains an attribute called "weights",
            # it's a trainable layer -
            # add it to the list of trainable layers
            # We don't need to check for biases -
            # checking for weights is enough
            if hasattr(self.layers[i], 'weights') and self.layers[i].frozen == False:
                self.trainable_layers.append(self.layers[i])

        # Update loss object with trainable layers
        self.loss.remember_trainable_layers(
            self.trainable_layers
        )

        # If output activation is Softmax and
        # loss function is Categorical Cross-Entropy
        # create an object of combined activation
        # and loss function containing
        # faster gradient calculation
        if isinstance(self.layers[-1], Activation_Softmax) and \
           isinstance(self.loss, Loss_CategoricalCrossentropy):
            # Create an object of combined activation
            # and loss functions
            self.softmax_classifier_output = \
                Activation_Softmax_Loss_CategoricalCrossentropy()

    def train(self,
              X: np.ndarray,
              y: np.ndarray,
              *,
              epochs: int = 1,
              print_every: int = 1,
              validation_data: tuple = None) -> None:
        """ 
        Train the model

        Parameters
        ----------
        X : array
            Input data
        y : array
            Target data
        epochs : int
            Number of epochs
        print_every : int
            Print every
        validation_data : tuple
            Validation data
        """

        # Initialize accuracy object
        self.accuracy.init(y)

        # Main training loop
        for epoch in range(1, epochs+1):

            # Perform the forward pass
            output = self.forward(X, training=True)

            # Calculate loss
            data_loss, regularization_loss = \
                self.loss.calculate(output, y,
                                    include_regularization=True)
            loss = data_loss + regularization_loss

            # Get predictions and calculate an accuracy
            predictions = self.output_layer_activation.predictions(
                output)
            accuracy = self.accuracy.calculate(predictions, y)

            # Perform backward pass
            self.backward(output, y)

            # Optimize (update parameters)
            self.optimizer.pre_update_params()
            for layer in self.trainable_layers:
                self.optimizer.update_params(layer)
            self.optimizer.post_update_params()

            # Print a summary
            if not epoch % print_every:
                print(f'epoch: {epoch}, ' +
                      f'acc: {accuracy:.3f}, ' +
                      f'loss: {loss:.3f} (' +
                      f'data_loss: {data_loss:.3f}, ' +
                      f'reg_loss: {regularization_loss:.3f}), ' +
                      f'lr: {self.optimizer.current_learning_rate}')

        # If there is the validation data
        if validation_data is not None:

            # For better readability
            X_val, y_val = validation_data

            # Perform the forward pass
            output = self.forward(X_val, training=False)

            # Calculate the loss
            loss = self.loss.calculate(output, y_val)

            # Get predictions and calculate an accuracy
            predictions = self.output_layer_activation.predictions(
                output)
            accuracy = self.accuracy.calculate(predictions, y_val)

            # Print a summary
            print(f'validation, ' +
                  f'acc: {accuracy:.3f}, ' +
                  f'loss: {loss:.3f}')

    def forward(self, X: np.ndarray, training: bool) -> np.ndarray:
        """ 
        Performs forward pass

        Parameters
        ----------
        X : array
            Input data
        training : bool
            Whether in training mode or not

        Returns
        -------
        array
            Output data
        """

        # Call forward method on the input layer
        # this will set the output property that
        # the first layer in "prev" object is expecting
        self.input_layer.forward(X, training)

        # Call forward method of every object in a chain
        # Pass output of the previous object as a parameter
        for layer in self.layers:
            layer.forward(layer.prev.output, training)

        # "layer" is now the last object from the list,
        # return its output
        return layer.output

    def backward(self, output: np.ndarray, y: np.ndarray) -> None:
        """ 
        Performs backward pass

        Parameters
        ----------
        output : array
            Output of the forward pass
        y : array
            Target data
        """
        # If softmax classifier
        if self.softmax_classifier_output is not None:
            # First call backward method
            # on the combined activation/loss
            # this will set dinputs property
            self.softmax_classifier_output.backward(output, y)

            # Since we'll not call backward method of the last layer
            # which is Softmax activation
            # as we used combined activation/loss
            # object, let's set dinputs in this object
            self.layers[-1].dinputs = \
                self.softmax_classifier_output.dinputs

            # Call backward method going through
            # all the objects but last
            # in reversed order passing dinputs as a parameter
            for layer in reversed(self.layers[:-1]):
                layer.backward(layer.next.dinputs)

            return
        # First call backward method on the loss
        # this will set dinputs property that the last
        # layer will try to access shortly
        self.loss.backward(output, y)
        # Call backward method going through all the objects
        # in reversed order passing dinputs as a parameter
        for layer in reversed(self.layers):
            layer.backward(layer.next.dinputs)

    # Saves the model
    def save(self, path):

        # Make a deep copy of current model instance
        model = copy.deepcopy(self)

        # Reset accumulated values in loss and accuracy objects
        model.loss.new_pass()
        model.accuracy.new_pass()

        # Remove data from the input layer
        # and gradients from the loss object
        model.input_layer.__dict__.pop('output', None)
        model.loss.__dict__.pop('dinputs', None)

        # For each layer remove inputs, output and dinputs properties
        for layer in model.layers:
            for property in ['inputs', 'output', 'dinputs',
                             'dweights', 'dbiases']:
                layer.__dict__.pop(property, None)

        # Open a file in the binary-write mode and save the model
        with open(path, 'wb') as f:
            pickle.dump(model, f)


class SimpleNeuralNet:
    """ 
    A simple neural network with 2 hidden layers

    Attributes
    ----------
    model : Model
        The model

    Methods
    -------
    predict(input_array: np.ndarray) -> int
        Predict the class of the input data
    """

    #! make better debugging in general to debug problems
    #! make data types so I can better identify data in flight
    def __init__(self, id: str, instructions: dict) -> None:
        """ 
        Initialize the model
        """
        self.id = id
        self.purpose = instructions['model_purpose']

        for key in instructions:
            setattr(self, key, instructions[key])

        self.build()

    def build(self) -> None:
        self.model = Model()
        self.model.add(Layer_Dense(self.input_size, 512, frozen=True))
        self.model.add(ACTIVATIONS.get('relu')())
        self.model.add(Layer_Dense(512, self.output_size))
        self.model.add(ACTIVATIONS.get(self.activation_type)())
        self.model.set(
            loss=LOSS.get(self.loss_type)(),
            optimizer=Optimizer_Adam(decay=5e-7),
            accuracy=Accuracy_Categorical()
        )
        self.model.finalize()

    def predict(self, input_array: np.ndarray) -> int:
        """ 
        Predict the class of the input data

        Parameters
        ----------
        input_array : array
            The input data

        Returns
        -------
        int
            The class of the input data
        """
        self.input = input_array

        self.output = self.model.forward(input_array, training=False)
        self.prediction = self.model.output_layer_activation.predictions(
            self.output)

        return self.output

    def learn(self, reality: list) -> None:
        """ 
        Learn from the reality

        Parameters
        ----------
        reality : list
            The reality (truth)
        """
        self.reality = reality
        reality_array = np.array(self.reality)

        if len(reality_array) == 0:
            pass  # nothing to learn
        else:
            # Optimize parameters
            self.model.backward(self.output, reality_array)
            self.model.optimizer.pre_update_params()
            for layer in self.model.trainable_layers:
                self.model.optimizer.update_params(layer)
            self.model.optimizer.post_update_params()

    def inherit_weights(self, genetics: List[np.ndarray]) -> None:
        """ 
        Update the weights based on provided derived genetics
        from parent Dooders

        Parameters
        ----------
        genetics : List[np.ndarray]
            The weights of the neural network
        """
        self.model.layers[0].weights = genetics[0]
        self.model.layers[2].weights = genetics[1]

    def save(self, path: str) -> None:
        """ 
        Save the model

        Parameters
        ----------
        path : str
            The path to save the model
        """
        np.save(path, np.array(self.weights, dtype=object))

    def save_weights(self, cycle_number: int) -> None:
        """ 
        Save the weights of the neural network from every dense layer

        Parameters
        ----------
        cycle_number : int
        """
        file_name = f"recent/dooders/model_{self.id}_{cycle_number}_{self.purpose}.npy"
        np.save(file_name, np.array(self.weights, dtype=object))

    def load_weights(self, weights_to_load: str) -> None:
        """ 
        Load the model

        Parameters
        ----------
        weights_to_load : str
            The filename for the weights to load i.e. "model_xyz123_1_Movement"
        """
        loaded_weights = np.load(
            f"recent/dooders/{weights_to_load}.npy", allow_pickle=True)
        self.inherit_weights(loaded_weights)

    @property
    def layers(self) -> list:
        """ 
        Get the layers of the neural network

        Returns
        -------
        list
            The layers of the neural network
        """
        return self.model.layers

    @property
    def weights(self) -> np.ndarray:
        """ 
        Get the weights of the neural network from every dense layer

        Returns
        -------
        np.ndarray
            The weights of the neural network
        """
        weights = []
        for layer in self.model.layers:
            if isinstance(layer, Layer_Dense):
                weights.append(layer.weights)
        return np.array(weights, dtype=object)
