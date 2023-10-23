from flask import Flask, render_template, request, render_template_string
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=["POST"])
def result():
    title = request.form.get("title")
    instructions = request.form.get("instructions")

    final = "generate a tutorial for the topic:" + title + \
        " with instructions as follows: " + instructions + ". use html to write it."

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "mistral",
        "prompt": final
    }

    response = requests.post(url, data=json.dumps(data), stream=True)

    response_values = ""

    for line in response.iter_lines():
        if line:
            line = line.rstrip()
            response_json = json.loads(line)
            response_value = response_json.get('response')
            if response_value is not None:
                response_values += response_value
            else:
                break

    return render_template_string(response_values)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
