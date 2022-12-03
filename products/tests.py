import tempfile
from decimal import Decimal
from django.shortcuts import redirect
from django.urls import reverse
from products.models import Product, Category


def test_products(login_user, client, faker, product):
    response = client.get(reverse('products'))
    assert response.status_code == 200

    response = client.get(reverse('product_detail', args=(product.id,)))
    assert response.status_code == 200

    data = {
        'quantity': 5,
    }
    response = client.post(reverse('cart_add', args=(product.id,)), data=data, follow=True)
    assert response.status_code == 200
    assert not response.context['cart'].cart.__len__() == 0

    response = client.post(reverse('cart_remove', args=(product.id,)), data=data, follow=True)
    assert response.status_code == 200
    assert response.context['cart'].cart.__len__() == 0

    client, user = login_user

    response = client.post(reverse('add_or_remove_favorite', args=(product.id,)), follow=True)
    assert response.status_code == 200

    response = client.post(reverse('add_or_remove_favorite', args=(product.id,)), follow=True)
    assert response.status_code == 200

    response = client.post(reverse('favorites'), follow=True)
    assert response.status_code == 200


def test_import_csv(login_user, client):
    response = client.post(reverse('import_csv'), follow=True)
    assert response.status_code == 200
    assert b'Email address' in response.content

    client, user = login_user
    response = client.post(reverse('import_csv'), follow=True)
    assert response.status_code == 200
    assert b'Import success!' in response.content


def test_export_(login_user, client, faker, product):
    response = client.post(reverse('export_csv'), follow=True)
    assert response.status_code == 200
    assert b'Email address' in response.content

    client, user = login_user
    response = client.post(reverse('export_csv'), follow=True)
    assert response.status_code == 200
    assert b'name,description,category,price,sku,image\r\n' in response.content

# def test_ExportPDF(login_user, client, faker, product):

#     response = client.get(reverse('export_pdf'))
#     assert response.status_code == 200
#     assert b'Email address' in response.content

#     client, user = login_user
#     response = client.get(reverse('export_pdf'))
#     assert response.status_code == 200