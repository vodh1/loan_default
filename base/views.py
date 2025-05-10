from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import auth_required

import pickle
import numpy as np
import pandas as pd
import os
import json


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'signup.html')

def get_model_statistics():
    """Load model statistics from the pickle file"""
    model_path = os.path.join('model', 'xgboost_model.pkl')
    try:
        # Load the model
        model = pickle.load(open(model_path, 'rb'))
        
        # Feature importance scores
        feature_scores = {
            'age': 93.50,
            'loan_to_income_ratio': 55.57,
            'interest_rate': 50.47,
            'months_employed': 33.31
        }
        
        # Calculate total score and percentages
        total_score = sum(feature_scores.values())
        feature_percentages = {
            key: round((value / total_score) * 100) 
            for key, value in feature_scores.items()
        }
        
        # Use the updated statistics provided by the user
        stats = {
            'total_records': 255347,
            'default_rate': 11.61,
            'avg_credit_score': 574.26,
            'avg_loan_amount': 127578.86,
            'defaulted_loans': 29653,
            'non_defaulted_loans': 225694,
            'feature_importance': feature_scores,
            'feature_percentages': feature_percentages,
            'model_info': {
                'total_features': 20,
                'categorical_features': 7,
                'numerical_features': 13,
                'missing_values': 0
            }
        }
        
        return stats
    except Exception as e:
        print(f"Error loading model statistics: {e}")
        return None

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def dashboard(request):
    """Load the dashboard with model statistics"""
    stats = get_model_statistics()
    
    if stats:
        context = {
            'user': request.user,
            'stats': stats,
            'total_records': stats['total_records'],
            'default_rate': stats['default_rate'],
            'avg_credit_score': stats['avg_credit_score'],
            'avg_loan_amount': stats['avg_loan_amount'],
            'defaulted_loans': stats['defaulted_loans'],
            'non_defaulted_loans': stats['non_defaulted_loans'],
            'default_percentage': stats['default_rate'],
            'non_default_percentage': 100 - stats['default_rate'],
        }
    else:
        # Fallback to static data if model loading fails
        context = {
            'user': request.user
        }
    
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def predict(request):
    """Loan default prediction page"""
    # This will be expanded later with the actual prediction form and logic
    return render(request, 'predict.html', {'user': request.user})