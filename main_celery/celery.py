import os
import dotenv
from celery import Celery

dotenv.load_dotenv()


celery_app = Celery(
    "main_celery",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

# Route 'scraping' and 'web_server' tasks to queues
celery_app.conf.task_routes = {
    "scraping.tasks.*": {"queue": "scraping_queue"},
    "web_server.tasks.*": {"queue": "web_server_queue"},
}

# Define Queues
celery_app.conf.task_queues = {
    "scraping_queue": {"binding_key": "scraping_queue"},
    "web_server_queue": {"binding_key": "web_server_queue"},
}


celery_app.conf.update(
    timezone="UTC",
    # set higher maximum interval for beat checks
    beat_max_loop_interval=int(
        os.getenv("MAX_BEAT_INTERVAL_SECONDS", 691200)
    ),  # default 8 days in seconds
    broker_connection_retry_on_startup=True
)

# register tasks
celery_app.autodiscover_tasks()
