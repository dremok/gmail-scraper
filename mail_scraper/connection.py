import sys

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def connect(email, password):
    FROM_EMAIL = "max.y.leander@gmail.com"
    FROM_PWD = password


if __name__ == '__main__':
    connect(sys.argv[1])
