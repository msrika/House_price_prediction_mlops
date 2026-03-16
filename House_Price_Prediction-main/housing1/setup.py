"""
Setup script for MLOps House Price Prediction
Run this after installation to set up the project structure
"""
import os
from pathlib import Path


def create_directory_structure():
    """Create necessary directories for the project"""
    directories = [
        "data/raw",
        "data/processed",
        "models",
        "models/registry",
        "artifacts",
        "logs",
        "experiments",
        "notebooks"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def create_gitkeep_files():
    """Create .gitkeep files for empty directories"""
    gitkeep_dirs = [
        "data/raw",
        "data/processed",
        "models",
        "artifacts",
        "logs",
        "experiments"
    ]
    
    for directory in gitkeep_dirs:
        gitkeep_path = Path(directory) / ".gitkeep"
        if not gitkeep_path.exists():
            with open(gitkeep_path, 'w') as f:
                f.write("# Keep this directory\n")
            print(f"✓ Created .gitkeep in: {directory}")


def copy_example_config():
    """Copy example config if config doesn't exist"""
    config_path = Path("configs/config.yaml")
    example_path = Path("configs/config.example.yaml")
    
    if not config_path.exists() and example_path.exists():
        import shutil
        shutil.copy(example_path, config_path)
        print(f"✓ Created config.yaml from example")


def main():
    """Main setup function"""
    print("\n🚀 Setting up MLOps House Price Prediction project...\n")
    
    create_directory_structure()
    create_gitkeep_files()
    copy_example_config()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Place your data file in data/raw/house_price.csv")
    print("2. Update configs/config.yaml with your settings")
    print("3. Run 'make train' to train a model")
    print("4. Run 'make api' to start the prediction API\n")


if __name__ == "__main__":
    main()
