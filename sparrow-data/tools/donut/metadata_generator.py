# tools/donut/metadata_generator.py

from pathlib import Path
import json
import cv2

class DonutMetadataGenerator:
    def generate(self, data_dir, files_list, split):
        base_img_dir = Path(data_dir) / "img"
        split_img_dir = base_img_dir / split
        split_img_dir.mkdir(parents=True, exist_ok=True)

        metadata_list = []

        for file_name in files_list:
            img_file = base_img_dir / f"{file_name.stem}.jpg"
            if img_file.exists():
                img = cv2.imread(str(img_file))
                cv2.imwrite(str(split_img_dir / f"{file_name.stem}.jpg"), img)

                with open(file_name, "r") as json_file:
                    data = json.load(json_file)
                    metadata_list.append({
                        "ground_truth": json.dumps({"gt_parse": data}),
                        "file_name": f"{file_name.stem}.jpg"
                    })

        with open(split_img_dir / "metadata.jsonl", "w") as outfile:
            for entry in metadata_list:
                json.dump(entry, outfile)
                outfile.write("\n")

        print(f"Generated metadata for {len(metadata_list)} images in {split} set")
