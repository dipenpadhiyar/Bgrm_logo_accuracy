import os
import time
from rembg import remove, new_session
from PIL import Image
import numpy as np

input_folder = "Logos" 

output_parent_folder = "processed_images" 

# List of models to process
models = [
    "u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg",
    "silueta", "isnet-general-use", "isnet-anime", "sam",
    "birefnet-general", "birefnet-general-lite", "birefnet-portrait",
    "birefnet-dis", "birefnet-hrsod", "birefnet-cod", "birefnet-massive"
]

os.makedirs(output_parent_folder, exist_ok=True)

log_file = os.path.join(output_parent_folder, "model_processing_log.md")

with open(log_file, "w") as log:
    log.write(f"# Model Processing Log\n")
    log.write(f"Input Folder: `{input_folder}`\n")
    log.write(f"Output Parent Folder: `{output_parent_folder}`\n\n")
    log.write("| Model Name           | Total Images | Total Time (s) | Avg Time/Image (s) |\n")
    log.write("|----------------------|--------------|----------------|--------------------|\n")

for model in models:
    print(f"Processing images with model: {model}")
    model_folder = os.path.join(output_parent_folder, model)
    os.makedirs(model_folder, exist_ok=True) 

    total_time = 0
    image_count = 0

    try:
        
        session = new_session(model_name=model)

        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                try:
                    input_path = os.path.join(input_folder, filename)
                    output_filename = os.path.splitext(filename)[0] + ".png"  # Enforce PNG format
                    output_path = os.path.join(model_folder, output_filename)

                    print(f"Processing file: {filename} with model: {model}")
                    start_time = time.time()
                    input_image = Image.open(input_path)
                    output_image = Image.fromarray(np.uint8(output_array))
                    output_image.save(output_path, format="PNG")
                    time_taken = time.time() - start_time
                    total_time += time_taken
                    image_count += 1

                    print(f"Processed {filename} in {time_taken:.2f} seconds. Saved to {output_path}.")
                except Exception as e:
                    print(f"Error processing file {filename} with model {model}: {e}")
    except Exception as e:
        print(f"Error initializing model {model}: {e}")
    avg_time = total_time / image_count if image_count > 0 else 0
    with open(log_file, "a") as log:
        log.write(f"| {model:<20} | {image_count:<12} | {total_time:.2f}      | {avg_time:.2f}           |\n")

print(f"Processing completed. Results saved in `{output_parent_folder}`.")
print(f"Processing log saved to `{log_file}`.")
