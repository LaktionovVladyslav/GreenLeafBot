import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TOKEN = os.getenv('TOKEN', '949216084:AAFwQZhyTtUm0GOE_UqAjCTC5h3NWJAIwQ0')
    DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://stqntfgkrjqnma:15f85ab1064261f4dc58063e2cddf02839674e134e919c8716c606c87848e08e@ec2-54-75-235-28.eu-west-1.compute.amazonaws.com:5432/dab86hkaa09fsr')
    LINK = 'https://greenleafbot.herokuapp.com/'