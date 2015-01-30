# -*- coding: utf-8 -*-

import pdb

import sys as sys
import logging as logging
import time as time

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 4:
    print 'Please enter username, password, your ip address and gsm number'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
public_ip_address = sys.argv[3]
address = sys.argv[4]
port = 9000

sms_client = oneapi.SmsClient(username, password)

notify_url = 'http://{0}:{1}'.format(public_ip_address, port)
# example:prepare-message-with-notify-url
sms = models.SMSRequest()
sms.sender_address = address
sms.address = address
sms.message = 'Test message'
# The url where the delivery notification will be pushed:
sms.notify_url = notify_url
# ----------------------------------------------------------------------------------------------------

result = sms_client.send_sms(sms)

if not result.is_success():
    print 'Error sending message:', result.exception
    sys.exit(1)

print result
print 'Is success = ', result.is_success()
print 'Client correlator = ', result.client_correlator

# Wait for 15 seconds for push-es
server = dummyserver.DummyWebServer(port)
server.start_wait_and_shutdown(15)

requests = server.get_requests()
if not requests:
    print 'No requests received'
    sys.exit(1)

for method, path, http_body in requests:
    # example:on-delivery-notification
    delivery_status = oneapi.SmsClient.unserialize_delivery_status(http_body)
    # ----------------------------------------------------------------------------------------------------
    print delivery_status
