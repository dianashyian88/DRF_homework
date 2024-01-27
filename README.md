Для запуска приложения, необходимо создать файл .env, в котором определить переменные:
SECRET_KEY
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
PGDATA
EMAIL_HOST_PASSWORD
CACHE_ENABLED
CACHES_LOCATION
STRIPE_BASE_URL
STRIPE_API_KEY
CELERY_BROKER_UR
CELERY_RESULT_BACKEND

При запуске на Linux, MacOS, необходимо в файле docker-compose.yaml 
соответствующим образом скорректировать команды в celery и celery_beat

Далее необходимо собрать образ, запустить контейнеры, применить миграции
ю.б.жkjghhggh