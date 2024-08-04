# run_donut.py

from pathlib import Path
import shutil
import random
from tools.donut.metadata_generator import DonutMetadataGenerator
from tools.donut.dataset_generator import DonutDatasetGenerator

def copy_files(src_dir, dst_dir, file_ext):
    for file in Path(src_dir).glob(f'*.{file_ext}'):
        shutil.copy(file, dst_dir)

def main():
    # Define source and destination directories
    src_dir_json = '../sparrow-ui/docs/json/key'
    src_dir_img = '../sparrow-ui/docs/images'
    base_path = Path('docs/models/donut/data')
    dst_dir_json = base_path / 'key'
    dst_dir_img = base_path / 'img'

    # Create destination directories if they don't exist
    dst_dir_json.mkdir(parents=True, exist_ok=True)
    dst_dir_img.mkdir(parents=True, exist_ok=True)

    # Copy JSON files and images
    copy_files(src_dir_json, dst_dir_json, 'json')
    copy_files(src_dir_img, dst_dir_img, 'jpg')

    # Prepare files for Donut format
    json_files = list(dst_dir_json.glob("*.json"))
    random.shuffle(json_files)

    # Split files into train, validation, and test sets
    total_files = len(json_files)
    train_size = int(total_files * 0.8)
    val_size = int(total_files * 0.1)
    train_files = json_files[:train_size]
    val_files = json_files[train_size:train_size+val_size]
    test_files = json_files[train_size+val_size:]

    print(f"Train set size: {len(train_files)}")
    print(f"Validation set size: {len(val_files)}")
    print(f"Test set size: {len(test_files)}")

    # Generate metadata
    metadata_generator = DonutMetadataGenerator()
    for split, files in [("train", train_files), ("validation", val_files), ("test", test_files)]:
        metadata_generator.generate(base_path, files, split)

    # Generate dataset
    dataset_generator = DonutDatasetGenerator()
    datasets = dataset_generator.generate(base_path)

    if datasets:
        print("Datasets generated successfully")
    else:
        print("Failed to generate datasets")

if __name__ == '__main__':
    main()