from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import os

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

# Ensure 'uploads/' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            writing_score=float(request.form.get('writing_score')),
            reading_score=float(request.form.get('reading_score')),

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")
        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])

@app.route('/predictbulk', methods=['GET', 'POST'])
def predict_bulk():
    if request.method == 'GET':
        return render_template('bulk_predict.html')
    else:
        try:
            file = request.files['file']
            if not file or not file.filename.endswith('.csv'):
                return "Invalid file format. Please upload a CSV file.", 400

            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Load the CSV as DataFrame
            data = pd.read_csv(file_path)

            # Predict using bulk file
            predict_pipeline = PredictPipeline()
            predictions = predict_pipeline.predict(data)

            # Combine input data and predictions
            data['Predictions'] = predictions
            results = data.to_dict(orient='records')  # Convert DataFrame to list of dicts

            # Render results
            return render_template('bulk_predict.html', results=results)
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)        


