import pytest
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password, valid_login


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('\PycharmProjects\pythonProject4\chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    pytest.driver.maximize_window()

    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    pytest.driver.save_screenshot('my_pets.png')

    yield

    pytest.driver.quit()


@pytest.fixture()
def get_pets_num():
    acc_info = pytest.driver.find_elements_by_css_selector('div.task3 > div.left')[0].text
    pets_num = acc_info.split()[2]

    assert int(pets_num) >= 0

    return int(pets_num)


@pytest.fixture()
def get_pets_info():
    names = pytest.driver.find_elements_by_css_selector('tbody > tr > td:nth-of-type(1)')
    ages = pytest.driver.find_elements_by_css_selector('tbody > tr > td:nth-of-type(2)')
    types = pytest.driver.find_elements_by_css_selector('tbody > tr > td:nth-of-type(3)')

    text_names = [names[i].text for i in range(len(names))]
    text_ages = [ages[i].text for i in range(len(ages))]
    text_types = [types[i].text for i in range(len(types))]

    return text_names, text_ages, text_types


def test_all_my_pets_are_in_table(get_pets_num):
    table_rows = []
    try:
        table_rows = WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#all_my_pets > table tr'))
        )
    except TimeoutException:
        print("Не удалось загрузить элементы на странице")

    finally:
        assert get_pets_num == len(table_rows) - 1


def test_half_of_pets_have_photo(get_pets_num):
    photos = []
    try:
        photos = WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#all_my_pets > table img'))
        )
    except TimeoutException:
        print("Не удалось загрузить элементы на странице")

    finally:
        photo_count = 0
        for i in range(len(photos)):
            if photos[i].get_attribute('src') != '':
                photo_count += 1
        assert photo_count >= get_pets_num / 2


def test_all_pets_have_name_age_type(get_pets_info):
    names, ages, types = get_pets_info
    for i in range(len(names)):
        assert names[i] != ''
        assert ages[i] != ''
        assert types[i] != ''


def test_all_pets_have_diff_name(get_pets_num, get_pets_info):
    names, ages, types = get_pets_info
    pets = {}
    for i in range(len(names)):
        pets[names[i]] = (ages[i], types[i])

    assert get_pets_num == len(pets)


def test_all_pets_are_unique(get_pets_info):
    names, ages, types = get_pets_info
    flag = True

    for i in range(len(names) - 1):
        for j in range(i + 1, len(names)):
            if names[i] == names[j] and ages[i] == ages[j] and types[i] == types[j]:
                flag = False
                break
        if not flag:
            break

    assert flag == True