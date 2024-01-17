from bottle import Bottle, request, response
import json
from nlp import classify_sentence  # Make sure to import the function correctly

app = Bottle()


@app.post('/classify')
def classify_text():
    try:
        # Parse input data
        data = request.json
        text = data.get('text')
        if not text:
            raise ValueError("No text provided.")

        # Use the NLP function to classify the text
        result = classify_sentence(text)

        # Prepare the response
        return json.dumps({'classification': result})
    except Exception as e:
        response.status = 400
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
