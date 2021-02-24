#!/usr/bin/env python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Cc, Bcc)
from nebula_sdk import Interface, Dynamic as D

relay = Interface()

api_key = relay.get(D.sendgrid.connection.apiKey)

fromAddress = relay.get("from")
toAddress = relay.get(D.to).split(",")
subject = relay.get(D.subject)

ccAddresses = None

try:
  ccAddresses = relay.get(D.cc).split(",")
except:
  pass

bccAddresses = None

try:
  bccAddresses = relay.get(D.bcc).split(",")
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

if ccAddresses is not None:
  ccs = []

  for ccAddress in ccAddresses:
    ccs.append(Cc(ccAddress))
    
  message.cc = ccs

if bccAddresses is not None:
  bccs = []

  for bccAddress in bccAddresses:
    bccs.append(Bcc(bccAddress))

  message.bcc = bccs

try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    toAddressString = ', '.join(toAddress)

    print(f'Your email titled "{subject}" was sent successfully to: {toAddressString}' )
except Exception as e:
    print(str(e))
    exit(1)
