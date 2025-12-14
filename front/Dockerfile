FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for better caching
COPY requirement.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirement.txt

# Copy the application
COPY streamlit_app_fixed.py .

# Expose Streamlit port
EXPOSE 8501

# Create directory for Streamlit config
RUN mkdir -p ~/.streamlit && \
    echo "[client]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Health check (fixed syntax)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501', timeout=5)" || exit 1

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app_fixed.py"]