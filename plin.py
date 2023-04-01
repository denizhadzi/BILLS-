from __future__ import print_function
import tempfile

import PyPDF2
import os



from calculating_bill import find_labelIds, change_label, search_email, get_message_detail, get_file_data

def plin():


    # staninvest najdi label_id
    data = []
    ceni = []
    text_pdf = []
    smetki_plin = {}

    plin_label_id = find_labelIds("plin")
    plin_placano_label_id = find_labelIds("plin/plin_placano")
    plin_messages = search_email(plin_label_id)

    if not plin_messages:
      return None
    else:
        for email_message in plin_messages:
                plinDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
                plinDetailPayload = plinDetail.get("payload")

                if "parts" in plinDetailPayload:
                    for plinPayload in plinDetailPayload['parts']:
                        if (plinPayload['filename'] != 0) and (".pdf" in plinPayload['filename']) and ("racun" in plinPayload['filename']):
                                    body = plinPayload['body']
                                    file_name = plinPayload['filename']
                                    if 'attachmentId' in body:
                                        attachment_id = body['attachmentId']
                                        attachment_content = get_file_data(email_message['id'], attachment_id)
                                        with tempfile.NamedTemporaryFile(mode='w+b') as _f:
                                            text = _f.write(attachment_content)
                                            with open(os.path.join(os.getcwd(), _f.name), "rb") as pdffile:
                                                pdfReader = PyPDF2.PdfFileReader(pdffile)
                                                page = pdfReader.getPage(0)
                                                text1 = page.extractText()
                                                split_right = text1.split("Koda namena:",1)[1]
                                                split_right_left = split_right.split(" €",1)[0]
                                                cena = float(split_right_left.replace(",", "."))
                                                ceni.append(cena)
                                                split_date_right = text1.split("\nSI",1)[0]
                                                split_date_right_left = split_date_right.split(" €\n",1)[1]
                                                date_dd = ((split_date_right_left.replace(". ", "-")).split("-", 2))[0]
                                                date_mm = ((split_date_right_left.replace(". ", "-")).split("-", 2))[1]
                                                date_yyy = ((split_date_right_left.replace(". ", "-")).split("-", 2))[2]
                                                date1 = date_yyy + "-" + date_mm
                                                if len(date1) == 7:
                                                    date = date1
                                                else:
                                                    date = date1[0] + date1[1] + date1[2] + date1[3] + date1[4] + "0" + date1[5]
                                            data.append(date)
                                    change_label(email_message['id'], plin_placano_label_id, plin_label_id)




        for value, key in zip(ceni, data):
            if key not in smetki_plin:
                smetki_plin[key]=value
            else:
                smetki_plin[key]=round((smetki_plin[key] + value), 2)
        return(smetki_plin)





















