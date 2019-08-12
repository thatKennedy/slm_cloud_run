import os
from flask import Flask
from fastai.text import load_learner

#download_blob('fast-aing_cloudbuild', 'fastai_models/fine_tuned/export.pkl', 'fine_tuned/export.pkl')
learner = load_learner('language_model_learner')

app = Flask(__name__)

@app.route('/')
def preset_language_model():
    text = "I liked this movie because"
    n_words = 25
    n_sentences = 4
    temp = .75
    output = ("\n".join(learner.predict(text, n_words, temperature=temp) for _ in range(n_sentences)))
    return output


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))