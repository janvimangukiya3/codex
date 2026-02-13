# 🚀 Food Delivery Time Predictor

An AI-powered web application that predicts food delivery times using machine learning. Built with Flask, scikit-learn, and modern web technologies.

## ✨ Features

- **Machine Learning Prediction**: Random Forest Regressor trained on real delivery data
- **Interactive Dashboard**: Comprehensive analytics with interactive charts
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Predictions**: Instant delivery time estimates
- **Data Visualizations**: Multiple charts showing delivery patterns and insights
- **Modern UI/UX**: Clean, professional interface with smooth animations

## 📊 Model Performance

- **Accuracy**: High R² score indicating strong predictive power
- **MAE**: Low mean absolute error for accurate predictions
- **RMSE**: Optimized root mean squared error
- **Cross-Validation**: 5-fold CV for robust performance evaluation

## 🛠️ Technologies Used

- **Backend**: Flask (Python web framework)
- **Machine Learning**: scikit-learn (Random Forest Regressor)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (interactive charts)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern gradients and animations

## 📁 Project Structure

```
├── app.py                      # Main Flask application
├── train_model_improved.py     # Enhanced model training script
├── Dataset.csv                 # Training dataset
├── delivery_model.pkl          # Trained model
├── model_columns.pkl           # Feature columns
├── requirements.txt            # Python dependencies
├── static/
│   └── style.css              # Responsive CSS styles
└── Templates/
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── predict.html           # Prediction interface
    ├── analytics.html         # Analytics dashboard
    └── about.html             # About page
```

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd food-delivery-predictor
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model** (optional - model already included)
   ```bash
   python train_model_improved.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## 📱 Pages

### Home Page
- Overview of the project
- Key statistics
- Feature highlights
- Call-to-action buttons

### Prediction Page
- Interactive form for input
- Real-time predictions
- User-friendly interface
- Error handling

### Analytics Dashboard
- Model performance metrics
- 6 interactive charts:
  - Delivery time distribution
  - Distance vs time correlation
  - Rating impact analysis
  - Vehicle type comparison
  - Order type analysis
  - Age group performance
- Key insights

### About Page
- Problem statement
- Solution approach
- Technical implementation
- Project workflow
- Business impact
- Future enhancements

## 🎯 Features Explained

### Input Features
- **Delivery Partner Age**: Age of the delivery person (18-65)
- **Delivery Partner Rating**: Rating score (1.0-5.0)
- **Distance**: Delivery distance in kilometers
- **Vehicle Type**: Motorcycle, Scooter, or Electric Vehicle
- **Order Type**: Snacks, Meal, Drinks, or Buffet

### Output
- **Predicted Delivery Time**: Estimated time in minutes

## 📈 Model Details

- **Algorithm**: Random Forest Regressor
- **Hyperparameters**:
  - n_estimators: 150
  - max_depth: 12
  - min_samples_split: 5
  - min_samples_leaf: 2
  - max_features: 'sqrt'
- **Data Preprocessing**:
  - Outlier removal using IQR method
  - Missing value handling
  - Duplicate removal
  - Feature scaling

## 🎨 Design Features

- Modern gradient backgrounds
- Smooth animations and transitions
- Card-based layout
- Responsive grid system
- Mobile-first approach
- Interactive hover effects
- Professional color scheme

## 🔮 Future Enhancements

- Real-time traffic data integration
- Weather condition analysis
- Time-of-day patterns
- Restaurant preparation time
- Deep learning models
- Mobile app development
- API for third-party integration

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created with ❤️ for the Food Delivery Time Estimation Project

---

**Note**: This is a machine learning project demonstrating end-to-end ML workflow from data preprocessing to deployment.
