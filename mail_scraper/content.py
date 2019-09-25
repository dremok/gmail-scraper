import email
from html.parser import HTMLParser


class MsgNode:
    def __init__(self):
        self.msg = []
        self.parent = None


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def parse_content(msg):
    content = []
    if msg.is_multipart():
        for payload in msg.get_payload():
            content.append(payload.get_payload(decode=True).decode('utf-8'))
    else:
        content.append(msg.get_payload(decode=True).decode('utf-8'))
    return strip_tags('\n'.join(content))


def fetch_mail(mail, mail_id):
    _, data = mail.fetch(mail_id, '(RFC822)')
    msg = email.message_from_string(data[0][1].decode('utf-8'))
    return parse_content(msg)


def parse_thread_from_mail(parsed_msg):
    current_msg = MsgNode()
    level = 0
    for line in parsed_msg.split('\n'):
        if line.startswith('>' * level):
            current_msg.msg.append(line)
        elif line.startswith('>' * (level + 1)):
            next_msg = MsgNode()
            current_msg.parent = next_msg
            current_msg = next_msg
            current_msg.msg.append(line)
