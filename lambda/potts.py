from flask import Flask, render_template
from flask_ask import Ask, session, statement, question
from slack import post_message
from helper import get_time_strings
import requests
import json
import config
from datetime import datetime

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('HelloIntent')
def handle_hello():
    speech_text = 'Hello'
    return statement(speech_text).simple_card('Hello', speech_text)


# Actions

@ask.intent('FindSlot')
def handle_find_slot(date=None):
    """
    If date is provided, find the free slots. Else ask for date and track using stage=='find_slot'
    :param date:
    :return:
    """
    if not date:
        session.attributes['stage'] = 'book_slot'
        return question('You didn\'t specify the date. What date you would like to book?')
    else:
        print(date)
        params = {
            'date': date
        }
        req = requests.get(config.API + '/find_slot', params=params)
        print(req.text)
        freeslots_string = get_time_strings(json.loads(req.text)['freesloats'])
        session.attributes['stage'] = 'find_slot'
        session.attributes['date'] = date
        return question('The free slots for ' + date + ' are '+ freeslots_string + ' Which one do you want me to book?')


@ask.intent('BookSlot')
def handle_book_slot(time=None, name='default'):
    """
    If time is provided, book for that time. Else ask the user to try again.
    :param slot_time:
    :return:
    """
    # Make request here

    if not time:
        return question('You didn\'t specify the time. Try again.')
    else:
        slot_date = session.attributes.get('date', None)
        params = {
            'starttime': time,
            'bookedbyuser': name,
            'date': slot_date
        }
        print(params)
        session.attributes['stage'] = 'book_slot'
        session.attributes['slot_params'] = params
        return question('You want to book at ' + time + ' Is that correct?')


@ask.intent('StartMeeting')
def handle_start_meeting():
    """

    :return:
    """
    req = requests.get(config.API + '/start_meeting')
    return statement('Meeting has been started for')


@ask.intent('EndMeeting')
def handle_end_meeting():
    """

    :return:
    """
    # Get meeting details
    req = requests.get(config.API + '/meeting/end')
    reply = 'The meeting has been marked ended.'
    return statement(reply)


@ask.intent('CancelSlot', mapping={'slot_date': 'date', 'slot_time': 'time'})
def handle_cancel_slot(slot_date, slot_time):
    """

    :return:
    """
    params = {
        'slot_date': slot_date,
        'slot_time': slot_time
    }
    req = requests.get(config.API + '/cancel_slot', params=params)
    status = json.loads(req.text)['status']
    if status == 'success':
        return statement('The task at ' + slot_date + ' ' + slot_time + ' has been cancelled.')
    elif status == 'not_exist':
        return statement('There is no task at this time.')
    return question('Error. Try again.')


@ask.intent('UndoTask')
def handle_undo_task():
    """

    :return:
    """
    # Send call to API for deleting (or whatever marking) the last added-task
    req = requests.get(config.API + '/undo_task')
    return statement('Your last added task has been deleted')


@ask.intent('AssignTask')
def handle_assign_task(task, userp=''):
    """

    :return:
    """
    post_message(task, userp)
    reply = 'Task has been assigned to ' + userp
    return statement(reply)


# Contextual Intents

@ask.intent('DateIntent')
def get_date(date):
    stage = session.attributes['stage']
    if stage == 'find_slot':
        return handle_find_slot(date)


@ask.intent('AMAZON.YesIntent')
def confirm_request():
    stage = session.attributes['stage']
    if stage == 'book_slot':
        params = session.attributes['slot_params']
        req = requests.get(config.API + '/book_slot', params=params)
        if json.loads(req.text)['status'] == 'success':
            return statement('OK. Booked.')
        return question('Slot already used. You may try again.')
    elif stage == '':
        return statement('Bye.')
    else:
        return statement('Bye.')


@ask.intent('AMAZON.NoIntent')
def confirm_request():
    stage = session.attributes['stage']
    if stage == 'finding_slot':
        return statement('OK. Bye!')
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
