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


# Actions

@ask.intent('FindSlot')
def find_slot(date=None):
    """
    If date is provided, find the free slots. Else ask for date and track using stage=='find_slot'
    :param date:
    :return:
    """
    if not date:
        session.attributes['stage'] = 'book_slot'
        return question('You didn\'t specify the date. What date you would like to book?')
    else:
        # Make request to api to book
        session.attributes['stage'] = 'find_slot'
        session.attributes['date'] = date
        return question('These are free slots for ' + date + ' Which one do you want me to book?')


@ask.intent('BookSlot')
def book_slot(slot_time=None):
    """
    If time is provided, book for that time. Else ask the user to try again.
    :param slot_time:
    :return:
    """
    # Make request here
    if not slot_time:
        return question('You didn\'t specify the time. Try again.')
    else:
        # Make request to API
        session.attributes['stage'] = 'book_slot'
        return question('I have booked this room for ' + slot_time + '. Are you sure?')


@ask.intent('StartMeeting')
def start_meeting():
    """

    :return:
    """
    # Send request to API to begin session and get current user
    meeting = {}
    return statement('Meeting has been started for .')

# Contextual Intents

@ask.intent('DateIntent')
def get_date(date):
    stage = session.attributes['stage']
    if stage == 'find_slot':
        return find_slot(date)


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
