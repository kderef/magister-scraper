if __name__ == "__main__":
    print("this file is a library.\nthis file is not meant to be run.")
    exit(1)

import config
import itertools
import platform
import sys
from os import getcwd, system
from os.path import isfile, join
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions, Chrome, ChromeOptions, Opera
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

running_windows = platform.system() == "Windows"

DRIVER = join(getcwd(), config.BROWSER)


class DriverNotFoundError(Exception):
    pass


class Cijfer:
    def __init__(self, vak, date, description, cijfer, weging, inhalen) -> None:
        self.vak = vak
        self.date = date
        self.description = description
        self.cijfer = cijfer
        self.weging = weging
        self.inhalen = inhalen

    @property
    def all(self):
        return [
            self.vak,
            self.description,
            self.cijfer,
            self.weging,
            self.date,
            self.inhalen,
        ]

    @property
    def simple(self):
        return [self.vak, self.cijfer, self.weging, self.date]


def log(type: str, msg: str):
    print("\033[92m{0} :\033[0m {1}".format(type, msg))


class Magister:
    def __init__(self) -> None:
        """arguments:
        * school (string) -> name of the school to log into
        * login_data (tuple) -> tuple with username and password, e.g: ("username", "password")
        * nobrowser (bool) -> if True, make browser window invisible.
        """
        system("cls||clear")
        self.nobrowser = not config.WINDOW_VISIBLE

        log("INFO", f"nobrowser = {self.nobrowser}")

        self.school = config.SCHOOL
        self.logindata = config.LOGIN

        if not isfile(DRIVER):
            raise DriverNotFoundError("ERROR: driver needs to be in folder.")

        log("INFO", '[driver path] = "{}"'.format(DRIVER))
        if config.BROWSER.startswith("geckodriver"):
            self.opts = FirefoxOptions()
            self.opts.headless = self.nobrowser

            log("INFO", "starting client...")
            self.driver = Firefox(options=self.opts, executable_path=DRIVER)
        elif config.BROWSER.startswith("operadriver"):
            self.opts = ChromeOptions()

            self.opts.binary_location = config.Locations.operaGX

            # NOTE --headless is not supported by opera

            self.opts.add_argument("--disable-gpu")
            self.opts.add_argument("--log-level=3")
            self.opts.add_argument("--silent")
            self.opts.add_experimental_option("w3c", True)

            self.driver = Opera(options=self.opts, executable_path=DRIVER)
        else:
            self.opts = ChromeOptions()
            if self.nobrowser:
                self.opts.add_argument("--headless")
            self.opts.add_argument("--log-level=3")
            self.opts.add_argument("--silent")
            self.driver = Chrome(options=self.opts, executable_path=DRIVER)

        log("INFO", "starting client...")

        print("\n\033[93mloading login page...", end="\033[92m")
        sleep(0.3)

    def login(self):
        username, password = self.logindata

        self.driver.get(f"https://{self.school}.magister.net")

        if (
            config.BROWSER.startswith("operadriver")
            and len(self.driver.window_handles) > 1
        ):
            self.driver.switch_to.window(self.driver.window_handles[-1])  # switch tabs

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        print("done.\033[0m")

        print("\n\033[93mlogging in...", end="\033[92m")

        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "username_submit").click()
        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "password_submit").click()

        print("done.\033[0m")

        print("\n\033[93mloading home page (this may take a while)...", end="\033[92m")

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "menu-vandaag"))
        )

        print("done.\033[0m")
        """ login successful """

    def agenda_items(self) -> list:
        # TODO implement this

        WebDriverWait(self.driver, 6).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, "icon-calendar"))
        )

        times = [i.text for i in self.driver.find_elements_by_class_name("les-info")]
        # items = [i.text for i in self.driver.find_elements_by_tag_name("td")]
        print(times)

    def go_home(self):
        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "menu-vandaag"))
        )
        self.driver.find_element_by_id("menu-vandaag").click()
        log("INFO", "went to homepage")

    def go_agenda(self):
        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "menu-agenda"))
        )
        self.driver.find_element_by_id("menu-agenda").click()
        log("INFO", "went to agenda page")

    def go_leermiddelen(self):
        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "menu-leermiddelen"))
        )
        self.driver.find_element_by_id("menu-leermiddelen").click()
        log("INFO", "went to leermiddelen page")

    def leermiddelen(self) -> dict:
        self.go_leermiddelen()
        for second in range(1, 6):
            print(
                "\033[92mINFO :\033[0m waiting for leermiddelen to load... [{}/5]".format(
                    second
                ),
                end="\r",
            )
            sleep(1)
        print()

        result = [i.text for i in self.driver.find_elements_by_tag_name("td")]

        if not result:
            log("INFO", "no leermiddelen found.")
            return

        leermiddelen = [
            list(y)
            for x, y in itertools.groupby(result, lambda z: z == "Digitaal")
            if not x
        ]
        for (i, _j) in enumerate(leermiddelen):
            leermiddelen[i] = [x for x in leermiddelen[i] if x != ""]

        leermiddelen_dict = []

        # TODO fix links not working in leermiddelen_dict

        for _, item in enumerate(leermiddelen):
            if len(item) != 3:
                continue
            leermiddelen_dict.append(
                {
                    "vak": item[0],
                    "titel": item[1],
                    "url": self.driver.find_elements_by_tag_name("a")(
                        item[1]
                    ).get_attribute("href"),
                    "ean": item[2],
                }
            )

        return leermiddelen_dict

    def cijfers(self, float_notation=",") -> list[Cijfer]:
        """
        retrieve the list of all the latest grades in the 'cijfers' section on the magister homepage.

        arguments:
            - self
            - float_notation (string) -> default ','\n
            if you want to convert your grades into floats (e.g "6.7" -> 6.7) specify float_notation as '.'
        """

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "menu-cijfers"))
        )
        self.driver.find_element_by_id("menu-cijfers").click()
        log("INFO", "went to 'cijfers'")

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.TAG_NAME, "td"))
        )

        cijfers = []
        sleep(0.5)

        result = [i.text for i in self.driver.find_elements_by_tag_name("td")]

        if config.BROWSER.startswith("chromedriver") or config.BROWSER.startswith(
            "operadriver"
        ):
            cijfers_spl = [
                list(y)
                for x, y in itertools.groupby(result, lambda z: z == " ")
                if not x
            ]
        else:
            cijfers_spl = [
                list(y)
                for x, y in itertools.groupby(result, lambda z: z == "")
                if not x
            ]
        """
        order: [vak, date, description, cijfer, weging]
        dict return:
            {
                "vak": i[0],
                "date": i[1],
                "description": i[2],
                "cijfer": i[3],
                "weging": i[4],
                "inhalen": i[3] == "Inh"
            }
        """
        for i in cijfers_spl:
            c = (
                Cijfer(i[0], i[1], i[2], i[3].replace(",", "."), i[4], i[3] == "Inh")
                if float_notation != ","
                else Cijfer(i[0], i[1], i[2], i[3], i[4], i[3] == "Inh")
            )
            cijfers.append(c)

        return cijfers

    def cijfers_all(self):
        # NOTE work in progress

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "menu-cijfers"))
        )
        self.driver.find_element_by_id("menu-cijfers").click()
        log("INFO", "went to 'cijfers'")

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.TAG_NAME, "dna-button"))
        )
        self.driver.find_element_by_tag_name("dna-button").click()
        log("INFO", "went to 'cijfers uitgebreid'")

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.TAG_NAME, "th"))
        )

        """ loaded uitgebreide cijfers """

        # TODO implement

    def stop(self):
        log("INFO", "stopping driver...")
        self.driver.quit()
        sys.exit(0)
