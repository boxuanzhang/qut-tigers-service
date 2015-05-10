DEBUG = True

# SERVER_NAME = ''
# APPLICATION_ROOT = ''

SUPER_USER = 'root'

# MongoDB
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'qut-tigers'

# Redis
REDIS_URL = 'redis://127.0.0.1:6379/qut-tigers'

# JSON Web Token
JWT_SECRET = '!>!>!!>!>!SET THIS IN PRODUCTION!<!<!!<!<!'
JWT_EXPIRE = 30 * 24 * 3600
JWT_METHOD = 'HS256'

# i18n
LOCALE_DIR = 'locale'
LOCALE_LANG = 'en'

# Qiniu
QINIU_UPLOAD_URL = 'http://upload.qiniu.com/'
QINIU_ACCESS_KEY = 'OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa'
QINIU_SECRET_KEY = 'T_BQjqxNzaBMUy0QTcC8OWHnt8KO3tX-9LxsgBgm'
QINIU_DOWNLOAD_URL = 'http://7xis0d.com1.z0.glb.clouddn.com'
QINIU_SCOPE = 'qut-tigers'
