import base64
from io import BytesIO

import PIL.Image
import PIL.ImageOps
import numpy as np
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Flatten, Dropout
from keras.losses import categorical_crossentropy
from keras.models import Sequential
from keras.optimizers import Adam

IMAGE_SIZE = 28


class DigitPredictor:
    model_name = '3conv_128-256_2max'

    def __init__(self):
        model = Sequential()

        model.add(Conv2D(filters=128, kernel_size=(3, 3), input_shape=(28, 28, 1), activation='relu'))
        model.add(Conv2D(filters=256, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(filters=512, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(10, activation='softmax'))

        model.compile(loss=categorical_crossentropy,
                      optimizer=Adam(),
                      metrics=['accuracy'])

        model.load_weights('web/' + self.model_name + '_weights.h5')
        self.model = model

    def predict(self, image_array):
        """
        Predicts the decimal digit in the given image array.

        :param image_array: a (1,28,28,1) tensor for the Keras model to classify
        :return: a dictionary containing {'prediction': X, 'probabilities': [0,1...9]}
        """
        probabilities = self.model.predict(image_array, verbose=0)
        prediction = int(np.argmax(probabilities))
        return {'prediction': prediction, 'probabilities': probabilities.tolist()[0]}


def convert_canvas_image_to_array(image_data):
    """ Converts a base64 encoded canvas PNG to a 4D tensor for Keras """
    # Split the image data from the metadata
    split_str = b'base64,'
    index = image_data.find(split_str) + len(split_str)
    # Decode the image data from base64
    png_data = base64.b64decode(image_data[index:])
    # Create a PIL image from the bytes
    image = PIL.Image.open(BytesIO(png_data))
    # Resize image
    image = image.resize([IMAGE_SIZE, IMAGE_SIZE], PIL.Image.LANCZOS)
    # Reshape into a 4D numpy tensor
    pix = np.array(image, dtype='float32')
    pix = pix[..., 3]
    pix = pix.reshape(1, 28, 28, 1)
    # Normalize from [0-255] -> [0,1]
    pix /= 255
    return pix
