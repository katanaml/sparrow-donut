# tools/donut/dataset_generator.py

from pathlib import Path
import random
from datasets import Dataset, DatasetDict
import json

class DonutDatasetGenerator:
    def generate(self, data_dir):
        img_dir = Path(data_dir) / "img"
        dataset_dict = DatasetDict()
        
        for split in ['train', 'validation', 'test']:
            split_dir = img_dir / split
            metadata_file = split_dir / "metadata.jsonl"
            
            if split_dir.exists() and metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = [json.loads(line) for line in f]
                
                dataset = Dataset.from_dict({
                    'image': [str(split_dir / item['file_name']) for item in metadata],
                    'ground_truth': [item['ground_truth'] for item in metadata]
                })
                
                dataset_dict[split] = dataset
                print(f"{split.capitalize()} set has {len(dataset)} images")
            else:
                print(f"Directory or metadata file not found for {split} set")
        
        if dataset_dict:
            print(f"Dataset features are: {next(iter(dataset_dict.values())).features.keys()}")
            
            if 'train' in dataset_dict and dataset_dict['train']:
                train_dataset = dataset_dict['train']
                random_sample = random.choice(range(len(train_dataset)))
                print(f"Random sample from training set:")
                print(f"Image path: {train_dataset[random_sample]['image']}")
                print(f"Ground truth: {train_dataset[random_sample]['ground_truth']}")
        else:
            print("No datasets were loaded")

        return dataset_dict