import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
import os


# Load the VGG16 model
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features

def find_duplicates(image_folder):
    features_dict = {}
    duplicates = []

    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            features = extract_features(image_path, model)
            features_dict[image_path] = features

    for img1, features1 in features_dict.items():
        for img2, features2 in features_dict.items():
            if img1 != img2:
                similarity = cosine_similarity(features1, features2)
                if similarity > 0.9:  # Adjust threshold
                    duplicates.append((img1, img2))

    return duplicates

image_folder = 'images/'
duplicates = find_duplicates(image_folder)

print(len(duplicates))
# for dup in duplicates:
#     print(f"Duplicate found: {dup}")
