# Loan Default Prediction System

A web application for predicting loan defaults using machine learning.

## Overview

This project combines a Django web application with an XGBoost machine learning model to predict the likelihood of loan defaults. The system allows users to:

1. Register and login to access the application
2. View dashboard analytics about loan default statistics
3. Submit loan applications and get real-time default risk predictions

## Project Structure

```
loan_default_prediction/
├── base/                       # Django app with core functionality
│   ├── api.py                  # API endpoints for prediction and auth
│   ├── views.py                # Web view handlers
│   ├── utils.py                # Utility functions
│   ├── urls.py                 # URL routing
│   └── models.py               # Database models
├── model/                      # Machine learning components
│   ├── main.ipynb              # Data analysis and model development notebook
│   ├── xgboost_model.pkl       # Trained XGBoost model
│   └── loan_default.csv        # Dataset for model training
├── templates/                  # HTML templates
│   ├── base.html               # Base template with common elements
│   ├── dashboard.html          # Dashboard analytics view
│   ├── predict.html            # Prediction form and results
│   ├── home.html               # Landing page
│   ├── login.html              # Login page
│   └── signup.html             # Registration page
├── django_project/             # Django project settings
│   └── settings.py             # Project configuration
├── manage.py                   # Django command-line utility
└── db.sqlite3                  # SQLite database
```

## Machine Learning Model

The loan default prediction model was built using the following workflow:

1. **Data Collection**: A dataset with 255,347 loan records was used
2. **Exploratory Data Analysis**: Analyzed relationships between variables
3. **Feature Engineering**: Created derived features like loan-to-income ratio
4. **Model Training**: Used XGBoost algorithm with hyperparameter tuning
5. **Model Evaluation**: Achieved strong prediction performance with key metrics:
   - Default rate in dataset: 11.61%
   - Model performance metrics available in the dashboard

### Key Features Used in Prediction

- Age (93.50 importance)
- Loan-to-income ratio (55.57 importance)
- Interest rate (50.46 importance)
- Months employed (33.31 importance)
- Additional features: credit score, loan amount, DTI ratio, employment type, etc.

## Web Application

The Django application provides a user-friendly interface for interacting with the prediction model.

### Key Components

1. **Authentication System**
   - User registration and login functionality
   - Protected routes for authenticated users

2. **Dashboard**
   - Visual analytics showing dataset statistics
   - Distribution of defaulted vs. non-defaulted loans
   - Feature importance visualization
   - Key metrics summary

3. **Prediction Interface**
   - Form to input borrower and loan information
   - Real-time prediction results with risk level
   - Visual explanation of prediction factors

## Installation and Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd loan-default-prediction
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

5. Access the application at `http://localhost:8000`

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Data Analysis**: Pandas, NumPy, Seaborn, Matplotlib
- **Machine Learning**: Scikit-learn, XGBoost, imbalanced-learn
- **Database**: SQLite

## Model Development Details

The machine learning model was developed in Jupyter Notebook (`model/main.ipynb`) with the following steps:

1. **Data Loading and Cleaning**:
   - Loaded dataset with 255,347 records
   - No missing values were found
   - Verified data types and distributions

2. **Exploratory Data Analysis**:
   - Analyzed feature distributions and relationships
   - Identified class imbalance (11.61% default rate)
   - Created visualizations to understand feature importance

3. **Feature Engineering**:
   - Created derived features like loan-to-income ratio
   - Encoded categorical variables
   - Normalized numerical features

4. **Model Development**:
   - Undersampling to address class imbalance
   - Trained multiple models (Decision Tree, Random Forest, XGBoost)
   - XGBoost performed best and was selected as the final model

5. **Model Evaluation**:
   - Used precision, recall, F1-score, and ROC-AUC metrics
   - Analyzed feature importance for model interpretability

## API Endpoints

- `/api/register/` - User registration
- `/api/login/` - User authentication
- `/api/logout/` - User logout
- `/api/predict/` - Loan default prediction

## Future Improvements
- Add more advanced feature engineering

