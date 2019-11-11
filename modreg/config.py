import os

#config database uri here
class Config:
    SECRET_KEY = 'c9970460fc2c3ad324add53c94e3bc2a'
    SQLALCHEMY_DATABASE_URI = 'postgres://vztzvvjrtwvstn:cab4c8cf60f45147554123154c162f980b274f30ed041f8b46ff7eaa03a80615@ec2-174-129-194-188.compute-1.amazonaws.com:5432/d6om5mduqv2h7s'
    USER_APP_NAME = "CS2102 Project"      # Shown in and email templates and page footers
    USER_EMAIL_SENDER_EMAIL = "somedummy@gmail.com" #not used but required to initialize app