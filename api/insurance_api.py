from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel, Field
import os

app = FastAPI()

# Загрузка модели
try:
    with open('lgb_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Модель загружена")
except Exception as e:
    print(f"❌ Ошибка загрузки модели: {e}")
    model = None

# Счетчик запросов
request_count = 0

class InsuranceInput(BaseModel):
    Age: float = Field(..., ge=18, le=100)
    Driving_License: int = Field(..., ge=0, le=1)
    Previously_Insured: int = Field(..., ge=0, le=1)
    Annual_Premium: float = Field(..., ge=0)
    Gender_Male: bool
    Vehicle_Damage_Yes: bool
    Vehicle_Age_1_2_Year: bool
    Vehicle_Age_lt_1_Year: bool
    Vehicle_Age_gt_2_Years: bool

@app.get("/")
def root():
    return {"message": "Insurance Prediction API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "OK" if model else "ERROR"}

@app.post("/predict")
def predict(input_data: InsuranceInput):
    global request_count

    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Проверка Vehicle Age
    vehicle_ages = [input_data.Vehicle_Age_1_2_Year,
                   input_data.Vehicle_Age_lt_1_Year,
                   input_data.Vehicle_Age_gt_2_Years]
    if sum(vehicle_ages) != 1:
        raise HTTPException(status_code=400, detail="Select exactly one Vehicle Age")

    try:
        request_count += 1

        # Создаем DataFrame
        new_data = pd.DataFrame([{
            'Age': float(input_data.Age),
            'Driving_License': int(input_data.Driving_License),
            'Previously_Insured': int(input_data.Previously_Insured),
            'Annual_Premium': float(input_data.Annual_Premium),
            'Gender_Male': 1 if input_data.Gender_Male else 0,
            'Vehicle_Damage_Yes': 1 if input_data.Vehicle_Damage_Yes else 0,
            'Vehicle_Age_1-2 Year': 1 if input_data.Vehicle_Age_1_2_Year else 0,
            'Vehicle_Age_< 1 Year': 1 if input_data.Vehicle_Age_lt_1_Year else 0,
            'Vehicle_Age_> 2 Years': 1 if input_data.Vehicle_Age_gt_2_Years else 0
        }])

        # Предсказание
        prediction = model.predict(new_data)[0]

        result = {
            "prediction": "Will buy" if prediction == 1 else "Will not buy",
            "prediction_numeric": int(prediction),
            "request_id": request_count
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    print("\n🚀 Insurance API starting on http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)