from django.urls import reverse
from django.core import mail

from Config.models import Config


def test_main_page(client, faker):
    response = client.get(reverse('main'))
    assert response.status_code == 200
    assert b"McDonald's Corporation" in response.content

    contact_email, _ = Config.objects.get_or_create(
        contact_form_email = 'baranikav@gmail.com'
    )

    data = {
        'email': faker.word(),
        'text': faker.sentence()
    }
    response = client.post(reverse('main'), data=data)
    assert response.status_code == 200
    assert not len(mail.outbox)

    data = {
        'email': faker.email(),
        'text': faker.sentence()
    }
    response = client.post(reverse('main'), data=data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('main') for i in response.redirect_chain)
    assert data['email'] in mail.outbox[0].body
    assert data['text'] in mail.outbox[0].body