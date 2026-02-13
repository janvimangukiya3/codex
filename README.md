# codex — Food Delivery Time Predictor

An AI-powered web application that predicts food delivery times using machine learning. Built with Flask, scikit-learn/XGBoost, and modern web technologies.

## ✨ Features

- Machine Learning Prediction (RandomForest / XGBoost)
- Interactive Dashboard with Plotly charts
- Responsive UI and prediction interface
- Pre-trained model included (`delivery_model.pkl`)

## 📁 Project Structure

```
├── app.py
├── train_model.py
├── train_model_improved.py
├── Dataset.csv
├── delivery_model.pkl
├── model_columns.pkl
├── requirements.txt
├── static/
└── Templates/
```

## 🚀 Quick Start

```powershell
cd /d E:\final\Hackathon\Hackathon\Hackathon
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## 🎯 Input Features

- `Delivery_person_Age`
- `Delivery_person_Ratings`
- `Type_of_order` (0..3)
- `Type_of_vehicle` (1..3)
- `Distance_km`

Derived features used in some training scripts: `Distance_sq`, `Distance_log`

## 📈 Model

- Target: `Delivery_Time`
- Preprocessing: duplicate removal, drop NA, outlier removal (IQR)

## 📄 License

Educational/demo project.

## 👨‍💻 Author

Janvi Mangukiya

