#import tabledef
#from tabledef import User, MentoreeTopic, Topic
import requests
print requests
# import pdb


# def send_message(recipient, subject, text):
#     return requests.post(
#         "https://api.mailgun.net/v2/samples.mailgun.org/messages",
#         auth=("api", "key-21q1narswc35vqr1u3f9upn3vf6ncbb9"),
#         data={"from": "Mentoree Match <mentoreematch@app27934969.mailgun.org>",
#               "to": recipient.email_address,
#               "subject": subject,
#               "text": "Testing some Mailgun awesomness!"})

def send_message():
    # pdb.set_trace()
    print dir(requests)
    x =  requests.post(
        "https://api.mailgun.net/v2/samples.mailgun.org/messages",
        auth=("api", "key-21q1narswc35vqr1u3f9upn3vf6ncbb9"),
        data={"from": "Mentoree Match <mentoreematch@app27934969.mailgun.org>",
              "to": "Daphnejwang@gmail.com",
              "subject": "testing email",
              "text": "Testing some Mailgun awesomness!"})
    return 'hi'
# key = 'YOUR API KEY HERE'
# sandbox = 'YOUR SANDBOX URL HERE'
# recipient = 'YOUR EMAIL HERE'

# request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
# request = requests.post(request_url, auth=('api', key), data={
#     'from': 'hello@example.com',
#     'to': recipient,
#     'subject': 'Hello',
#     'text': 'Hello from Mailgun'
# })

# print 'Status: {0}'.format(request.status_code)
# print 'Body:   {0}'.format(request.text)

send_message()
