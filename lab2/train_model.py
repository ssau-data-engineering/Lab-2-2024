import tensorflow as tf
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D, Activation
from keras.optimizers import Adam
from keras.callbacks import LambdaCallback
import numpy as np
import logging


def log_loss(epoch, logs):
    with open('/data/loss_log.txt', 'a') as file:
        file.write(f"Epoch {epoch}: loss = {logs['loss']}\n")

loss_logger = LambdaCallback(on_epoch_end=log_loss)

def create_model(input_shape):

    inputs = Input(shape=input_shape)

    x = Conv2D(16, kernel_size=(3, 3), padding='same')(inputs)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    
    x = Conv2D(32, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    
    x = Conv2D(32, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    
    x = Conv2D(32, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Flatten()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.4)(x)
    
    outputs = Dense(input_shape[0]*input_shape[1], activation='linear')(x)
    outputs = tf.keras.layers.Reshape((input_shape[0], input_shape[1]))(outputs)

    model = Model(inputs=inputs, outputs=outputs)
    return model


def loss_function(y_true, y_pred):
    return tf.cast(1 / tf.shape(y_true)[0], tf.float32) * 0.5 * tf.reduce_sum(tf.math.pow(y_true - y_pred, 2))


def error_rate(y_true, y_pred):
    num = tf.reduce_sum(tf.math.abs(y_pred - y_true), axis=[1, 2])
    denom = tf.reduce_sum(tf.math.abs(y_true), axis=[1, 2])
    per_image = (tf.cast(100 / (tf.shape(y_true)[1] * tf.shape(y_true)[2]), tf.float32) * num / denom)
    return tf.reduce_mean(per_image)


model = create_model((256, 256, 1))
model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss=loss_function,
)


x_train = np.load('/data/x_train.npy')
y_train = np.load('/data/y_train.npy')
x_val = np.load('/data/x_val.npy')
y_val = np.load('/data/y_val.npy')

model.fit(x_train,
          y_train,
          validation_data=(x_val, y_val),
          epochs=50,
          callbacks=[loss_logger]
        )

model.save('/data/trained_model.keras')