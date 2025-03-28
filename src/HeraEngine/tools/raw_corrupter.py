import os
import numpy as np
from tqdm import tqdm
from PIL import Image

def image_to_raw_data(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        width, height = img.size
        pixels = list(img.getdata())
        
    raw_data = [str(width), str(height)]
    for r, g, b, a in pixels:
        raw_data.append("0" if a == 0 else str((r << 16) | (g << 8) | b))
    
    return raw_data

def apply_corruption(raw_data):
    width, height = map(int, raw_data[:2])
    pixel_array = np.array(raw_data[2:], dtype=np.uint32).reshape(height, width)
    
    # Column shifting
    n_cols = pixel_array.shape[1]
    shifted_cols = np.argsort(np.arange(n_cols) + np.random.randint(-15, 16, n_cols))
    pixel_array = pixel_array[:, shifted_cols]
    
    # Value corruption
    corruption_factors = np.random.randint(0, 256, pixel_array.shape, dtype=np.uint32)
    corrupted_array = (pixel_array * corruption_factors).flatten()
    
    return ";".join([str(width), str(height)] + corrupted_array.astype(str).tolist())

def process_image_files(root_folder):
    png_files = []
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".png"):
                base_path = os.path.join(root, file)
                raw_path = os.path.splitext(base_path)[0] + ".raw"
                png_files.append((base_path, raw_path))
    
    for input_path, output_path in tqdm(png_files, desc="Processing images"):
        # Save raw data
        raw_data = image_to_raw_data(input_path)
        with open(output_path, "w") as f:
            f.write(";".join(raw_data))
        
        # Save corrupted version
        corrupted_data = apply_corruption(raw_data)
        with open(f"{output_path}.corrupted", "w") as f:
            f.write(corrupted_data)

if __name__ == "__main__":
    target_folder = "Assets/Textures/Cutscenes"
    process_image_files(target_folder)
    print("\nImage processing completed successfully.")