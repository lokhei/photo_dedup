import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
import os
from sklearn.cluster import DBSCAN


# Load the VGG16 model
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features

def find_duplicates(image_folder, similarity_threshold=0.9):
    features_dict = {}
    duplicates_dict = {}
    seen = set()

    # Extract features for each image
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    for filename in image_files:
        image_path = os.path.join(image_folder, filename)
        features = extract_features(image_path, model)
        features_dict[image_path] = features

    # Compare images
    image_paths = list(features_dict.keys())
    for i in range(len(image_paths)):
        img1 = image_paths[i]
        if img1 in seen:
            continue
        for j in range(i + 1, len(image_paths)):
            img2 = image_paths[j]
            if img2 in seen:
                continue
            features1 = features_dict[img1]
            features2 = features_dict[img2]
            similarity = cosine_similarity(features1, features2)[0][0]
            if similarity > similarity_threshold:
                if img1 not in duplicates_dict:
                    duplicates_dict[img1] = []
                duplicates_dict[img1].append(img2)
                seen.add(img2)

    return duplicates_dict

