'''
Model_4 is a variant of model_1.
All are based on the cnn layer, but the face data is not considered in the feature extraction process.
'''

import tensorflow as tf
import keras
from keras import layers, Input, Sequential
import matplotlib.pyplot as plt
import ResNet
import ReadDatei


# draw statistical graph
def plot_hist(train, val, title):
    plt.plot(train)
    plt.plot(val)
    plt.title("model_1" + title)
    plt.ylabel(title)
    plt.xlabel("epoch")
    plt.legend(["train", "validation"], loc="upper left")
    plt.show()


# define hyperparameters
epochs = 100
learn_rate = 0.000005

# define network
# define input
input_tensor_eyebrow = layers.Input(shape=(224, 224, 1,))
input_tensor_eye = layers.Input(shape=(224, 224, 1,))
input_tensor_nose = layers.Input(shape=(224, 224, 1,))
input_tensor_mouth = layers.Input(shape=(224, 224, 1,))

# define cnn layer
eyebrow = ResNet.res_net(input_tensor_eyebrow)
eye = ResNet.res_net(input_tensor_eye)
nose = ResNet.res_net(input_tensor_nose)
mouth = ResNet.res_net(input_tensor_mouth)

# stitching matrix
new_tensor = keras.layers.concatenate((eyebrow, eye, nose, mouth), axis=-1)
new_tensor = layers.Flatten()(new_tensor)

# dense layer
dense_layer = layers.Dense(units=1000, kernel_initializer="he_normal")(new_tensor)
dense_layer = keras.layers.BatchNormalization()(dense_layer)
dense_layer = layers.Activation('relu')(dense_layer)

# output
opt_tensor = layers.Dense(units=7, activation=keras.activations.softmax)(dense_layer)

network = keras.Model([input_tensor_eyebrow, input_tensor_eye,
                       input_tensor_nose, input_tensor_mouth], opt_tensor)

# model
network.compile(
    optimizer=tf.optimizers.Adam(learning_rate=learn_rate),
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False), metrics=['accuracy']
)

# training
history = network.fit_generator(ReadDatei.read_datasets(50, "train_datas", 4), steps_per_epoch=630, epochs=epochs,
                                validation_data=ReadDatei.read_datasets(50, "val_datas", 4), validation_steps=70)

# result
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plot_hist(acc, val_acc, "accuracy")
plot_hist(loss, val_loss, "loss")





