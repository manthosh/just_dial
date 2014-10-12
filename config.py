import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'Anguraj-loves-Swathi'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@localhost/ethakaval'

UPLOADS_DEFAULT_DEST = basedir + '/app/static/img/'
#UPLOADS_DEFAULT_URL = 'static/img'