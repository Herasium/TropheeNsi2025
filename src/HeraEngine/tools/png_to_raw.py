import os
import time
from PIL import Image

def clear_console():
    # Cross-platform console clear command
    os.system('cls' if os.name == 'nt' else 'clear')

def print_table(results):
    header = ("Input File", "Output File", "Status")
    # Combine header with all rows for width calculation
    all_rows = [header] + results
    col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(3)]
    
    def print_border():
        print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
    
    print_border()
    print("| " + " | ".join(header[i].ljust(col_widths[i]) for i in range(3)) + " |")
    print_border()
    for row in results:
        print("| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(3)) + " |")
    print_border()

def image_to_hex_list(image_path):
    img = Image.open(image_path).convert("RGBA")
    pixels = list(img.getdata())
    hex_list = [str(img.size[0]), str(img.size[1])]
    
    for r, g, b, a in pixels:
        if a == 0:
            hex_list.append("0")
        else:
            hex_list.append(str((r << 16) | (g << 8) | b))
    
    return hex_list

def process_images_recursively(root_folder):
    conversion_results = []
    # Gather all PNG files from the folder tree
    files_to_process = []
    for subdir, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.lower().endswith(".png"):
                file_in = os.path.join(subdir, filename)
                file_out = os.path.join(subdir, f"{os.path.splitext(filename)[0]}.raw")
                files_to_process.append((file_in, file_out))
    
    # Process each file one by one and update the table
    for file_in, file_out in files_to_process:
        # Add file entry with initial status "Processing"
        conversion_results.append((file_in, file_out, "Processing"))
        clear_console()
        print_table(conversion_results)
        
        # Process the image file
        data = image_to_hex_list(file_in)
        with open(file_out, "w") as file:
            file.write(";".join(data))
        
        # Update the status to "Converted"
        conversion_results[-1] = (file_in, file_out, "Converted")
        clear_console()
        print_table(conversion_results)
        
   
    
    print("\nAll files processed.")

folder_path = "Assets/Textures/"
process_images_recursively(folder_path)
