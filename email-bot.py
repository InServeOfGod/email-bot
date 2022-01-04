import smtplib
import sys
import time
from datetime import datetime


# helper function to show help
def helper(option='') -> None:
    if option != '':
        print('The option --{} is required!'.format(option))

    with open('helper.txt') as f:
        print(f.read())
    exit(0)


# the set of options
options = {
    "secure_port": 587,
    "unsecure_port": 25,
    "tls": True,
    "seconds": 0,
    "count": 1,
    "host": "localhost",
    "sender": "",
    "credential": "root",
    "receivers": [],
    "messages": [],
    "files": []
}

# check for arguments provided
for arg in sys.argv[1:]:
    if arg == '--help':
        helper()

    if arg[0:len('--host')] == '--host':
        options['host'] = arg[7:]

    if arg == '--secure':
        options['tls'] = True

    if arg == '--unsecure':
        options['tls'] = False

    if arg[0:len('--receivers')] == '--receivers':
        receivers = arg.split(':')[1]
        mails = receivers.split(',')
        options['receivers'] = mails

    if arg[0:len('--sender')] == '--sender':
        options['sender'] = arg[len('--sender')+1:]
        options['credential'] = input("Enter password : ")

    if arg[0:len('--messages')] == '--messages':
        messages = arg.split(':')[1]
        msg = messages.split(',')
        options['messages'] = msg

    if arg[0:len('--file')] == '--file':
        file = arg.split(':')[1]

        try:
            with open(file) as f:
                options['messages'] = f.read()

        except FileNotFoundError:
            print("The file {} is not found trying to use --messages option".format(file))

    if arg[0:len('--days')] == '--days':
        seconds = int(arg[len('--days')+1:]) * 24 * 60 * 60
        options['seconds'] += seconds

    if arg[0:len('--hours')] == '--hours':
        seconds = int(arg[len('--hours')+1:]) * 60 * 60
        options['seconds'] += seconds

    if arg[0:len('--minutes')] == '--minutes':
        seconds = int(arg[len('--minutes')+1:]) * 60
        options['seconds'] += seconds

    if arg[0:len('--seconds')] == '--seconds':
        seconds = int(arg[len('--seconds')+1:])
        options['seconds'] += seconds

    if arg[0:len('--count')] == '--count':
        options['count'] = int(arg[len('--count')+1:])

    if arg[0:len('--attachments')] == '--attachments':
        attachments = arg.split(':')[1]
        files = attachments.split(',')
        options['files'] = files

if options.get('receivers') == '':
    helper('receivers')

if options.get('sender') == '':
    helper('sender')

if options.get('messages') == '':
    helper('messages')

tls = options.get('tls')
smtp = None

# check if tls option is enabled and use port due to its result
if tls:
    port = options.get("secure_port")

else:
    port = options.get('unsecure_port')

try:
    host = options.get('host')

    # setup SMTP server
    print("[*] Setting up SMTP...")
    smtp = smtplib.SMTP(host=host, port=port)
    print("[+] SMTP has been set")

    # start tls if tls option is enabled
    if tls:
        smtp.starttls()

    # login
    print("[*] Logging in...")
    smtp.login(user=options.get('sender'), password=options.get('credential'))
    print("[+] Logged in")

except smtplib.SMTPConnectError:
    print("[!] SMTP setup failed. Connection error")
    exit(-1)

except smtplib.SMTPHeloError:
    print("[!] Start TLS failed")
    exit(-1)

except smtplib.SMTPAuthenticationError:
    print("[!] Login failed. Invalid credentials")
    exit(-1)

except smtplib.SMTPNotSupportedError:
    print("[!] The AUTH command is not supported by the server")
    exit(-1)

except smtplib.SMTPException:
    print("[!] No suitable authentication method was found")
    exit(-1)

except Exception:
    print("[!] Unexpected error occurred")
    exit(-1)


# wait for some seconds before proceeding
seconds = int(options.get('seconds'))
print("[*] Waiting for {} seconds".format(seconds))

while seconds > 0:
    print("[*] {} Seconds left...".format(seconds))
    seconds -= 1
    time.sleep(1)
    options['seconds'] = seconds

# TODO : attach files also

# send messages x times
for i in range(options.get('count')):
    print(i+1, end=" => ")

    # send one message for each one receiver
    for receiver in options.get('receivers'):
        for message in options.get('messages'):
            try:
                print("[*] sending email to {}...".format(receiver))
                smtp.sendmail(from_addr=options.get('sender'), to_addrs=receiver, msg=message)
                print("[+] email has been sent {}".format(datetime.now()))

            except smtplib.SMTPHeloError:
                print("[!] The server didn't reply properly to the helo greeting")

            except smtplib.SMTPRecipientsRefused:
                print("[!] The server rejected ALL recipients")

            except smtplib.SMTPSenderRefused:
                print("[!] The server didn't accept the sender")

            except smtplib.SMTPDataError:
                print("[!] The server replied with an unexpected error code")

            except smtplib.SMTPNotSupportedError:
                print("[!] SMTP not supported")

            finally:
                # new line
                print()

# close server
print("[*] Closing SMTP server...")
smtp.close()
print("[+] Server has been closed and all processes are done completely.")
