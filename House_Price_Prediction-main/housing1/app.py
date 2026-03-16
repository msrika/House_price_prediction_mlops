from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from visualization import DataVisualizer
import os

app = Flask(__name__)
app.static_folder = 'static'

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Data", "house_price.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

X = df.drop("Price", axis=1)
y = df["Price"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        area = float(request.form["Area"])
        bedrooms = float(request.form["Bedrooms"])
        bathrooms = float(request.form["Bathrooms"])
        stories = float(request.form["Stories"])
        parking = float(request.form["Parking"])
        age = float(request.form["Age"])
        location = float(request.form["Location"])

        # Prepare input for model
        arr = np.array([[area, bedrooms, bathrooms, stories, parking, age, location]])

        prediction = model.predict(arr)[0]

        return render_template(
            "index.html",
            prediction_text=f"Predicted House Price: Rs. {int(prediction):,}"
        )

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}")


@app.route("/visualize")
def visualize():
    """Route to display data visualizations"""
    viz = DataVisualizer()
    insights = viz.get_data_insights()
    
    # Create visualizations
    correlation_img = viz.create_correlation_heatmap()
    distribution_img = viz.create_feature_distributions()
    scatter_img = viz.create_scatter_plots()
    perf_img, metrics = viz.create_model_performance_charts()
    
    return render_template(
        "index.html",
        show_visualizations=True,
        correlation_img=correlation_img,
        distribution_img=distribution_img,
        scatter_img=scatter_img,
        perf_img=perf_img,
        metrics=metrics,
        insights=insights
    )


@app.route("/dashboard")
def dashboard():
    """Route for interactive dashboard"""
    viz = DataVisualizer()
    interactive_dashboard = viz.create_interactive_dashboard()
    
    return render_template(
        "index.html",
        show_dashboard=True,
        interactive_dashboard=interactive_dashboard
    )


if __name__ == "__main__":
    # Get port from environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run with production server when deployed
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # For local development
        app.run(host='0.0.0.0', port=port, debug=True)