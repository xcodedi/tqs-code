import os
import re

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_number_sequence(folder, extensions=('.lst', '.pdf', '.dxf')):
    try:
        if not os.path.isdir(folder):
            print(f"⚠️ The folder '{folder}' does not exist or is not accessible.")
            return

        files = os.listdir(folder)
        filtered_files = [
            file for file in files 
            if file.lower().endswith(tuple(ext.lower() for ext in extensions))
        ]

        if not filtered_files:
            print("ℹ️ No files with the specified extensions were found.")
            return

        numbers = []
        for name in filtered_files:
            matches = re.findall(r'(\d+)', name)
            for match in matches:
                numbers.append(int(match))

        if not numbers:
            print("⚠️ No numbers were found in the file names.")
            return

        unique_numbers = sorted(set(numbers))  # Remove duplicates and sort
        print("📂 Numbers found:", unique_numbers)

        start = 1
        end = unique_numbers[-1]
        expected = set(range(start, end + 1))
        numbers_set = set(unique_numbers)

        missing = sorted(expected - numbers_set)
        duplicates = [n for n in numbers if numbers.count(n) > 1]

        if missing:
            print(f"❌ Missing numbers in sequence: {missing}")
        else:
            print("✅ All numbers are present, starting at 1 with no gaps.")

        if duplicates:
            print(f"⚠️ Warning: Duplicate numbers found: {sorted(set(duplicates))}")

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    clear_screen()
    folder = input("Enter the folder path to check (or press Enter for current directory): ").strip()
    folder = folder if folder else os.getcwd()
    check_number_sequence(folder)