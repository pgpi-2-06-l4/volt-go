import dj_database_url

DEBUG = True

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://admin:LeEp5N4apL7BK8SMk6bWgPywzlshpdQi@dpg-clpl40946foc73dbi2ng-a.oregon-postgres.render.com/voltgosql',
        conn_max_age=600
    )
}
STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/static/media/'
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['http://10.5.0.1:8001', 'http://localhost:8001']
