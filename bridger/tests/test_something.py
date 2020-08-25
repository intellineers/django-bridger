# import pytest
# import time
# from selenium import webdriver
# from channels.testing import ChannelsLiveServerTestCase

# from django.contrib.auth import get_user_model, authenticate
# from .selenium.utils import menu_items_for_user

# def login(url, username, password):
#     driver = webdriver.Chrome()
#     driver.get(f"{url}/frontend/")
#     driver.implicitly_wait(10)
#     driver.find_element_by_xpath("//input[contains(@class, 'form-control')]").send_keys(username)
#     driver.find_element_by_xpath("//input[contains(@class, 'text-input')]").send_keys(password)
#     driver.find_element_by_xpath("//button").click()
#     time.sleep(1)
#     return driver


# @pytest.mark.django_db
# class TestLive(ChannelsLiveServerTestCase):

#     @pytest.mark.parametrize
#     def test_something1(self):
#         user = get_user_model().objects.create_superuser(
#             username="root",
#             email="a@a.de",
#             password="root"
#         )
#         driver = login(self.live_server_url, "root", "root")

#         # self.driver.find_element_by_class_name("root-menu__trigger").click()

#         # menu_items = self.driver.find_elements_by_class_name("menu__menu-item")
#         # for menu_item in menu_items:
#         #     menu_item.click()
#         #     time.sleep(3)

#         assert False