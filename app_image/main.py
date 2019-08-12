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


class IMBDLanguageModel_25n_words(Resource):

    def get(self):

        n_words = 25
        temp = .75

        parser = reqparse.RequestParser()
        parser.add_argument('start_txt')
        request_body = parser.parse_args()

        text = "My favorite part was when"

        try:
            text = dict(request_body['start_txt'])
        except:
            pass
        logger.info("Calling prediction on model")
        start_time = time.time()
        output = join(learner.predict(text, n_words, temperature=temp))
        logger.info("--- Inference time: %s seconds ---" % (time.time() - start_time))

        return output


api.add_resource(IMBDLanguageModelDemo, '/')
api.add_resource(IMBDLanguageModel_25n_words, '/25nw')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))