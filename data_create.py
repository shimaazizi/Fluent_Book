import os
import shutil
import hashlib
from collections import defaultdict

# Unified class list
unified_classes = [
    'gloves', 'goggles', 'helmet', 'mask', 'no_suit', 'no_gloves',
    'no_goggles', 'no_helmet', 'no_mask', 'no_shoes', 'shoes', 'suit',
    'no_vest', 'person', 'vest', 'boots', 'human', 'glasses', 'hat',
    'no_boots', 'no_hat'
]

# Define class mappings for each dataset to the unified class list
dataset_class_mappings = [
    # Dataset 1 (nc: 12)
    {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11},
    # Dataset 2 (nc: 5)
    {0: 2, 1: 7, 2: 12, 3: 13, 4: 14},
    # Dataset 3 (nc: 5)
    {0: 15, 1: 0, 2: 2, 3: 13, 4: 14},
    # Dataset 4 (nc: 5)
    {0: 15, 1: 0, 2: 2, 3: 13, 4: 14},
    # Dataset 5 (nc: 4)
    {0: 15, 1: 2, 2: 14, 3: 12},
    # Dataset 6 (nc: 16)
    {0: 0, 1: 2, 2: 13, 3: 15, 4: 14, 5: 15, 6: 17, 7: 0, 8: 18, 9: 2,
     10: 19, 11: 19, 12: 5, 13: 18, 14: 12, 15: 14}
]

def calculate_file_hash(file_path, chunk_size=8192):
    """Calculate the MD5 hash of a file to identify duplicates."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def update_annotation_file(label_path, class_mapping, output_path):
    """Reads the YOLO annotation file, updates class IDs using the mapping, and writes to a new file."""
    with open(label_path, 'r') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        new_class_id = class_mapping[class_id]
        updated_line = f"{new_class_id} " + " ".join(parts[1:]) + "\n"
        updated_lines.append(updated_line)

    with open(output_path, 'w') as f:
        f.writelines(updated_lines)

def merge_datasets(datasets, class_mappings, splits, merged_root):
    """Merges images and labels from multiple datasets to a unified format with detailed statistics."""
    image_counter = 0
    seen_hashes = set()  # Set to track file hashes and avoid duplicates
    duplicate_count = defaultdict(int)
    dataset_stats = defaultdict(lambda: defaultdict(int))

    for dataset, class_mapping in zip(datasets, class_mappings):
        for split in splits:
            image_dir = os.path.join(dataset['root'], split, 'images')
            label_dir = os.path.join(dataset['root'], split, 'labels')

            if not os.path.exists(image_dir) or not os.path.exists(label_dir):
                print(f"Warning: Directory not found - {image_dir} or {label_dir}")
                continue

            for image_file in os.listdir(image_dir):
                if image_file.endswith('.jpg'):
                    image_path = os.path.join(image_dir, image_file)
                    dataset_stats[dataset['root']][split] += 1

                    try:
                        file_hash = calculate_file_hash(image_path)
                    except Exception as e:
                        print(f"Error calculating hash for {image_path}: {str(e)}")
                        continue

                    if file_hash not in seen_hashes:
                        seen_hashes.add(file_hash)
                        
                        # Copy image
                        shutil.copy(image_path, os.path.join(merged_root, split, 'images', f'{image_counter}.jpg'))
                        
                        # Update and copy label
                        label_file = image_file.replace('.jpg', '.txt')
                        label_path = os.path.join(label_dir, label_file)
                        if os.path.exists(label_path):
                            update_annotation_file(
                                label_path,
                                class_mapping,
                                os.path.join(merged_root, split, 'labels', f'{image_counter}.txt')
                            )
                        else:
                            print(f"Warning: Missing label for image {image_file}")
                        
                        image_counter += 1
                    else:
                        duplicate_count[dataset['root']] += 1

    print("\nMerging complete!")
    print(f"Total unique images processed: {image_counter}")
    
    print("\nDuplicate images per dataset:")
    for dataset, count in duplicate_count.items():
        print(f"{dataset}: {count}")
    
    print("\nDetailed statistics per dataset and split:")
    for dataset, splits_data in dataset_stats.items():
        print(f"\nDataset: {dataset}")
        for split, count in splits_data.items():
            print(f"  {split}: {count} images")

    return image_counter, duplicate_count, dataset_stats

def validate_merged_dataset(datasets, merged_root, splits):
    """Validates the merged dataset against the original datasets."""
    all_images_count = 0
    all_labels_count = 0
    merged_images_count = 0
    merged_labels_count = 0

    for dataset in datasets:
        for split in splits:
            images_count, labels_count = count_files_in_dataset(dataset['root'], split)
            all_images_count += images_count
            all_labels_count += labels_count
            print(f"Original {split}: {images_count} images, {labels_count} labels from {dataset['root']}")

    for split in splits:
        merged_images, merged_labels = count_files_in_merged_dataset(merged_root, split)
        merged_images_count += merged_images
        merged_labels_count += merged_labels
        print(f"Merged {split}: {merged_images} images, {merged_labels} labels")

    print("\nSummary:")
    print(f"Total original images: {all_images_count}")
    print(f"Total original labels: {all_labels_count}")
    print(f"Total merged images: {merged_images_count}")
    print(f"Total merged labels: {merged_labels_count}")

    if merged_images_count == merged_labels_count:
        print("Validation successful: Number of merged images matches number of merged labels.")
    else:
        print("Validation failed: Mismatch between number of merged images and labels.")

    return all_images_count, all_labels_count, merged_images_count, merged_labels_count

def count_files_in_dataset(dataset_root, split):
    """Counts images and labels in a dataset split."""
    image_dir = os.path.join(dataset_root, split, 'images')
    label_dir = os.path.join(dataset_root, split, 'labels')
    
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    return len(image_files), len(label_files)

def count_files_in_merged_dataset(merged_root, split):
    """Counts images and labels in the merged dataset split."""
    merged_image_dir = os.path.join(merged_root, split, 'images')
    merged_label_dir = os.path.join(merged_root, split, 'labels')
    merged_image_files = [f for f in os.listdir(merged_image_dir) if f.endswith('.jpg')]
    merged_label_files = [f for f in os.listdir(merged_label_dir) if f.endswith('.txt')]
    return len(merged_image_files), len(merged_label_files)

# Main execution
if __name__ == "__main__":
    datasets = [
        {'root': '/home/shima98/clothing/PPEs.v8-allclasses-roboflow-fast-model.yolov8 (1)'},
        {'root': '/home/shima98/clothing/construction safety.v2-release.yolov8 (1)'},
        {'root': '/home/shima98/clothing/PPE Detection.v1i.yolov8'},
        {'root': '/home/shima98/clothing/ppe safety.v1i.yolov8 (1)'},
        {'root': '/home/shima98/clothing/WithPPE.v1i.yolov8'},
        {'root': '/home/shima98/clothing/Construction PPE.v3i.yolov8'}
    ]
    splits = ['train', 'test', 'valid']
    merged_root = '/home/shima98/dataset_merge'

    # Ensure merged_root directories exist
    for split in splits:
        os.makedirs(os.path.join(merged_root, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(merged_root, split, 'labels'), exist_ok=True)

    # Merge datasets
    total_processed, duplicates, stats = merge_datasets(datasets, dataset_class_mappings, splits, merged_root)

    print(f"\nTotal images in original datasets: {sum(sum(splits.values()) for splits in stats.values())}")
    print(f"Total unique images in merged dataset: {total_processed}")
    print(f"Total duplicate images: {sum(duplicates.values())}")

    # Validate merged dataset
    validate_merged_dataset(datasets, merged_root, splits)
