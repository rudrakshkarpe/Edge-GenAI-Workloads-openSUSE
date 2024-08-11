FROM python:3.10-slim as base

FROM base AS python-deps

# Install compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base AS runtime

# Copy installed dependencies from python-deps stage
COPY --from=python-deps /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Install application into container
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Setup a health check against Streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["python", "-m", "streamlit"]
CMD ["run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]