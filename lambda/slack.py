import slackclient
import config

slack = slackclient.SlackClient(config.TOKEN)


def post_message(message, person='default', channel = config.TARGET_CHANNEL):
    slack.api_call('chat.postMessage',
                   channel=channel,
                   text='Assigned to ' + person + ':\n' + message)