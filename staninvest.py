from __future__ import print_function
import xml.etree.ElementTree as ET
import tempfile


from calculating_bill import find_labelIds, change_label, search_email, get_message_detail, get_file_data


def staninvest():


    # staninvest najdi label_id
    data = []
    ceni = []
    smetki_staninvest = {}

    staninvest_placano_label_id = find_labelIds("staninvest/staninvest_placano")
    staninvest_label_id = find_labelIds("staninvest")
    staninvest_messages = search_email(staninvest_label_id)

    if not staninvest_messages:
      return None
    else:
        for email_message in staninvest_messages:
                staninvestDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
                staninvestDetailPayload = staninvestDetail.get("payload")

                if "parts" in staninvestDetailPayload:
                    for staninvestPayload in staninvestDetailPayload['parts']:
                        if (staninvestPayload['filename'] != 0) and (".xml" in staninvestPayload['filename']):
                                    body = staninvestPayload['body']
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
                                    change_label(email_message['id'], staninvest_placano_label_id, staninvest_label_id)
        for value, key in zip(ceni, data):
                if key not in smetki_staninvest:
                    smetki_staninvest[key]=value
                else:
                    smetki_staninvest[key]=round((smetki_staninvest[key] + value), 2)
        return(smetki_staninvest)





















