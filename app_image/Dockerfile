FROM gcr.io/fast-aing/base_slm

COPY language_model_learner language_model_learner
COPY main.py main.py

CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 main:app
