FROM python:3.14-slim
COPY inventory_manager.py /app/inventory_manager.py
WORKDIR /data
CMD ["python", "-u", "/app/inventory_manager.py"]
