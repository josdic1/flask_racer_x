import os

def tree_viewer(root):
    # Print the root folder name
    print(os.path.basename(root))
    
    # Define essential file extensions
    essential_extensions = ('.py', '.txt', '.json', '.jsx', '.js', '.css', '.html', '.yaml', '.ini')
    
    # Get all top-level folders, excluding non-essential ones
    folders = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
    
    # Sort and iterate through top-level folders
    for folder in sorted(folders):
        folder_path = os.path.join(root, folder)
        if folder in ['node_modules', '__pycache__', 'venv', '.venv', '.git']:  # Skip non-essential folders
            continue
        print(f"├── {folder}")
        
        # Get essential files in the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(essential_extensions)]
        for i, file in enumerate(sorted(files)):
            prefix = "│   ├── " if i < len(files) - 1 or any(os.path.isdir(os.path.join(folder_path, d)) for d in os.listdir(folder_path) if d not in ['node_modules', '__pycache__', 'venv', '.venv', '.git']) else "│   └── "
            print(f"{prefix}{file}")
        
        # Get essential subfolders
        subdirs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d)) and d not in ['node_modules', '__pycache__', 'venv', '.venv', '.git']]
        for i, subdir in enumerate(sorted(subdirs)):
            prefix = "│   ├── " if i < len(subdirs) - 1 else "│   └── "
            print(f"{prefix}{subdir}")
            
            # Get essential files in the subfolder
            subdir_path = os.path.join(folder_path, subdir)
            subfiles = [f for f in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, f)) and f.endswith(essential_extensions)]
            for j, subfile in enumerate(sorted(subfiles)):
                sub_prefix = "│       ├── " if j < len(subfiles) - 1 or any(os.path.isdir(os.path.join(subdir_path, d)) for d in os.listdir(subdir_path) if d not in ['node_modules', '__pycache__', 'venv', '.venv', '.git']) else "│       └── "
                print(f"{sub_prefix}{subfile}")
            
            # Get essential sub-subfolders
            subsubdirs = [d for d in os.listdir(subdir_path) if os.path.isdir(os.path.join(subdir_path, d)) and d not in ['node_modules', '__pycache__', 'venv', '.venv', '.git']]
            for j, subsubdir in enumerate(sorted(subsubdirs)):
                sub_prefix = "│       ├── " if j < len(subsubdirs) - 1 else "│       └── "
                print(f"{sub_prefix}{subsubdir}")
                
                # Get essential files in the sub-subfolder
                subsubdir_path = os.path.join(subdir_path, subsubdir)
                subsubfiles = [f for f in os.listdir(subsubdir_path) if os.path.isfile(os.path.join(subsubdir_path, f)) and f.endswith(essential_extensions)]
                for k, subsubfile in enumerate(sorted(subsubfiles)):
                    sub_sub_prefix = "│           ├── " if k < len(subsubfiles) - 1 else "│           └── "
                    print(f"{sub_sub_prefix}{subsubfile}")

# Run for the current project root
tree_viewer(os.getcwd())