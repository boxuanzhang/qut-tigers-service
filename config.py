

DEBUG = True

# SERVER_NAME = ''
# APPLICATION_ROOT = ''

# MongoDB
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'qut-tigers'

# Redis
REDIS_URL = 'redis://127.0.0.1:6379/qut-tigers'

# JSON Web Token
JWT_SECRET = '\'oI(`\\r?y k92Os>IxE,)j\\x0bu/iTqj\\x0b8$!B/7HUd7Kw9*9y$E:63<jXVH9:"Xsol,&{\''
JWT_EXPIRE = 30 * 24 * 3600
JWT_METHOD = 'HS256'

# i18n
LOCALE_DIR = 'locale'
LOCALE_LANG = 'en'

# Qiniu
QINIU_UPLOAD_URL = 'http://upload.qiniu.com/'
QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''
if DEBUG:
    QINIU_DOWNLOAD_URL = ''
    QINIU_SCOPE = ''
else:
    QINIU_DOWNLOAD_URL = ''
    QINIU_SCOPE = ''


# LeanCloud
if DEBUG:
    LEANCLOUD_APPID = ''
    LEANCLOUD_APPKEY = ''
    LEANCLOUD_MASTERKEY = ''
    LEANCLOUD_INTERNALKEY = ''
else:
    LEANCLOUD_APPID = ''
    LEANCLOUD_APPKEY = ''
    LEANCLOUD_MASTERKEY = ''
    LEANCLOUD_INTERNALKEY = ''
