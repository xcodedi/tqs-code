import os
import re

os.system('cls' if os.name == 'nt' else 'clear')

# Path to the folder containing files
folder = r"\\Mebranco\arquivo morto\arquivo morto\projetos\2024\3324-basso-45\Plantas\PDFs"

# Iterate through all files in the folder
for filename in os.listdir(folder):
    old_path = os.path.join(folder, filename)

    # Skip if not a file
    if not os.path.isfile(old_path):
        continue

    # Get the first 3 numeric characters
    first_three = filename[:3]

    # Look for another 3-digit number later in the filename
    match = re.search(r'(\d{3})', filename[3:])
    if match:
        new_number = match.group(1)

        # If different, rename the file
        if first_three != new_number:
            new_name = new_number + filename[3:]
            new_path = os.path.join(folder, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")