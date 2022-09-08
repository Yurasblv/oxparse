"""SCRAPPER FILE"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.db import Adt, db


class Scrapper:
    """
    Main class for grabbing data.

    In __init__ we set options for Selenium Chrome web driver
    Executable path is where driver located.
    Also u can configure to use local browser via webdriver.manager library.
    For that we install chrome and driver in the dockerfile and configure new path for driver.

    Take attention about version of the chrome driver! .
    """
    def __init__(self, url=None):
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path="/usr/local/bin/chromedriver", chrome_options=self.options
        )
        self.driver.maximize_window()

    def navigate(self, page_number):
        """Method get url of the resource"""
        self.url = f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page_number}/c37l1700273"
        self.driver.get(self.url)

    def get_adts(self, class_name):
        """Return iterator with all ad instances on the page"""
        adts = self.driver.find_elements(by=By.CSS_SELECTOR, value=class_name)[:45]
        iterator = [data for data in adts]
        return iterator

    def get_adt_info(self, data):
        """Methods separate data by groups for next filtration"""
        for element in data:
            main_info = (
                element.find_element(By.CLASS_NAME, value="clearfix")
                .find_element(By.CLASS_NAME, value="info")
                .find_element(By.CLASS_NAME, value="info-container")
            )
            bedrooms = (
                element.find_element(By.CLASS_NAME, value="clearfix")
                .find_element(By.CLASS_NAME, value="rental-info")
                .find_element(By.XPATH, value="span[@class='bedrooms']")
                .text[6:]
            )
            image_url = (
                element.find_element(By.CLASS_NAME, value="clearfix")
                .find_element(By.CLASS_NAME, value="left-col")
                .find_element(By.XPATH, value="div[@class='image']/picture/img")
                .get_attribute("data-src")
            )
            self.__refactor_adt_info(main_info, bedrooms, image_url)

    def __refactor_adt_info(self, main_info, bedrooms, image_url):
        """

        Extract data from groups to each column in dictionary.
        After each instance pass next step , dictionary cleans

        """
        title = main_info.find_element(By.CLASS_NAME, value="title").text
        city = main_info.find_element(
            By.XPATH, value="div[@class='location']/span[1]"
        ).text
        date = main_info.find_element(
            By.XPATH, value="div[@class='location']/span[2]"
        ).text
        description = main_info.find_element(
            By.XPATH, value="div[@class='description']"
        ).text
        image_url = image_url
        beds = bedrooms
        currency = main_info.find_element(By.CLASS_NAME, value="price").text[:1]
        amount = main_info.find_element(By.CLASS_NAME, value="price").text[1:]
        refactored_data = {
            "title": title,
            "city": city,
            "description": description,
            "beds": beds,
            "image_url": image_url,
            "date": date,
            "currency": currency,
            "amount": amount,
        }
        self.__save_to_postgres(**refactored_data)
        refactored_data.clear()

    def __save_to_postgres(self, **data):
        """Method for saving instance to database"""
        instance = Adt(
            title=data["title"],
            city=data["city"],
            description=data["description"],
            beds=data["beds"],
            img_url=data["image_url"],
            date=Adt.formatted_date(data["date"]),
            currency=data["currency"],
            amount=Adt.check_amount(data["amount"]),
        )
        db.session.add(instance)
        db.session.commit()
        return instance

    def has_data(self, data):
        """
        Bool constraint for extraction.
        If page not have any record it return False
        """
        return len(data) > 0


def grab():
    """
    Loop function
    """
    scrapper = Scrapper()
    page_number = 1
    while True:
        scrapper.navigate(page_number)
        data = scrapper.get_adts(class_name="div[class*=search-item]")
        scrapper.get_adt_info(data)
        if scrapper.has_data(data=data) is False:
            break
    scrapper.driver.close()
