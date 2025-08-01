import os

def load_files(directory, extensions=(".py",)):
    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extensions):
                path = os.path.join(root, filename)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    files[path] = f.read()
    return files
