import os

def load_file(filename: str, default: str = "") -> str:
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[WARNING] File not found: {filename}. Using default.")
    except Exception as e:
        print(f"[ERROR] Failed to load file: {filename}. Using default.")   
    return default        
