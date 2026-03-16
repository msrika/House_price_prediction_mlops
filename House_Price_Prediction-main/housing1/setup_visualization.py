#!/usr/bin/env python3
"""
Setup script for visualization libraries
"""
import subprocess
import sys

def install_visualization_libraries():
    """Install visualization libraries"""
    print("Installing visualization libraries...")
    
    libraries = [
        "matplotlib",
        "seaborn", 
        "plotly"
    ]
    
    for lib in libraries:
        try:
            print(f"Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"✓ {lib} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {lib}")
            return False
    
    print("✓ All visualization libraries installed successfully!")
    return True

def test_visualization_module():
    """Test the visualization module"""
    print("\nTesting visualization module...")
    
    try:
        from visualization import DataVisualizer
        viz = DataVisualizer()
        
        if viz.load_data():
            print("✓ Data loaded successfully")
            
            # Test creating a simple visualization
            img = viz.create_correlation_heatmap()
            if img:
                print("✓ Correlation heatmap created successfully")
            
            # Test model performance charts
            perf_img, metrics = viz.create_model_performance_charts()
            if perf_img and metrics:
                print("✓ Model performance charts created successfully")
                print(f"Model metrics: R²={metrics['r2']:.3f}, MAE={metrics['mae']:.2f}")
            
            print("✓ Visualization module working correctly")
            return True
        else:
            print("✗ Failed to load data")
            return False
    except Exception as e:
        print(f"✗ Error testing visualization module: {e}")
        return False

def main():
    """Main setup function"""
    print("🏠 House Price Prediction - Visualization Setup")
    print("=" * 50)
    
    # Install libraries
    if not install_visualization_libraries():
        print("✗ Failed to install visualization libraries")
        return False
    
    # Test visualization module
    if not test_visualization_module():
        print("✗ Visualization module test failed")
        return False
    
    print("\n🎉 Visualization setup completed successfully!")
    print("\n📊 Available features:")
    print("- Correlation heatmaps")
    print("- Feature distribution plots")
    print("- Scatter plots")
    print("- Model performance charts")
    print("- Interactive dashboard")
    print("- Data insights")
    
    print("\n🚀 To run the application:")
    print("1. Run: python app.py")
    print("2. Visit: http://localhost:5000")
    print("3. Navigate to 'Visualizations' or 'Dashboard' tabs")
    
    return True

if __name__ == "__main__":
    main()