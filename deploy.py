import pickle
import pandas as pd
from flask import Flask, request, render_template

# Load the saved model (make sure to have your model in the correct path)
model = pickle.load(open('saved_model.sav', 'rb'))

# Initialize the Flask application
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve input values from the form
        amount = request.form.get('amount', '').strip()
        feature_1 = request.form.get('feature_1', '').strip()
        feature_2 = request.form.get('feature_2', '').strip()
        feature_3 = request.form.get('feature_3', '').strip()
        feature_4 = request.form.get('feature_4', '').strip()

        # Ensure all fields are provided
        if not amount or not feature_1 or not feature_2 or not feature_3 or not feature_4:
            return render_template('index.html', result="Error: All fields are required!")

        # Convert inputs to float (ensure they are valid numeric values)
        amount = float(amount)
        feature_1 = float(feature_1)
        feature_2 = float(feature_2)
        feature_3 = float(feature_3)
        feature_4 = float(feature_4)

        # Create a DataFrame with the input features
        feature_names = ['Amount', 'Feature_1', 'Feature_2', 'Feature_3', 'Feature_4']
        input_features = pd.DataFrame([[amount, feature_1, feature_2, feature_3, feature_4]], columns=feature_names)

        # Make prediction using the model
        result = model.predict(input_features)[0]

        # Return result to the user
        return render_template('index.html', result=f"Fraud Status: {'Fraud' if result == 1 else 'Not Fraud'}")

    except ValueError:
        return render_template('index.html', result="Error: Please enter valid numeric values!")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
