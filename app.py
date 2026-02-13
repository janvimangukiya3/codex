from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import plotly
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Base directory (script location) to resolve relative data/model paths
BASE_DIR = Path(__file__).resolve().parent

# Load model and data using absolute paths relative to this file
model_path = BASE_DIR / "delivery_model.pkl"
data_path = BASE_DIR / "Dataset.csv"

if not model_path.exists():
    raise FileNotFoundError(f"Model file not found at {model_path}.\nRun the training script to create it, or place the file there.")
model = joblib.load(model_path)

if not data_path.exists():
    raise FileNotFoundError(f"Dataset file not found at {data_path}.")
df = pd.read_csv(data_path)

# Prepare analytics data
def get_analytics_data():
    """Generate comprehensive analytics from the dataset"""
    
    # Basic statistics
    stats = {
        'total_deliveries': len(df),
        'avg_delivery_time': round(df['Delivery_Time'].mean(), 2),
        'avg_distance': round(df['Distance_km'].mean(), 2),
        'avg_rating': round(df['Delivery_person_Ratings'].mean(), 2)
    }
    
    # Vehicle type mapping
    vehicle_map = {1: 'Motorcycle', 2: 'Scooter', 3: 'Electric'}
    order_map = {0: 'Snacks', 1: 'Meal', 2: 'Drinks', 3: 'Buffet'}
    
    # Distribution charts data
    vehicle_dist = df['Type_of_vehicle'].value_counts().to_dict()
    vehicle_dist = {vehicle_map.get(k, f'Type {k}'): v for k, v in vehicle_dist.items()}
    
    order_dist = df['Type_of_order'].value_counts().to_dict()
    order_dist = {order_map.get(k, f'Type {k}'): v for k, v in order_dist.items()}
    
    return stats, vehicle_dist, order_dist

# Model performance metrics
def get_model_performance():
    """Calculate model performance metrics"""
    from sklearn.model_selection import train_test_split
    
    # Prepare data
    # Prepare data
    features = [
        "Delivery_person_Age",
        "Delivery_person_Ratings",
        "Type_of_vehicle",
        "Type_of_order",
        "Distance_km"
    ]
    X = df[features]
    y = df['Delivery_Time']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    return {
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'r2': round(r2, 4),
        'accuracy': round(r2 * 100, 2)
    }

@app.route("/")
def home():
    """Home page with overview"""
    stats, vehicle_dist, order_dist = get_analytics_data()
    return render_template("index.html", stats=stats)

@app.route("/predict-page")
def predict_page():
    """Prediction interface page"""
    return render_template("predict.html")

@app.route("/analytics")
def analytics():
    """Analytics dashboard page"""
    stats, vehicle_dist, order_dist = get_analytics_data()
    performance = get_model_performance()
    
    return render_template("analytics.html", 
                         stats=stats, 
                         performance=performance)

@app.route("/about")
def about():
    """About the project page"""
    return render_template("about.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        age = float(data["age"])
        rating = float(data["rating"])
        distance = float(data["distance"])
        vehicle = int(data["vehicle"])
        order = int(data["order"])
        
        # Create input dataframe ensuring correct column order
        input_data = {
            "Delivery_person_Age": [age],
            "Delivery_person_Ratings": [rating],
            "Type_of_vehicle": [vehicle],
            "Type_of_order": [order],
            "Distance_km": [distance]
        }
        input_df = pd.DataFrame(input_data)
        
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 2)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route("/api/charts/delivery-time-distribution")
def chart_delivery_time():
    """Generate delivery time distribution chart"""
    fig = px.histogram(df, x='Delivery_Time', nbins=30,
                      title='Delivery Time Distribution',
                      labels={'Delivery_Time': 'Delivery Time (minutes)', 'count': 'Frequency'},
                      color_discrete_sequence=['#667eea'])
    fig.update_layout(template='plotly_white', showlegend=False)
    return jsonify(json.loads(fig.to_json()))

