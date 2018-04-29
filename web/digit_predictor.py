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
        predictions = self.model.predict(image_array, verbose=0)
        return np.argmax(predictions)

def convert_base64_image(image_data):
    """ Converts a base64 encoded PNG to a 4D tensor """
    # Split the image string and decode from base64
    split_str = b'base64,'
    index = image_data.find(split_str) + len(split_str)
    png_data = base64.b64decode(image_data[index:])
    # Resize image
    image = PIL.Image.open(BytesIO(png_data))
    image = image.resize([IMAGE_SIZE, IMAGE_SIZE], PIL.Image.LANCZOS)
    # Reshape into a 4D numpy tensor
    pix = np.array(image, dtype='float32')
    pix = pix[..., 3]
    pix = pix.reshape(1, 28, 28, 1)
    # Normalize from [0-255] -> [0,1]
    pix /= 255
    return pix


if __name__ == '__main__':
    model = DigitPredictor()
    img = b'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAM8UlEQVR4Xu2dy89eVRWHf9yUYgEdIIlxopFgDIEYEiVVsF5iNcbohJFIVAQcSP8Bw8REx06MoSgOMA4aJjoyamzFKzo0YtIWNSbGcgkSQEFRMas9X9p+3/u+Z53znr3PWXs9Z9a+6+zLs9bv22ffL9Le56ikA5KulnSppJclPSfpkKQTK+z5Lwg0S+CiXTU7LuldkvatqPFpSbdJOtksDSoGgV0EzhfIEUl3rBHHzmvWmqwSD2Ah0CSBHYG8VtIzkvb31PJfkg5LMjHxQKB5AjsCebekH0m60lHj70r6lMMOEwiEJ7AjEOt3/NgpkIck3RW+5lQAAg4COwJ5TfeJ1deC2CfWw5Je7Ua5fi3pa92/HdlhAoFYBM7vpH9D0mckXb6hCiaM/0m6pLOxf/9X0sck/TBW1SktBPoJ7B7m/YmkW9aMVJkwLl6TpInkI91nWn+uWEAgCIHdArFiWyf8oKSrupbCPqtsaNc+w/qeVen1vcPvEFgsgXUBfZOkGzuRnJL0A2cNviPp005bzCCweAKev/ifk/QtZ03+LOktTlvMILB4Ah6BWMf9286a2Fqt6522mEFg8QQ8AnmdpBedNbEh4DudtphBYPEEPAKxSvxe0jsctfGm50gKEwjMT2BIQD8r6Q1rimxDwB+Q9NP5q0QJIDAdgSECsVytE/7m8yYK7f/+3c2BHJuuWKQEgWUQGCoQK/Xtkj4o6fWSfi7p6yw1WYYzKcX0BMYIZKpS2N4T24BlOxdZ0zUVVdKZlMBcAvmLpDexpmtSX5JYAQJzCOTv3efZquqwpquAk0lyPIHaAvmDpLc7ilu7XI4iYZKRQM1AtL0mzzshs6bLCQqzsgRqCoQ1XWV9SeoFCNQUCGu6CjiQJMsSqCkQ1nSV9SWpFyBQUyBW/CWs6WL+pUAgtZpkbYEYxznXdDH/0mokF6rXHAKxqsyxpov5l0JB1HKycwnEmNZc08X8S8tRXLBucwqkYLUuSJr5l1qkG8wng0DukfSA03d2PvE1TlvMEhDIIJAvS7rf6Uub6bfVxTwQOEMgg0Bs74qdO+x5npJ0rccQmxwEMgjkPd3GLo9HH+tOlvTYYpOAQAaB2Mn1tvPxMoc/H+lG1xymmGQgkEEg3pPrzd+vOI9YzRAb1DFJH8QcbaNYNprV93CDVh+hZL9naEHMpXaD1i92ncayztXcoJVMBJuqm0Ug3KBF0I8ikEUg1g+x41M9HXX7FHtwFE1eao5AFoHYLb4vOAVyL7f4NhfnoyuURSDc4js6RHK/mEUg9EFyx/no2mcRiHcuxIZ576MPMjqemnsxi0DMcZ5bfP8pyfbO80DgDIFMArH6brrF1051/HBnQ3hAIKVArNJPdns+Vv1xON0dqH2S+IBAxhbkiCQ71cSutV73vNzzO5GTiECmTyybC7Edg/t7/Mt6rEQC6KtqJoEwF9IXDfy+h0AmgTAXggAGE8gkEO9ciN25+EXmQgbHUpMvZBKIdy7kVUnXS2Ikq8mQH1apbAIxOn/trn/bRIqRrGFx1Kx1NoEwktVsKJepWDaBMJJVJo6aTTWbQBjJajaUy1Qsm0C8I1ms6i0Tb+FSzSYQ70jWS5KuCOdNCjw5gYwCMYi2qvd9ki5eQ/RpSXYiI0O9k4dcrASzCsQWLdqtu5dscBdDvbFiuUhpMwqEod4iodRmohkFwlBvm7FcpFYZBTLkMOuHJN1VhDyJhiCQUSC2H8TOyPI8D0u602OITZsEMgrEPrF+5jxEjnN624x7d60yCoTZdHd4YJhRIN7ZdPaFoI90x/7suNxzRhb7QhBIWoGY69kXggB6CWT8xDIo3slC+8yyo0ht5j3qc7OkG7rTXB6XdFyStY48DgJZBZJlJOtot+bsqm5Zja1StqOPDkk64YiP9CZZBfLebqjXEwB2dZvZR3uspbByr1pvxmJMpzezCqT1u9Ptk9BWAKxbrWzhYa3J5c44SWuWVSAtLzfhNq0J5ZxVIN65EOvM3i/pKxMyL53UrZIedWbym+4GYKd5PrOsAjFP21zI3Y6roaPtC/msJFtk6XmekPQ2j2FWm8wCsU+RfzgEEm2o96CkY86APiXpOqdtSrPMAml1qLf1AYiqQs0skFaHem0A4lc9I1g7QcZ+lx65ZRZIq39prYNuHfW+h8WYfYQS3lF4PpIWWxDPDVo7DLiwFIFsJNBaC+JdX2ZQnpf0Tkl/dMRIapPMn1ittSBDDqP4vqRPpI58Z+UzC6S1FoSdks6gH2KWWSCttSC2OsDmdS7tCQDOHR6gkMwCeX93BKkH158kvdVjOKON57RIKx6d8wFOyiyQlpZkDOmgf0nSVwfESGrTzAI5IMn2eniepe8JGdJB5ygjj8c7m8wCaekAOTroA4J+iGlmgdhf3V86l2Qs/a+ud/k+HfQh6mAm/cwJi55n6Z9YVgfPUUZ00D3ePs8mcwvS2jyIufVJSdes+cNnv1m/i9nzASLJLJAh224fkXT7AK5zmNohDVanfSsy/093kondrMUzgEBmgXi/2w3nK5LMfqmPZ5FitJ2Ri2CdWSDmgAck3ePwhHVuDy/0ADnvHMiS6+BwwTwm2QViI1nWAd90V+GOZ5Y6ksUcSEHtZBdIC/MHLdShYIhvl3R2gXj7IUvefeetA3MgI7SSXSDe+YOlX4XAHMiI4Pe8gkDOUmrhKoTfSrpxzWgbcyAeNaywQSBtXIVgp7jbJOC1uwYcXpR0WtJHJdkhcTwDCSAQKfr5WJsmCJ+VdIukkwPjAvOOAAI5e0VA1DVZTBAWljICkaLuLGSCsLA4LHkEIkXdWcgEIQKpQOBs5zbizkKbILRy9x3SYBA5YnRkKNGCnF2EaKM9lzkY2rqtBx12NUy+2d0i1ZcXE4R9hDb8jkDOwrGJNgv+TVeWvSTpii1YT/mqt/9hedoqALPnGUEAgZyDZnslbluzcNFuhrVv/qVsNhrS//iepE+OiA1eoZO+JwZsxe6HJNm1ydaa2OfJ3xY40cYCxUrypQXZC/qmbsmGieR33RyJrcVa0hO137Qkhq6yIBAXpsUZcZNtJZcgkEqgJ85mSB9kqRu9JkZSJjkEUoZr6VTpg5Qm3KWPQCqBnjgb+iATA12XHAKpBHribOiDTAwUgVQCWimb6Ev0K2HaPhtakO0ZzpFC5CX6c/AanScCGY1u1hdbPDZ1VqB8Yi0S/+hC2SWcH3e+HeHgbWdV6pvRgtRnvm2O1kG31ceeZe6W12Pdtttt8035PgKJ5/ZbJT06oNjsBRkAa7cpAtkC3kyv3j3gjGBbQ3bvgvawzIRsfLYIZDy7ud78Qrd/xZO/CWTTHhdPGqltEEg89w8RiPVVroxXxeWUGIEsxxfekgwRyAvd3hZv2tjtIoBA4oUEAqnoMwRSEfZEWSGQiUB6kkEgHkrLsvn8gFGppyW9cVnFj1UaBBLLX1bag5KOOYt9StJ1TlvMVhBAIPHCgnVYFX2GQCrCniirIddXM4u+JXQEsiXAGV73Xrm25GvjZsA2LksEMo7b3G9x5VolDyCQSqALZGMnQdrlOPtWpM2VaxMBRyATgZwpGTvSx0a17JA7u+vdToJ8aoEnQc6EZ/tsEcj2DOdOIcJJkHMzGp0/AhmNjhczEEAgGbxMHUcTQCCj0fFiBgIIJIOXqeNoAghkNDpezEAAgWTwMnUcTQCBjEbHixkIIJAMXqaOowkgkNHoeDEDAQSy3ss3S7pB0n5Jj0s6LmlpdxVmiNFZ64hAVuM/KumApKu7Iz5flvScpEOSTszqMTKvSgCB7MVtLYVtSlq1SvZ0d5f6yapeIrPZCCCQC9EfkXTHGnHsWFprsko8szmRjMsRQCDn2Nqp6c90fY5NxG1J+eEB5+OW8x4pFyeAQM4h5mrl4uEWLwMEcs5nXK0cL36LlxiBnEPsPQzBPrHuG3B4W3EnkkE5AgjkQrYchlAu1kKmjED2uo3DEEKGcplCI5DVXFcdhmAjXDZR+EQZV5DqEgkgkPVe4TCEJUZs5TIhkMrAyS4WAQQSy1+UtjIBBFIZONnFIoBAYvmL0lYmgEAqAye7WAQQSCx/UdrKBBBIZeBkF4sAAonlL0pbmQACqQyc7GIRQCCx/EVpKxNAIJWBk10sAggklr8obWUCCKQycLKLRQCBxPIXpa1MAIFUBk52sQggkFj+orSVCSCQysDJLhYBBBLLX5S2MgEEUhk42cUigEBi+YvSViaAQCoDJ7tYBBBILH9R2soEEEhl4GQXiwACieUvSluZAAKpDJzsYhFAILH8RWkrE0AglYGTXSwCCCSWvyhtZQIIpDJwsotFAIHE8helrUwAgVQGTnaxCCCQWP6itJUJIJDKwMkuFgEEEstflLYyAQRSGTjZxSKAQGL5i9JWJoBAKgMnu1gEEEgsf1HaygQQSGXgZBeLAAKJ5S9KW5nA/wHnY93Y8+GmVwAAAABJRU5ErkJggg=='
    pix = convert_base64_image(img)
    print(model.predict(pix))
