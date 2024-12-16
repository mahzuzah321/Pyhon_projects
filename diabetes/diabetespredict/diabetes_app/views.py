from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import joblib
import numpy as np
import os

# Define the path to the model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'diabetes_model.pkl')

# Load the model
model = joblib.load(MODEL_PATH)

def predict(request):
    if request.method == 'POST':
        try:
            data = request.POST
            # Extract and validate features from the request
            features = [
                'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
            ]
            input_data = []
            for feature in features:
                if feature not in data:
                    return HttpResponseBadRequest(f'Missing feature: {feature}')
                try:
                    input_data.append(float(data[feature]))
                except ValueError:
                    return HttpResponseBadRequest(f'Invalid value for feature: {feature}')
            
            # Convert to numpy array and reshape for model input
            input_array = np.array([input_data])
            
            # Make prediction
            prediction = model.predict(input_array)
            
            # Determine the message based on prediction
            if prediction[0] == 1:
                message = "1<br> The person has diabetes."
            else:
                message = "0<br> The person does not have diabetes."
            
            # Render the result template with the prediction and message
            context = {
                'prediction': int(prediction[0]),
                'message': message
            }
            return render(request, 'result.html', context)
        
        except Exception as e:
            return HttpResponseBadRequest(f'Error processing request: {str(e)}')
    else:
        return render(request, 'predict.html')
