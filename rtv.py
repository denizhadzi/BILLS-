from __future__ import print_function
import xml.etree.ElementTree as ET
import tempfile

import os.path
import base64

from calculating_bill import find_labelIds, change_label, search_email, get_message_detail, get_file_data

class GmailException(Exception):
	"""gmail base exception class"""

class NoEmailFound(GmailException):
	"""no email found"""

def rtv():

    data = []
    ceni = []
    smetki_rtv = {}
    rtv_placano_label_id = find_labelIds("rtv/rtv_placano")
    rtv_label_id = find_labelIds("rtv")
    rtv_messages = search_email(rtv_label_id)

    if not rtv_messages:
      return None
    else:
        for email_message in rtv_messages:
                rtvDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
                rtvDetailPayload = rtvDetail.get("payload")

                if "parts" in rtvDetailPayload:
                    for rtvPayload in rtvDetailPayload['parts']:
                        if (rtvPayload['filename'] != 0) and (".xml" in rtvPayload['filename']) and ("ovojnica" not in rtvPayload['filename']):
                                    body = rtvPayload['body']
                                    if 'attachmentId' in body:
                                        attachment_id = body['attachmentId']
                                        attachment_content = get_file_data(email_message['id'], attachment_id)
                                        with tempfile.NamedTemporaryFile(mode='w+b') as _f:
                                            text = _f.write(attachment_content)
                                            tree = ET.parse(_f.name)
                                            root = tree.getroot()
                                            numbers = []
                                            for x in root[0].findall("{urn:eslog:2.00}G_SG50"):
                                                a = float((((x[0])[0])[1]).text)
                                                numbers.append(a)
                                                aaa = max(numbers)
                                                bbb = min(numbers)
                                                final_expense = aaa-abs(bbb)
                                            ceni.append(final_expense)
                                            for y in root[0].findall("{urn:eslog:2.00}S_DTM"):
                                                if ((y[0])[0]).text == "137":
                                                    date = ((y[0])[1]).text
                                                    date_final = date[0] + date[1] + date[2] + date[3] + date[4] + date[5] + date[6]
                                                    data.append(date_final)
                                    change_label(email_message['id'], rtv_placano_label_id, rtv_label_id)





        for value, key in zip(ceni, data):
                if key not in smetki_rtv:
                    smetki_rtv[key]=value
                else:
                    smetki_rtv[key]=round((smetki_rtv[key] + value), 2)

        return(smetki_rtv)



