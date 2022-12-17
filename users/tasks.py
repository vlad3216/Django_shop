from shop1.celery import app


@app.task
def send_sms(phone: str, code: int):
    print(code)