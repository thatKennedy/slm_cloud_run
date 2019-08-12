import os
from fastai.text import load_learner
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

learner = load_learner('language_model_learner')

class IMBDLanguageModelDemo(Resource):
    def get(self):
        text = "My favorite part was when"
        n_words = 25
        n_sentences = 25
        temp = .75
        output = ("\n".join(learner.predict(text, n_words, temperature=temp) for _ in range(n_sentences)))
        return output


class IMBDLanguageModel_3s_words(Resource):

    def get(self):

        n_words = 25
        n_sentences = 3
        temp = .75

        parser = reqparse.RequestParser()
        parser.add_argument('start_txt')
        request_body = parser.parse_args()

        if isinstance(request_body, str):
            request_body = json.loads(request_body)
        text = requests.get(request_body['start_txt'], stream=True)

        output = ("\n".join(learner.predict(text, n_words, temperature=temp) for _ in range(n_sentences)))
        return output

api.add_resource(IMBDLanguageModelDemo, '/')
api.add_resource(IMBDLanguageModel_3s_words, '/3')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))