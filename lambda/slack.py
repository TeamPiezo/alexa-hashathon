import slackclient
import config

slack = slackclient.SlackClient(config.TOKEN)


def post_message(message, person='default', channel='C6ENKDXR6'):
    print(message)
    print(person)
    slack.api_call('chat.postMessage',
                   channel=channel,
                   text='Assigned to ' + str(person) + ':\n' + str(message))
