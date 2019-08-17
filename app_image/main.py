import os
from fastai.text import load_learner
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

#learner_clf = load_learner('language_classifier_learner')


class IMDBLanguageModelDemo(Resource):
    def get(self):
        learner = load_learner('language_model_learner')

        #text = "My favorite part was when"
        text = "The best scene was"
        n_words = 25
        n_sentences = 12
        temp = .75
        output = ("\n".join(learner.predict(text, n_words, temperature=temp) for _ in range(n_sentences)))
        return output


class IMDBLanguageModelParse(Resource):

    def get(self):

        learner = load_learner('language_model_learner')

        temp = .75
        n_sentences = 1

        parser = reqparse.RequestParser()
        parser.add_argument('start_txt')
        parser.add_argument('n_words')
        request_body = parser.parse_args()
        try:
            if isinstance(request_body, str):
                request_body = json.loads(request_body)
            text = request_body['start_txt']
            n_words = int(request_body['n_words'])
        except:
            text = "the plot"
            n_words = 35

        output = ("\n".join(learner.predict(text, n_words, temperature=temp) for _ in range(n_sentences)))
        return output

api.add_resource(IMDBLanguageModelDemo, '/')
api.add_resource(IMDBLanguageModelParse, '/lm')
#api.add_resource(IMBDLanguageModelClass, '/rc')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))