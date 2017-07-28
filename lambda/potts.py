from flask import Flask, render_template
from flask_ask import Ask, session, statement, question
import requests
import json
import time

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('HelloIntent')
def hello():
    speech_text = 'Hello'
    return statement(speech_text).simple_card('Hello', speech_text)


@ask.intent('FindSlot')
def find_slot(date=None):
    speech_text = 'These are the '
    # Make request here
    if not date:
        session.attributes['stage'] = 'book_slot'
        return question('You didn\'t specify the date. What date you would like to book?')
    else:
        # Make request to
        session.attributes['stage'] = 'find_slot'
        session.attributes['date'] = date
        return question('These are free slots for ' + date + ' Which one do you want me to book?')


@ask.intent('DateIntent')
def get_date(date):
    stage = session.attributes['stage']
    if stage == 'find_slot':
        return find_slot(date)


@ask.intent('BookSlot')
def book_slot(time=None):
    speech_text = 'These are the '
    # Make request here
    if not time:
        return question('You didn\'t specify the date. What date you would like to book?')
    else:
        # Make request to API
        session.attributes['stage'] = 'book_slot'
        return question('I have booked this room for ' + time + '. Are you sure?')


@ask.intent('AMAZON.YesIntent')
def confirm_request():
    stage = session.attributes['stage']
    if stage == 'book_slot':
        return statement('OK. Booked.')
    elif stage == '':
        return statement('Bye.')
    else:
        return statement('Bye.')


@ask.intent('AMAZON.NoIntent')
def confirm_request():
    stage = session.attributes['stage']
    if stage == 'finding_slot':
        return statement('OK. If you don\'nt want to book, bye!')
    elif stage == '':
        return statement('Bye.')
    else:
        return statement('Bye.')


@ask.intent('AMAZON.CancelIntent')
def terminate():
    return statement('Bye.')


@ask.launch
def launched():
    welcome_msg = 'Welcome to Potts, your own office assistant. Just like Tony Stark.'
    return question(welcome_msg)

if __name__ == '__main__':
    app.run(debug=True)
