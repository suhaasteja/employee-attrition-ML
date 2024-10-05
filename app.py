from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)

# Load the trained model
try:
    model = pickle.load(open('attrition_model.pkl', 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")

# Define LabelEncoders (same as used in training)
label_encoders = {
    'BusinessTravel': LabelEncoder().fit(['Travel_Rarely', 'Travel_Frequently', 'Non-Travel']),
    'Department': LabelEncoder().fit(['Sales', 'Research & Development', 'Human Resources']),
    'EducationField': LabelEncoder().fit(['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other']),
    'Gender': LabelEncoder().fit(['Male', 'Female']),
    'JobRole': LabelEncoder().fit([
        'Sales Representative', 'Research Scientist', 'Laboratory Technician', 'Manufacturing Director',
        'Healthcare Representative', 'Manager', 'Human Resources', 'Sales Executive', 'Research Director'
    ]),
    'MaritalStatus': LabelEncoder().fit(['Single', 'Married', 'Divorced']),
    'OverTime': LabelEncoder().fit(['Yes', 'No']),
    'SalarySlab': LabelEncoder().fit(['Upto 5k', '5k-10k', '10k-20k', 'Above 20k'])
}

@app.route('/')
def index():
    return "Employee Attrition Prediction API is running"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)  # Log incoming data for debugging

        # Check if any field is missing
        required_fields = [
            'Age', 'BusinessTravel', 'Department', 'DistanceFromHome', 'Education',
            'EducationField', 'EnvironmentSatisfaction', 'Gender', 'HourlyRate', 'JobInvolvement',
            'JobLevel', 'JobRole', 'JobSatisfaction', 'MaritalStatus', 'MonthlyIncome',
            'NumCompaniesWorked', 'OverTime', 'PercentSalaryHike', 'RelationshipSatisfaction',
            'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
            'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
            'SalarySlab'
        ]
        
        # Check for missing fields and return error if any are missing
        for field in required_fields:
            if field not in data:
                print(f"Missing field: {field}")
                return jsonify({'error': f'Missing field in request: {field}'}), 400

        # Convert categorical fields using Label Encoding
        categorical_fields = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime', 'SalarySlab']
        for field in categorical_fields:
            if field in data:
                data[field] = label_encoders[field].transform([data[field]])[0]

        # Create feature array with same columns used in training (ensure matching column order)
        features = [
            data['Age'],  # Age (numeric)
            data['BusinessTravel'],  # BusinessTravel (label encoded)
            data['Department'],  # Department (label encoded)
            data['DistanceFromHome'],  # DistanceFromHome (numeric)
            data['Education'],  # Education (numeric)
            data['EducationField'],  # EducationField (label encoded)
            data['EnvironmentSatisfaction'],  # EnvironmentSatisfaction (numeric)
            data['Gender'],  # Gender (label encoded)
            data['HourlyRate'],  # HourlyRate (numeric)
            data['JobInvolvement'],  # JobInvolvement (numeric)
            data['JobLevel'],  # JobLevel (numeric)
            data['JobRole'],  # JobRole (label encoded)
            data['JobSatisfaction'],  # JobSatisfaction (numeric)
            data['MaritalStatus'],  # MaritalStatus (label encoded)
            data['MonthlyIncome'],  # MonthlyIncome (numeric)
            data['NumCompaniesWorked'],  # NumCompaniesWorked (numeric)
            data['OverTime'],  # OverTime (label encoded)
            data['PercentSalaryHike'],  # PercentSalaryHike (numeric)
            data['RelationshipSatisfaction'],  # RelationshipSatisfaction (numeric)
            data['StockOptionLevel'],  # StockOptionLevel (numeric)
            data['TotalWorkingYears'],  # TotalWorkingYears (numeric)
            data['TrainingTimesLastYear'],  # TrainingTimesLastYear (numeric)
            data['WorkLifeBalance'],  # WorkLifeBalance (numeric)
            data['YearsAtCompany'],  # YearsAtCompany (numeric)
            data['YearsInCurrentRole'],  # YearsInCurrentRole (numeric)
            data['YearsSinceLastPromotion'],  # YearsSinceLastPromotion (numeric)
            data['YearsWithCurrManager'],  # YearsWithCurrManager (numeric)
            data['SalarySlab']  # SalarySlab (label encoded)
        ]

        # If the model expects more features, pad with zeros
        expected_features = 33  # Adjust this number to match the expected number of features in the model
        if len(features) < expected_features:
            features += [0] * (expected_features - len(features))  # Add zeros to match the required number of features

        # Convert features into NumPy array and reshape for prediction
        input_data = np.array(features).reshape(1, -1)

        # Make prediction using the model
        prediction = model.predict(input_data)[0]

        # Return the prediction as a JSON response
        return jsonify({'prediction': int(prediction)})

    except KeyError as e:
        print(f"KeyError: Missing field {str(e)}")
        return jsonify({'error': f'Missing field in request: {str(e)}'}), 400
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
