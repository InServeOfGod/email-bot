# Python Email-bot Version : 2022.1
Author : InServeOfGod

$ python3 email-bot.py --secure --host:<SMTP> --receivers:<EMAIL> --sender:<EMAIL> --messages:<MSG> --file:<TEXTFILE> [--days, --hours --minutes, --seconds, --count, --attachments] --help

    - Separate the content of the arguments with comma (,) to prevent missing info provided to program.

    --help:
        Shows this help message

    --host: ( * optional ):
        This is the host to use to make our SMTP request, default is localhost

    --secure ( * optional ):
        Default, the mail will be sent under TLS

    --unsecure ( * optional ):
        the mail will not send under TLS

    --receivers ( * required ) :
        list of receiver(s) of mails

    --sender ( * required ) :
        This is option who will send the email. Program will ask for password in order to login

    --messages ( * required unless --file provided ) :
        message(s) to send

    --file ( * required unless --message provided ) :
        if provided then message parameter will be ignored and contain of the file will be sent as message

    --days ( * optional ):
        days after send

    --hours ( * optional ):
        hours after send

    --minutes ( * optional ):
        minutes after send

    --seconds ( * optional ):
        seconds after send

    --count ( * optional ):
        how many times the emails will be sent

    --attachments ( * optional ):
        file(s) to attach the email

#Example Usages :
    $ python3 email-bot.py --secure --days:1 --hours:5 --minutes:5 --seconds:50 --count:3 --sender:localhost
        --receivers:example@gmail.com,example2@gmail.com --messages:"hello","goodbye" --attachments:"image.png","document.pdf"

    $ python3 email-bot.py --unsecure --minutes:1 --receivers:example@gmail.com --file:"msg.txt"
    $ python3 email-bot.py --secure --receivers:abc@gmail.com --messages:"good morning"
    $ python3 email-bot.py --receivers:abc@gmail.com,xyz@gmail.com --messages:"good morning" --minutes:30
