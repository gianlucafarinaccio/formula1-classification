import os
import random
import shutil

# Define paths
dataset_path = 'dataset'
images_path = os.path.join(dataset_path, 'images')
labels_path = os.path.join(dataset_path, 'labels')

# Train-test split ratio
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

# Get list of image files
images = [f for f in os.listdir(images_path) if f.endswith('.jpg')]
random.shuffle(images)

# Calculate split indices
train_split = int(train_ratio * len(images))
val_split = int((train_ratio + val_ratio) * len(images))

# Split into train, val, test
train_images = images[:train_split]
val_images = images[train_split:val_split]
test_images = images[val_split:]

# Move files
def move_files(file_list, src_folder, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    for file in file_list:
        shutil.move(os.path.join(src_folder, file), dest_folder)

move_files(train_images, images_path, os.path.join(images_path, 'train'))
move_files(train_images, labels_path, os.path.join(labels_path, 'train'))

move_files(val_images, images_path, os.path.join(images_path, 'val'))
move_files(val_images, labels_path, os.path.join(labels_path, 'val'))

move_files(test_images, images_path, os.path.join(images_path, 'test'))
move_files(test_images, labels_path, os.path.join(labels_path, 'test'))
