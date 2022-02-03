from platform import system
from getpass import getuser

RUNNING_WINDOWS = (system() == "Windows")

class Browsers:
    firefox = "geckodriver.exe" if RUNNING_WINDOWS else "geckodriver"
    chrome  = "chromedriver.exe" if RUNNING_WINDOWS else "chromedriver"
    opera = "operadriver.exe"

class Locations:
    operaGX = f"C:\\Users\\{getuser()}\\AppData\\Local\\Programs\\Opera GX\\opera.exe"

# -------------------------------------------------- #
"""
if using chrome:
    BROWSER = Browsers.chrome
if using operaGX:
    BROWSER = Browsers.opera
if using firefox:
    BROWSER = Browsers.firefox
"""
BROWSER = Browsers.opera

# school name, example: SCHOOL = "osghengelo"
SCHOOL = "osghengelo"

# specifies whether the browser window will be visible or not
# values: True or False
WINDOW_VISIBLE = False

LOGIN = (
    "username",
    "password"
)
