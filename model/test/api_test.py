from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Загружаем модель
try:
    with open('lgb_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Модель загружена")
except Exception as e:
    print(f"❌ Ошибка загрузки модели: {e}")
    model = None

@app.route('/health', methods=['GET'])
def health():
    """Проверка доступности API"""
    return jsonify({"status": "ok"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Старый endpoint для одной строки (для совместимости)"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Empty data"}), 400

        features = [
            float(data.get('Age', 0)),
            int(data.get('Driving_License', 0)),
            int(data.get('Previously_Insured', 0)),
            float(data.get('Annual_Premium', 0)),
            int(data.get('Gender_Male', 0)),
            int(data.get('Vehicle_Damage_Yes', 0)),
            int(data.get('Vehicle_Age_1_2_Year', 0)),
            int(data.get('Vehicle_Age_lt_1_Year', 0)),
            int(data.get('Vehicle_Age_gt_2_Years', 0)),
        ]

        prediction = model.predict([features])[0]
        return jsonify({"prediction_numeric": int(prediction)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """НОВЫЙ endpoint для батча (отправляем 100 строк, получаем 100 предсказаний)"""
    try:
        data = request.json
        batch = data.get('data', [])

        if not batch:
            return jsonify({"predictions": []}), 200

        # Преобразуем в список признаков
        features_list = []
        for item in batch:
            features = [
                float(item.get('Age', 0)),
                int(item.get('Driving_License', 0)),
                int(item.get('Previously_Insured', 0)),
                float(item.get('Annual_Premium', 0)),
                int(item.get('Gender_Male', 0)),
                int(item.get('Vehicle_Damage_Yes', 0)),
                int(item.get('Vehicle_Age_1_2_Year', 0)),
                int(item.get('Vehicle_Age_lt_1_Year', 0)),
                int(item.get('Vehicle_Age_gt_2_Years', 0)),
            ]
            features_list.append(features)

        # Предсказываем весь батч сразу (это быстро!)
        predictions = model.predict(features_list)

        return jsonify({"predictions": predictions.tolist()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("🚀 Запуск Flask API на http://127.0.0.1:5000")
    print("Endpoints:")
    print("  GET  /health          - проверка доступности")
    print("  POST /predict         - одна строка")
    print("  POST /predict_batch   - 100 строк за раз")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
