import os
from fastai.text import load_learner
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

learner = load_learner('language_model_learner')


class IMBDLanguageModelDemo(Resource):
    def get(self):
        text = "I liked this movie because"
        n_words = 25
        n_sentences = 4
        temp = .75
        output = ("\n".join(learner.predict(text, n_words, temperature=temp) for _ in range(n_sentences)))
        return output


api.add_resource(IMBDLanguageModelDemo, '/')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))