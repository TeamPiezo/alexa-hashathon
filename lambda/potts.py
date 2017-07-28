from flask import Flask
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('HelloIntent')
def hello():
    speech_text = "Hello"
    return statement(speech_text).simple_card('Hello', speech_text)

@ask.launch
def launched():
    return question('Welcome to Potts, your own office assistant. Just like Tony Stark.')

if __name__ == '__main__':
    app.run()