@app.route("/api/charts/distance-vs-time")
def chart_distance_time():
    """Generate distance vs time scatter plot"""
    fig = px.scatter(df, x='Distance_km', y='Delivery_Time',
                    title='Distance vs Delivery Time',
                    labels={'Distance_km': 'Distance (km)', 'Delivery_Time': 'Time (min)'},
                    color_discrete_sequence=['#f093fb'])
    
    # Add manual trendline
    z = np.polyfit(df['Distance_km'], df['Delivery_Time'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(x=df['Distance_km'].sort_values(), 
                            y=p(df['Distance_km'].sort_values()),
                            mode='lines',
                            name='Trend',
                            line=dict(color='#667eea', width=3)))
    
    fig.update_layout(template='plotly_white')
    return jsonify(json.loads(fig.to_json()))

@app.route("/api/charts/rating-impact")
def chart_rating_impact():
    """Generate rating impact chart"""
    rating_groups = df.groupby('Delivery_person_Ratings')['Delivery_Time'].mean().reset_index()
    fig = px.bar(rating_groups, x='Delivery_person_Ratings', y='Delivery_Time',
                title='Average Delivery Time by Rating',
                labels={'Delivery_person_Ratings': 'Rating', 'Delivery_Time': 'Avg Time (min)'},
                color='Delivery_Time',
                color_continuous_scale='Viridis')
    fig.update_layout(template='plotly_white')
    return jsonify(json.loads(fig.to_json()))

@app.route("/api/charts/vehicle-comparison")
def chart_vehicle():
    """Generate vehicle type comparison"""
    vehicle_map = {1: 'Motorcycle', 2: 'Scooter', 3: 'Electric'}
    df_temp = df.copy()
    df_temp['Vehicle_Name'] = df_temp['Type_of_vehicle'].map(vehicle_map)
    
    vehicle_stats = df_temp.groupby('Vehicle_Name')['Delivery_Time'].agg(['mean', 'count']).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=vehicle_stats['Vehicle_Name'], y=vehicle_stats['mean'],
                        name='Avg Time', marker_color='#667eea'))
    fig.update_layout(title='Average Delivery Time by Vehicle Type',
                     xaxis_title='Vehicle Type',
                     yaxis_title='Average Time (minutes)',
                     template='plotly_white')
    return jsonify(json.loads(fig.to_json()))

@app.route("/api/charts/order-type-analysis")
def chart_order_type():
    """Generate order type analysis"""
    order_map = {0: 'Snacks', 1: 'Meal', 2: 'Drinks', 3: 'Buffet'}
    df_temp = df.copy()
    df_temp['Order_Name'] = df_temp['Type_of_order'].map(order_map)
    
    order_stats = df_temp.groupby('Order_Name')['Delivery_Time'].mean().reset_index()
    
    fig = px.pie(order_stats, values='Delivery_Time', names='Order_Name',
                title='Delivery Time Distribution by Order Type',
                color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(template='plotly_white')
    return jsonify(json.loads(fig.to_json()))

@app.route("/api/charts/age-performance")
def chart_age():
    """Generate age vs performance chart"""
    age_bins = pd.cut(df['Delivery_person_Age'], bins=[20, 25, 30, 35, 40, 50], 
                     labels=['20-25', '26-30', '31-35', '36-40', '41-50'])
    df_temp = df.copy()
    df_temp['Age_Group'] = age_bins
    
    age_stats = df_temp.groupby('Age_Group', observed=True)['Delivery_Time'].mean().reset_index()
    
    fig = px.line(age_stats, x='Age_Group', y='Delivery_Time',
                 title='Delivery Time by Age Group',
                 markers=True,
                 labels={'Age_Group': 'Age Group', 'Delivery_Time': 'Avg Time (min)'},
                 color_discrete_sequence=['#f093fb'])
    fig.update_layout(template='plotly_white')
    return jsonify(json.loads(fig.to_json()))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
