# CELERY SETTINGS
BROKER_URL = 'django://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Database backend settings
# http://docs.celeryproject.org/en/latest/configuration.html#conf-database-result-backend
CELERY_RESULT_BACKEND = 'db+scheme://user:password@host:port/dbname'
