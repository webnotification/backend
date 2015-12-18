# notification.backend

### Before running django app

##### Run celery
``` bash
celery --app=backend.celery:app worker --loglevel=INFO
```

##### Run rabbitmq/redis
``` bash
rabbitmq-server
redis-server
```
