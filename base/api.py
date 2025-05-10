from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
import pickle
import numpy as np
import pandas as pd
import os
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def register_api(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)  # Auto-login the user
        
        return Response({
            'success': True,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data
        })
    return Response({
        'success': False,
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_api(request):
    logout(request)
    return Response({'success': True, 'message': 'Successfully logged out'}) 

@api_view(['POST'])
@csrf_exempt
def predict_api(request):
    try:
        # Extract form data
        data = request.data
        
        # Get all required fields
        try:
            age = int(data.get('age', 0))
            income = float(data.get('income', 0))
            loan_amount = float(data.get('loan_amount', 0))
            credit_score = int(data.get('credit_score', 0))
            months_employed = int(data.get('months_employed', 0))
            num_credit_lines = int(data.get('num_credit_lines', 0))
            interest_rate = float(data.get('interest_rate', 0))
            loan_term = int(data.get('loan_term', 0))
            dti_ratio = float(data.get('dti_ratio', 0))
            education = int(data.get('education', 1))
        except (ValueError, TypeError) as e:
            return Response({
                'success': False,
                'error': f"Invalid input data: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Boolean fields (convert checkbox values to boolean)
        has_mortgage = data.get('has_mortgage') == 'true' or data.get('has_mortgage') == True
        has_dependents = data.get('has_dependents') == 'true' or data.get('has_dependents') == True
        has_cosigner = data.get('has_cosigner') == 'true' or data.get('has_cosigner') == True
        
        # Special fields
        employment_type = data.get('employment_type')
        marital_status = data.get('marital_status')
        loan_purpose = data.get('purpose')
        
        # Calculate derived features
        loan_to_income_ratio = loan_amount / (income + 1e-5)
        monthly_loan_payment = loan_amount / (loan_term + 1e-5)
        credit_per_line = loan_amount / (num_credit_lines + 1e-5)
        
        # Create feature dictionary for one-hot encoding
        features = {
            'Age': age,
            'Income': income,
            'LoanAmount': loan_amount,
            'CreditScore': credit_score,
            'MonthsEmployed': months_employed,
            'NumCreditLines': num_credit_lines,
            'InterestRate': interest_rate,
            'LoanTerm': loan_term,
            'DTIRatio': dti_ratio,
            'Education': education,
            'HasMortgage': 1 if has_mortgage else 0,
            'HasDependents': 1 if has_dependents else 0,
            'HasCoSigner': 1 if has_cosigner else 0,
            'EmploymentType_Full-time': True if employment_type == 'Full-time' else False,
            'EmploymentType_Part-time': True if employment_type == 'Part-time' else False,
            'EmploymentType_Self-employed': True if employment_type == 'Self-employed' else False,
            'EmploymentType_Unemployed': True if employment_type == 'Unemployed' else False,
            'MaritalStatus_Divorced': True if marital_status == 'divorced' else False,
            'MaritalStatus_Married': True if marital_status == 'married' else False,
            'MaritalStatus_Single': True if marital_status == 'single' else False,
            'LoanPurpose_Auto': True if loan_purpose == 'Auto' else False,
            'LoanPurpose_Business': True if loan_purpose == 'Business' else False,
            'LoanPurpose_Education': True if loan_purpose == 'Education' else False,
            'LoanPurpose_Home': True if loan_purpose == 'Home' else False,
            'LoanPurpose_Other': True if loan_purpose == 'Other' else False,
            'LoanToIncomeRatio': loan_to_income_ratio,
            'MonthlyLoanPayment': monthly_loan_payment,
            'CreditPerLine': credit_per_line
        }
        
        # Convert to DataFrame for model input
        input_df = pd.DataFrame([features])

        # Load the model
        model_path = os.path.join('model', 'xgboost_model.pkl')

        try:
            model = pickle.load(open(model_path, 'rb'))
        except (FileNotFoundError, IOError) as e:
            return Response({
                'success': False,
                'error': f"Model file not found at {model_path}. Please ensure the model file exists."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'success': False,
                'error': f"Error loading model: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Make prediction
        probability = model.predict_proba(input_df)[0][1]  # Probability of class 1 (default)
        percentage = round(probability * 100, 2)
        
        # Determine risk level based on probability
        if percentage < 20:
            risk_level = "Low Risk"
        elif percentage < 50:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"
        
        return Response({
            'success': True,
            'probability': percentage,
            'risk_level': risk_level,
            'features': {
                'loan_to_income_ratio': round(loan_to_income_ratio, 2),
                'monthly_payment': round(monthly_loan_payment, 2),
                'credit_per_line': round(credit_per_line, 2)
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST) 