import unittest
from selenium import webdriver
from tests.selenium.auth_scenario import run_auth_scenario
from tests.selenium.books_scenario import run_books_scenario
from tests.selenium.collections_scenario import run_collections_scenario
from tests.selenium.reviews_scenario import run_reviews_scenario
from tests.selenium.roles_scenario import run_roles_scenario
from tests.selenium.utils import clear_user, clear_book


class SeleniumTest(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-web-security")
        options.add_argument('--start-maximized')
        cls.driver = webdriver.Chrome(options=options)
        clear_user()
        clear_book()

    @classmethod
    def tearDown(cls):
        cls.driver.close()

    def test_auth_scenario(self):
        run_auth_scenario(self.driver)

    def test_books_scenario(self):
        run_books_scenario(self.driver)

    def test_reviews_scenario(self):
        run_reviews_scenario(self, self.driver)

    def test_collections_scenario(self):
        run_collections_scenario(self, self.driver)

    def test_roles_scenario(self):
        run_roles_scenario(self, self.driver)
