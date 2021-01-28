#!/usr/bin/env python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Cc, Bcc)
from nebula_sdk import Interface, Dynamic as D

relay = Interface()

api_key = relay.get(D.sendgrid.connection.apiKey)

fromAddress = relay.get("from")
toAddress = relay.get(D.to)
subject = relay.get(D.subject)

ccAddress = None

try:
  ccAddress = relay.get(D.cc)
except:
  pass

bccAddress = None

try:
  bccAddress = relay.get(D.bcc)
except:
  pass

text = None

try: 
  text = relay.get(D.body.text)
except:
  pass

html = None

try: 
  html = relay.get(D.body.html)
except: 
  pass

message = Mail(
    from_email=fromAddress,
    to_emails=toAddress,
    subject=subject,
    plain_text_content=text,
    html_content=html)

if ccAddress is not None:
  message.cc = Cc(ccAddress)

if bccAddress is not None:
  message.bcc = Bcc(bccAddress)

try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)

    print(f'Your email titled "{subject}" was sent successfully to: {toAddress}' )

    relay.outputs.set('statusCode', response.status_code)
    relay.outputs.set('body', response.body)
    relay.outputs.set('headers', response.headers)
except Exception as e:
    print(str(e))
    exit(1)
