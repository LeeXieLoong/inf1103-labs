FROM python:3.14-slim
COPY persistent_auditor.py /app/persistent_auditor.py
WORKDIR /data
CMD ["python", "-u", "/app/persistent_auditor.py"]
