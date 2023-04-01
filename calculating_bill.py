from __future__ import print_function

import os.path
from email.message import EmailMessage
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import base64

from googleapiclient.errors import HttpError

SCOPES = ['https://mail.google.com/']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


def find_labelIds(str):
    service = build('gmail', 'v1', credentials=creds)
    label_id = 0
    labels_list = service.users().labels().list(userId='me').execute()
    labels = labels_list.get("labels")
    for i in range(len(labels)):
        if labels[i]["name"] == str:
            label_id = labels[i]["id"]
    return label_id



def search_email(label_id):
    try:
        service = build('gmail', 'v1', credentials=creds)
        messages_list = service.users().messages().list(
            userId ="me",
            labelIds = label_id
        ).execute()

        messages = messages_list.get("messages")
        next_page_token = messages_list.get("nextPageToken")

        while next_page_token:
            messages_list = service.users().messages().list(
                userId ="me",
                labelIds = label_id,
                pageToken=next_page_token
            ).execute

            messages.extend(messages_list.get("messages"))
            next_page_token = messages_list.get("nextPageToken")
        return messages
    except Exception as e:
	    raise NoEmailFound('No emails returned')

def get_message_detail(message_id, msg_format="full", metadata_headers:list=None):
    service = build('gmail', 'v1', credentials=creds)
    message_detail = service.users().messages().get(
        userId="me",
        id = message_id,
        format=msg_format,
        metadataHeaders=metadata_headers
    ).execute()
    return message_detail

def get_file_data(message_id, attachment_id):
    service = build('gmail', 'v1', credentials=creds)
    response = service.users().messages().attachments().get(
        userId="me",
        messageId=message_id,
        id = attachment_id
    ).execute()

    file_data = base64.urlsafe_b64decode(response.get("data").encode("UTF-8"))
    return file_data

def change_label(message_id, label_id_add, lebel_id_remove):
    service = build('gmail', 'v1', credentials=creds)
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={'removeLabelIds': lebel_id_remove, 'addLabelIds': label_id_add }
    ).execute()

def sendmessage(subject,content):
    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    message.set_content(content)
    message['To'] = 'deniz.hadji@lineal.si'
    message['From'] = 'denizhadzi@gmail.com'
    message['Subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
    .decode()


    create_message = {
        'raw': encoded_message
    }
    send_message = (service.users().messages().send
                (userId="me", body=create_message).execute())
    return(send_message)


