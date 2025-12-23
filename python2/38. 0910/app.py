from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['Get','POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        features = np.array([[
            data['Age'], 
            data['Gender_Encoded'], 
            data['Blood_Pressure'], 
            data['Cholesterol']
        ]], dtype=float)
        print('features 0 : ',features)
        # 정규화
        scaler = joblib.load(r'C:\Temp\2025\python2\38. 0910\blood_cholesterol.scaler')
        # 3) Blood_Pressure(2번째 인덱스=2), Cholesterol(3번째 인덱스=3)만 변환
        features[:, [2, 3]] = scaler.transform(features[:, [2, 3]])
        print('features 1 : ',features)
        # 모델로 예측
        model = joblib.load(r'C:\Temp\2025\python2\38. 0910\diabetes_model.pkl')
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features).max())
        
        # 추론 결과를 JSON으로 반환
        return jsonify({
            'Age' : data['Age'],
            'Blood_Pressure' : data['Blood_Pressure'],
            'Cholesterol' : data['Cholesterol'],
            'Gender' : '남성' if data['Gender_Encoded'] ==1 else '여성',
            'prediction': '당뇨병' if prediction == 1 else '당뇨병 아님',
            'probability': probability})

if __name__ == '__main__':
    app.run(port = 5001, debug=True)