import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TOKEN = os.getenv('TOKEN', '945677813:AAGSWQ1OVlpDOUiY1rxHSuPPcjuHALw6Efg')
    DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://localhost:5432/green_leaf_dev')