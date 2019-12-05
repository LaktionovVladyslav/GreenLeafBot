import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TOKEN = os.getenv('TOKEN', '873014740:AAHf_Q1H3Qt2hkCVTcaIt6NOIVfnoQMJ8EI')
    DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://kzoaanghlapdqx'
                                             ':d483368ec976b52500c6ff955f67b4e7032b2f18b24a6df99c513af33330d6ee@ec2'
                                             '-54-228-207-163.eu-west-1.compute.amazonaws.com:5432/dfu81j7kauqrqa')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://h:pba002627df5f5acb40d5396cac63f85badde5a724a7766b91585beb2e94e5721'
                                       '@ec2-52-51-164-88.eu-west-1.compute.amazonaws.com:29349')
    LINK = 'https://callermanager.herokuapp.com/'
