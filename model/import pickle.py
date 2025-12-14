import pickle
import pandas as pd

# Загрузите модель
with open('lgb_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("Модель загружена успешно")
print(f"Тип модели: {type(model)}")

# Создайте тестовые данные
test_data = pd.DataFrame([{
    'Age': 35.0,
    'Driving_License': 1,
    'Previously_Insured': 0,
    'Annual_Premium': 2500.0,
    'Gender_Male': 1,
    'Vehicle_Damage_Yes': 1,
    'Vehicle_Age_1-2 Year': 1,
    'Vehicle_Age_< 1 Year': 0,
    'Vehicle_Age_> 2 Years': 0
}])

print(f"\nДанные для предсказания:")
print(test_data)

print(f"\nСтолбцы: {test_data.columns.tolist()}")

# Попробуйте предсказание
try:
    prediction = model.predict(test_data)
    print(f"\nПредсказание: {prediction}")
except Exception as e:
    print(f"\nОшибка при предсказании: {e}")