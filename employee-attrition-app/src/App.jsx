import React, { useState } from 'react';
import axios from 'axios';

function App() {
  // List of fields with default values
  const fieldData = [
    { name: 'Age', label: 'Age', type: 'number', defaultValue: 18 },
    { name: 'BusinessTravel', label: 'Business Travel', type: 'text', defaultValue: 'Travel_Rarely' },
    { name: 'Department', label: 'Department', type: 'text', defaultValue: 'Sales' },
    { name: 'DistanceFromHome', label: 'Distance From Home', type: 'number', defaultValue: 10 },
    { name: 'Education', label: 'Education', type: 'number', defaultValue: 3 },
    { name: 'EducationField', label: 'Education Field', type: 'text', defaultValue: 'Medical' },
    { name: 'EnvironmentSatisfaction', label: 'Environment Satisfaction', type: 'number', defaultValue: 3 },
    { name: 'Gender', label: 'Gender', type: 'text', defaultValue: 'Female' },
    { name: 'HourlyRate', label: 'Hourly Rate', type: 'number', defaultValue: 69 },
    { name: 'JobInvolvement', label: 'Job Involvement', type: 'number', defaultValue: 2 },
    { name: 'JobLevel', label: 'Job Level', type: 'number', defaultValue: 1 },
    { name: 'JobRole', label: 'Job Role', type: 'text', defaultValue: 'Sales Representative' },
    { name: 'JobSatisfaction', label: 'Job Satisfaction', type: 'number', defaultValue: 3 },
    { name: 'MaritalStatus', label: 'Marital Status', type: 'text', defaultValue: 'Single' },
    { name: 'MonthlyIncome', label: 'Monthly Income', type: 'number', defaultValue: 1200 },
    { name: 'NumCompaniesWorked', label: 'Number of Companies Worked', type: 'number', defaultValue: 1 },
    { name: 'OverTime', label: 'Over Time', type: 'text', defaultValue: 'No' },
    { name: 'PercentSalaryHike', label: 'Percent Salary Hike', type: 'number', defaultValue: 12 },
    { name: 'RelationshipSatisfaction', label: 'Relationship Satisfaction', type: 'number', defaultValue: 3 },
    { name: 'StockOptionLevel', label: 'Stock Option Level', type: 'number', defaultValue: 0 },
    { name: 'TotalWorkingYears', label: 'Total Working Years', type: 'number', defaultValue: 0 },
    { name: 'TrainingTimesLastYear', label: 'Training Times Last Year', type: 'number', defaultValue: 2 },
    { name: 'WorkLifeBalance', label: 'Work Life Balance', type: 'number', defaultValue: 3 },
    { name: 'YearsAtCompany', label: 'Years at Company', type: 'number', defaultValue: 0 },
    { name: 'YearsInCurrentRole', label: 'Years in Current Role', type: 'number', defaultValue: 0 },
    { name: 'YearsSinceLastPromotion', label: 'Years Since Last Promotion', type: 'number', defaultValue: 0 },
    { name: 'YearsWithCurrManager', label: 'Years with Current Manager', type: 'number', defaultValue: 0 },
    // Added SalarySlab field
    { name: 'SalarySlab', label: 'Salary Slab', type: 'select', defaultValue: 'Upto 5k' }
  ];

  const [employeeData, setEmployeeData] = useState(
    fieldData.reduce((acc, field) => {
      acc[field.name] = field.defaultValue;
      return acc;
    }, {})
  );

  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEmployeeData({ ...employeeData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', employeeData);
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Error making prediction:', error);
    }
  };

  return (
    <div className="App">
      <h1>Employee Attrition Prediction</h1>
      <form onSubmit={handleSubmit}>
        {/* Dynamically generating form fields */}
        {fieldData.map((field) => (
          <div key={field.name}>
            <label>{field.label}: </label>
            {field.type === 'select' ? (
              <select
                name={field.name}
                value={employeeData[field.name]}
                onChange={handleChange}
              >
                <option value="Upto 5k">Upto 5k</option>
                <option value="5k-10k">5k-10k</option>
                <option value="10k-20k">10k-20k</option>
                <option value="Above 20k">Above 20k</option>
              </select>
            ) : (
              <input
                type={field.type}
                name={field.name}
                value={employeeData[field.name]}
                onChange={handleChange}
              />
            )}
          </div>
        ))}
        <button type="submit">Predict Attrition</button>
      </form>

      {/* Display Prediction */}
      {prediction !== null && (
        <div>
          <h2>Prediction: {prediction === 1 ? 'Will Leave' : 'Will Stay'}</h2>
        </div>
      )}
    </div>
  );
}

export default App;
