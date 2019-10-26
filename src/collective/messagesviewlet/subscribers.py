# -*- coding: utf-8 -*-
from collective.messagesviewlet.message import generate_uid


def change_hidden_uid(message, event):
    """
        Generate a new uid if the message is activated
    """
    if event.action == 'activate':
        message.hidden_uid = generate_uid()
