import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from currencies.clients.clients import currency_clients
from currencies.models import CurrencyHistory

from shop1.celery import app
from shop1.model_choice import Currency

logger = logging.getLogger(__name__)


@app.task
def clear_old_currencies():
    CurrencyHistory.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=3),
    ).delete()


@shared_task
def get_currencies():
    for client in currency_clients:
        currency_list = client.get_currency()
        if currency_list == []:
            continue
        currency_history_list = []
        for currency in currency_list:
            try:
                currency_history_list.append(
                    CurrencyHistory(
                        currency=currency['currency'],
                        buy=currency['buy'],
                        sale=currency['sale']
                    )
                )
            except (KeyError, ValueError) as err:
                logger.error(err)
        break

    if currency_history_list:
        CurrencyHistory.objects.bulk_create(currency_history_list)
        clear_old_currencies.delay()