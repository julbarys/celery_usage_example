# celery_usage_example

## Установка celery

```shell
pip3 install celery
```

## Запуск демона celery

```shell
python3 -m celery -A tasks worker --loglevel=info
```