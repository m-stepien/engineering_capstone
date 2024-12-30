import matplotlib.pyplot as plt
import numpy as np
from keras.api import preprocessing
from keras.src.legacy.backend import expand_dims
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras import layers, Input
from keras import models
import cv2
from keras.src.models import model


def train_model():
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    validation_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    train_generator = train_datagen.flow_from_directory(
        './images',
        target_size=(64, 64),
        batch_size=16,
        class_mode='categorical',
        classes=['50', '70', '100', 'null']
    )

    validation_generator = validation_datagen.flow_from_directory(
        './images/test',
        target_size=(64, 64),
        batch_size=16,
        class_mode='categorical',
        classes=['50', '70', '100', 'null']
    )

    model = models.Sequential([
        Input(shape=(64, 64, 3)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(4, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        epochs=60,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size
    )

    plt.plot(history.history['accuracy'], label='Dokładność treningowa')
    plt.plot(history.history['val_accuracy'], label='Dokładność walidacji')
    plt.xlabel('Epoki')
    plt.ylabel('Dokładność')
    plt.legend(loc='lower right')
    plt.show()

    model.save('traffic_sign_model.keras')




train_model()