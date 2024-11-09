from tensorflow import keras
from keras import Sequential
from keras.layers import \
Dense, Conv2D, MaxPooling2D, Flatten, \
RandomFlip, RandomRotation, Resizing, \
Rescaling, BatchNormalization
from keras.callbacks import LambdaCallback

BATCH_SIZE = 32
IMG_W = 256
IMG_H = 256
EPOCH = 20
CHANNEL = 3

INPUT_SHAPE = [BATCH_SIZE, IMG_W, IMG_H, CHANNEL]

def log_loss(epoch, logs):
    with open('/data/loss.txt', 'a') as file:
        file.write(f"ep {epoch}, loss {logs['loss']}\n")

def create_model(n_classes):

    augmentation = Sequential([
        Resizing(IMG_W, IMG_H),
        Rescaling(1.0/255),
        RandomFlip(mode="horizontal_and_vertical"),
        RandomRotation(0.1),
    ])

    model = keras.models.Sequential([
        augmentation,

        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=INPUT_SHAPE),
        MaxPooling2D((2, 2)),
        BatchNormalization(),

        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        BatchNormalization(),

        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        BatchNormalization(),

        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        BatchNormalization(),

        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        BatchNormalization(),

        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        BatchNormalization(),

        Flatten(),

        Dense(64, activation='relu'),

        Dense(n_classes, activation='softmax')
    ])

    return model


train_data = keras.utils.image_dataset_from_directory('/data/train')
val_data = keras.utils.image_dataset_from_directory('/data/validation')
test_data = keras.utils.image_dataset_from_directory('/data/test')

classes = train_data.class_names

model = create_model(len(classes))
model.build(input_shape=INPUT_SHAPE)
model.compile(
optimizer= 'adam',
loss= keras.losses.SparseCategoricalCrossentropy(from_logits=False),
metrics= ['accuracy']
)

loss_logger = LambdaCallback(on_epoch_end=log_loss)
model.fit(train_data,
          epochs=EPOCH,
          batch_size=BATCH_SIZE,
          verbose=1,
          validation_data=val_data,
          callbacks=[loss_logger])

model.save('/data/model.keras')