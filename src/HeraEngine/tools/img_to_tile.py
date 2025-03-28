from PIL import Image
import os

def split_image(image_path, grid_size):
    image = Image.open(image_path)
    width, height = image.size
    cell_width = width // grid_size
    cell_height = height // grid_size
    
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_folder = os.path.join(os.path.dirname(image_path), image_name)
    os.makedirs(output_folder, exist_ok=True)
    
    for i in range(grid_size):
        for j in range(grid_size):
            left = j * cell_width
            upper = i * cell_height
            right = left + cell_width
            lower = upper + cell_height
            
            cell = image.crop((left, upper, right, lower))
            cell.save(os.path.join(output_folder, f"{i}_{j}.png"))
    
    print(f"Image split into {grid_size}x{grid_size} and saved in '{output_folder}'")

split_image("Assets/Textures/Minigames/Puzzle/prune.png", 3)
