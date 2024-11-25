from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D, Activation
from keras.optimizers import Adam
from keras.callbacks import LambdaCallback
import pandas as pd
import numpy as np

# Логирование потерь
def log_loss(epoch, logs):
    with open('mnist_loss_log.txt', 'a') as file:
        file.write(f"Epoch {epoch}: loss = {logs['loss']}, val_loss = {logs['val_loss']}/n")

loss_logger = LambdaCallback(on_epoch_end=log_loss)

# Создание модели
def create_mnist_model(input_shape):
    inputs = Input(shape=input_shape)

    x = Conv2D(32, kernel_size=(3, 3), padding='same')(inputs)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(64, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(128, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(10, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=outputs)
    return model

# Загрузка данных
X_train = pd.read_csv('C:/Users/Dekart/Desktop/Универ/6233 - первый сезон/6. Инженерия данных/Labs/Prerequisites/airflow/data/X_train.csv').to_numpy().astype('float32')
X_test = pd.read_csv('C:/Users/Dekart/Desktop/Универ/6233 - первый сезон/6. Инженерия данных/Labs/Prerequisites/airflow/data/X_test.csv').to_numpy().astype('float32')
y_train = pd.read_csv('C:/Users/Dekart/Desktop/Универ/6233 - первый сезон/6. Инженерия данных/Labs/Prerequisites/airflow/data/y_train.csv').to_numpy().astype('float32')
y_test = pd.read_csv('C:/Users/Dekart/Desktop/Универ/6233 - первый сезон/6. Инженерия данных/Labs/Prerequisites/airflow/data/y_test.csv').to_numpy().astype('float32')

# Преобразование входных данных в формат с каналом
X_train = np.expand_dims(X_train.reshape(-1, 28, 28), axis=-1)
X_test = np.expand_dims(X_test.reshape(-1, 28, 28), axis=-1)

# Создание модели
model = create_mnist_model((28, 28, 1))

# Компиляция модели
model.compile(
    optimizer=Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Обучение модели
model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=10,
    batch_size=128,
    callbacks=[loss_logger]
)

# Сохранение модели
model.save('C:/Users/Dekart/Desktop/Универ/6233 - первый сезон/6. Инженерия данных/Labs/Prerequisites/airflow/data/new_mnist_trained_model.keras', save_format='tf')