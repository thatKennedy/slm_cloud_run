FROM gcr.io/fast-aing/base_slm
COPY main.py .
CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 main:app
