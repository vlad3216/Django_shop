import logging
from bs4 import BeautifulSoup
from shop1.api_clients import BaseClient

logger = logging.getLogger(__name__)


class Parser(BaseClient):
    base_url = 'https://comfy.ua/ua/desktop-computer/'

    def parse(self):
        response = self.get_request(
            method='get',
        )
        soup = BeautifulSoup(response)
        try:
            category_name = soup.find(
                'h1', attrs={'class': 'b-title'}
            ).text
        except (AttributeError, IndexError) as err:
            logger.error(err)
        else:
            product_list = []
            for element in soup.find_all(
                'li',
                class_="b-online-edit b-product-gallery__item js-productad"
            ):
                try:
                    name = element.find(
                        'a',
                        class_="b-product-gallery__title").text
                    sku = element.find(
                        'span',
                        class_="b-product-gallery__sku").text
                    price = element.find(
                        'span', class_="b-product-gallery__current-price"
                        ).text.replace('\xa0', '').split('г')[0]
                    image_url = element.find(
                        'img', class_="b-product-gallery__image").attrs['src']
                    product_list.append({
                                            'name': name,
                                            'description': name,
                                            'price': price,
                                            'sku': sku,
                                            'category': category_name,
                                            'image': image_url
                                        })
                except (AttributeError, KeyError) as err:
                    logger.error(err)
            return product_list


products_parser = Parser()