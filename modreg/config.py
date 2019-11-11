import os

#config database uri here
class Config:
    SECRET_KEY = 'c9970460fc2c3ad324add53c94e3bc2a'
    SQLALCHEMY_DATABASE_URI = 'postgres://hlwsozdbaciqel:fe05139be83c565210c53a5a48d097f602de5ab21b43bcdea8ab9e9e6dce855f@ec2-107-22-160-102.compute-1.amazonaws.com:5432/dmj6idt7voapg'
    USER_APP_NAME = "CS2102 Project"      # Shown in and email templates and page footers
    USER_EMAIL_SENDER_EMAIL = "somedummy@gmail.com" #not used but required to initialize app