import telebot
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
bot = telebot.AsyncTeleBot(Config.TOKEN)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
