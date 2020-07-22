import pytest
import time

from django.contrib.auth import get_user_model, authenticate

@pytest.mark.django_db
def test_something(selenium, live_server):
    user = get_user_model().objects.create_superuser(
        username="root", email="a@a.de", password="root"
    )

    selenium.get(f"{live_server}/frontend/")
    selenium.implicitly_wait(10)

    # username_input, password = selenium.find_elements_by_class_name("form-group")
    # print(username_input)

    selenium.find_element_by_xpath("//input[contains(@class, 'form-control')]").send_keys("root")
    selenium.find_element_by_xpath("//input[contains(@class, 'text-input')]").send_keys("root")

    selenium.find_element_by_xpath("//button").click()
    time.sleep(5)
    assert False