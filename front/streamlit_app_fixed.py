import streamlit as st
import requests
import json
from datetime import datetime

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="🛡️ Insurance Prediction",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== Custom CSS ====================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 1rem;
    }
    .prediction-yes {
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
    }
    .prediction-no {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
    }
    .error-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin-top: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin-top: 1rem;
    }
    .form-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# ==================== API Configuration ====================
# Исправлено: правильная работа с secrets
import os

API_BASE_URL = os.getenv("API_URL", "http://api:5000")


# ==================== Header ====================
st.title("🛡️ Insurance Prediction System")
st.markdown("Предскажите вероятность покупки полиса страхования транспортного средства")

# ==================== Sidebar ====================
st.sidebar.markdown("## ⚙️ Настройки")
api_url = st.sidebar.text_input("API URL", value=API_BASE_URL)

# Кнопка проверки статуса API
if st.sidebar.button("🔍 Проверить статус API"):
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get("status") == "OK":
                st.sidebar.success("✅ API работает корректно")
            else:
                st.sidebar.warning("⚠️ API работает, но модель не загружена")
    except Exception as e:
        st.sidebar.error(f"❌ Ошибка подключения: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Информация")
st.sidebar.info(
    "Это приложение использует модель машинного обучения LightGBM "
    "для предсказания вероятности покупки страховки клиентом."
)

# ==================== Main Form ====================
st.markdown("### 📝 Заполните данные клиента")

with st.form(key="prediction_form"):
    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Личные данные")
        age = st.number_input(
            "Возраст",
            min_value=18,
            max_value=100,
            value=30,
            help="Возраст клиента (18-100 лет)"
        )

        driving_license = st.selectbox(
            "Водительское удостоверение",
            options=[0, 1],
            format_func=lambda x: "✅ Есть" if x == 1 else "❌ Нет",
            help="Наличие водительского удостоверения"
        )

        previously_insured = st.selectbox(
            "Ранее застрахован",
            options=[0, 1],
            format_func=lambda x: "✅ Да" if x == 1 else "❌ Нет",
            help="Был ли ранее застрахован"
        )

        gender_male = st.checkbox(
            "Мужчина",
            value=True,
            help="Отметьте, если клиент - мужчина"
        )

    with col2:
        st.subheader("🚗 Данные об автомобиле")
        annual_premium = st.number_input(
            "Стоимость страховки (₽)",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
            help="Годовая страховая премия в рублях"
        )

        vehicle_damage = st.checkbox(
            "Повреждение транспорта",
            value=False,
            help="Был ли транспорт поврежден в прошлом"
        )

        st.subheader("🔧 Возраст транспорта")
        vehicle_age_option = st.radio(
            "Выберите возраст транспорта",
            options=["< 1 года", "1-2 года", "> 2 лет"],
            help="Возраст транспортного средства"
        )

        # Map the selection to boolean values
        vehicle_age_lt_1 = vehicle_age_option == "< 1 года"
        vehicle_age_1_2 = vehicle_age_option == "1-2 года"
        vehicle_age_gt_2 = vehicle_age_option == "> 2 лет"

    # ==================== Submit Button ====================
    st.markdown("---")
    submit_button = st.form_submit_button(
        "🔮 Сделать предсказание",
        use_container_width=True
    )

# ==================== Prediction Logic ====================
if submit_button:
    # Validate input
    if not (vehicle_age_lt_1 or vehicle_age_1_2 or vehicle_age_gt_2):
        st.error("❌ Пожалуйста, выберите возраст транспорта")
    else:
        # Prepare request data
        request_data = {
            "Age": float(age),
            "Driving_License": int(driving_license),
            "Previously_Insured": int(previously_insured),
            "Annual_Premium": float(annual_premium),
            "Gender_Male": bool(gender_male),
            "Vehicle_Damage_Yes": bool(vehicle_damage),
            "Vehicle_Age_1_2_Year": vehicle_age_1_2,
            "Vehicle_Age_lt_1_Year": vehicle_age_lt_1,
            "Vehicle_Age_gt_2_Years": vehicle_age_gt_2
        }

        try:
            # Make API request
            with st.spinner("⏳ Обработка запроса..."):
                response = requests.post(
                    f"{api_url}/predict",
                    json=request_data,
                    timeout=10
                )

            # Handle response
            if response.status_code == 200:
                result = response.json()

                # Display results
                st.success("✅ Предсказание выполнено успешно!")

                col1, col2 = st.columns(2)

                with col1:
                    # Prediction result
                    prediction = result.get("prediction_numeric", 0)
                    prediction_text = result.get("prediction", "Unknown")

                    if prediction == 1:
                        st.markdown(
                            f'<div class="prediction-box prediction-yes">✅ {prediction_text}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="prediction-box prediction-no">❌ {prediction_text}</div>',
                            unsafe_allow_html=True
                        )

                with col2:
                    st.metric(
                        "ID запроса",
                        result.get("request_id", "N/A"),
                        delta=None
                    )

                # Detailed information
                st.markdown("### 📋 Детали предсказания")
                info_col1, info_col2 = st.columns(2)

                with info_col1:
                    st.write(f"**Возраст:** {age} лет")
                    st.write(f"**Водительское удостоверение:** {'✅ Есть' if driving_license else '❌ Нет'}")
                    st.write(f"**Ранее застрахован:** {'✅ Да' if previously_insured else '❌ Нет'}")

                with info_col2:
                    st.write(f"**Годовая премия:** ₽{annual_premium:,.0f}")
                    st.write(f"**Повреждение транспорта:** {'✅ Да' if vehicle_damage else '❌ Нет'}")
                    st.write(f"**Возраст транспорта:** {vehicle_age_option}")

                # Success message
                st.markdown(
                    '<div class="info-box">💡 Результат сохранен в истории запросов</div>',
                    unsafe_allow_html=True
                )

            else:
                # API error response
                error_detail = response.json().get("detail", "Unknown error")
                st.error(f"❌ Ошибка API: {error_detail}")

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Не удалось подключиться к API. "
                f"Убедитесь, что API запущена на {api_url}"
            )
        except requests.exceptions.Timeout:
            st.error("❌ Время ожидания ответа от API истекло")
        except Exception as e:
            st.error(f"❌ Неожиданная ошибка: {str(e)}")

# ==================== Footer ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🛡️ Insurance Prediction System v1.0</p>
    <p>Разработано с использованием Streamlit и FastAPI</p>
</div>
""", unsafe_allow_html=True)
