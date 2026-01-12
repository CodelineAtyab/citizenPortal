# 1. Test stage
FROM python:3.11-alpine AS test
WORKDIR /app
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY . .
RUN pytest -v
RUN touch /tmp/tests-passed

# 2. Production stage
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

COPY --from=test /tmp/tests-passed /tmp/tests-passed

CMD ["python", "main.py"]