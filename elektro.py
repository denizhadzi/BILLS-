from __future__ import print_function
import xml.etree.ElementTree as ET
import tempfile

import os.path
import base64

from calculating_bill import find_labelIds, change_label, search_email, get_message_detail, get_file_data


def elektro():

    data = []
    ceni = []
    smetki_elektro = {}

    elektro_label_id = find_labelIds("elektro")
    elektro_placano_label_id = find_labelIds("elektro/elektro_placano")
    elektro_messages = search_email(elektro_label_id)

    if not elektro_messages:
      return None
    else:
        for email_message in elektro_messages:
                elektroDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
                elektroDetailPayload = elektroDetail.get("payload")

                if "parts" in elektroDetailPayload:
                    for elektroPayload in elektroDetailPayload['parts']:
                        if (elektroPayload['filename'] != 0) and (".xml" in elektroPayload['filename']) and ("ovojnica" not in elektroPayload['filename']):
                                    body = elektroPayload['body']
                                    if 'attachmentId' in body:
                                        attachment_id = body['attachmentId']
                                        attachment_content = get_file_data(email_message['id'], attachment_id)

                                        with tempfile.NamedTemporaryFile(mode='w+b') as _f:
                                            text = _f.write(attachment_content)
                                            tree = ET.parse(_f.name)
                                            root = tree.getroot()
                                            numbers = []
                                            for x in root[0].findall('.//{urn:eslog:2.00}G_SG50'):
                                                if x[0][0][0].text == "388":
                                                    a = float((((x[0])[0])[1]).text)
                                                    numbers.append(a)
                                                    aaa = max(numbers)

                                                    final_expense = aaa
                                            ceni.append(final_expense)
                                            for y in root[0].findall("{urn:eslog:2.00}S_DTM"):
                                                if ((y[0])[0]).text == "137":
                                                    date = ((y[0])[1]).text
                                                    date_final = date[0] + date[1] + date[2] + date[3] + date[4] + date[5] + date[6]
                                                    data.append(date_final)
                                    change_label(email_message['id'], elektro_placano_label_id, elektro_label_id)
        for value, key in zip(ceni, data):
                if key not in smetki_elektro:
                    smetki_elektro[key]=value
                else:
                    smetki_elektro[key]=round((smetki_elektro[key] + value), 2)
        return(smetki_elektro)




