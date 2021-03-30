#!/usr/bin/env python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Cc, Bcc)
from relay_sdk import Interface, Dynamic as D

relay = Interface()

def coerce_to_list(data):
  return data if isinstance(data, list) else [data]

api_key = relay.get(D.sendgrid.connection.apiKey)

from_address = relay.get("from")
subject = relay.get(D.subject)
to_address = coerce_to_list(relay.get(D.to))

cc_addresses = None

try:
  cc_addresses = coerce_to_list(relay.get(D.cc))
except:
  pass

bcc_addresses = None

try:
  bcc_addresses = coerce_to_list(relay.get(D.bcc))
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
    from_email=from_address,
    to_emails=to_address,
    subject=subject,
    plain_text_content=text,
    html_content=html)

if cc_addresses is not None:
  ccs = []

  for cc_address in cc_addresses:
    ccs.append(Cc(cc_address))
    
  message.cc = ccs

if bcc_addresses is not None:
  bccs = []

  for bcc_address in bcc_addresses:
    bccs.append(Bcc(bcc_address))

  message.bcc = bccs

try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    to_address_string = ', '.join(to_address)

    print(f'Your email titled "{subject}" was sent successfully to: {to_address_string}' )
except Exception as e:
    print(str(e))
    exit(1)
