import pytest
from selenium import webdriver


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('\PycharmProjects\pythonProject4\chromedriver.exe')
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    pytest.driver.find_element_by_id('email').send_keys('vasya@mail.com')
    pytest.driver.find_element_by_id('pass').send_keys('12345')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        print('NAME: ', names[i].text)
        assert names[i].text != ''
        assert descriptions[i].text != ''
        print('Descriptions: ', descriptions[i].text)
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0