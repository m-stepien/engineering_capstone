import numpy as np
from keras.api import preprocessing
from keras.src.legacy.backend import expand_dims
from keras.src.saving import load_model

model = load_model('traffic_sign_model.keras')


def predict_image(image_path):
	img = preprocessing.image.load_img(image_path, target_size=(64, 64))
	img_array = preprocessing.image.img_to_array(img)
	img_array = expand_dims(img_array, 0)

	predictions = model.predict(img_array)

	confidence = predictions.max(axis=-1)[0]
	class_idx = predictions.argmax(axis=-1)[0]

	threshold = 0.7
	class_labels = ['50', '70', '100', 'null']

	if confidence < threshold or class_labels[class_idx] == 'null':
		return None
	print(confidence, class_labels[class_idx])
	return class_labels[class_idx]


# Example usage
prediction = predict_image("./images/100/52782106_605.jpg")
print(f"Predicted class: {prediction}")
