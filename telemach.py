from __future__ import print_function
import xml.etree.ElementTree as ET
import tempfile

import os.path


from calculating_bill import find_labelIds, change_label, search_email, get_message_detail, get_file_data

def telemach():

    data = []
    ceni = []
    smetki_telemach = {}

    telemach_placano_label_id = find_labelIds("telemach/telemach_placano")
    telemach_label_id = find_labelIds("telemach")
    telemach_messages = search_email(telemach_label_id)

    if not telemach_messages:
      return None
    else:
        for email_message in telemach_messages:
                telemachDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
                telemachDetailPayload = telemachDetail.get("payload")

                if "parts" in telemachDetailPayload:
                    for telemachPayload in telemachDetailPayload['parts']:
                        if (telemachPayload['filename'] != 0) and (".xml" in telemachPayload['filename']) and ("ovojnica" not in telemachPayload['filename']):
                                    body = telemachPayload['body']
                                    if 'attachmentId' in body:
                                        attachment_id = body['attachmentId']
                                        attachment_content = get_file_data(email_message['id'], attachment_id)
                                        with tempfile.NamedTemporaryFile(mode='w+b') as _f:
                                            text = _f.write(attachment_content)
                                            tree = ET.parse(_f.name)
                                            root = tree.getroot()
                                            numbers = []
                                            for x in root[0].findall('.//{urn:eslog:2.00}G_SG27'):
                                                if x[0][0][0].text == "38":
                                                    a = float((((x[0])[0])[1]).text)
                                                    numbers.append(a)
                                                    aaa = max(numbers)

                                                    final_expense = aaa
                                            ceni.append(final_expense)
                                            for y in root[0].findall("{urn:eslog:2.00}G_SG8"):
                                                if y[1][0][0].text == "13":
                                                    date = (y[1][0][1]).text
                                                    date_final = date[0] + date[1] + date[2] + date[3] + date[4] + date[5] + date[6]
                                                    data.append(date_final)
                                    change_label(email_message['id'], telemach_placano_label_id, telemach_label_id)

        for value, key in zip(ceni, data):
            if key not in smetki_telemach:
                smetki_telemach[key]=value
            else:
                smetki_telemach[key]=round((smetki_telemacht[key] + value), 2)
        return(smetki_telemach)





