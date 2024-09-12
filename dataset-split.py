import os
import random
import shutil

# Define paths
dataset_path = 'f1-monza-dataset'
images_path = os.path.join(dataset_path, 'images')
turns = ["prima-variante", "biassono", "seconda-variante","lesmo-uno", "lesmo-due", "ascari-uno", "ascari-due", "parabolica"]


# Train-test split ratio
train_ratio = 0.70
val_ratio = 0.15
test_ratio = 0.15

# Get list of image files
images = [f for f in os.listdir(images_path) if f.endswith('.jpg')]
print(images)
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
    for file in file_list:
        subdir = turns[int(file.split("__")[1])]
        print(subdir)
        dest_folder_turns = os.path.join(dest_folder, subdir)
        print(dest_folder_turns)
        shutil.move(os.path.join(src_folder, file), dest_folder_turns)

move_files(train_images, images_path, os.path.join(images_path, 'train'))

move_files(val_images, images_path, os.path.join(images_path, 'val'))

move_files(test_images, images_path, os.path.join(images_path, 'test'))
