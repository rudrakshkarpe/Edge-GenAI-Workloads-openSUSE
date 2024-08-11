FROM python:3.10-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python depend"encies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install application into container
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Setup a health check against Streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
# ENTRYPOINT ["python", "-m", "streamlit"]
# CMD ["run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]z
