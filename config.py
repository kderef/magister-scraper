from platform import system
from getpass import getuser

running_windows = system() == "Windows"

class Browsers:
    firefox = "geckodriver.exe" if running_windows else "geckodriver"
    chrome  = "chromedriver.exe" if running_windows else "chromedriver"

class Locations:
    operaGX = f"C:\\Users\\{getuser()}\\AppData\\Local\\Programs\\opera.exe"

# -------------------------------------------------- #
# if using chrome or chromium based:
#       BROWSER = Browsers.chrome
# if using firefox or firefox based:
#       BROWSER = Browsers.Firefox
BROWSER = Browsers.firefox
# specify the location of your browser (this only applies if you're using a chromium-based)
USING_OPERA = 0 # set this to 1 if you are using opera or operaGX

# school name, example: SCHOOL = "osghengelo"
SCHOOL = "schoolname"

LOGIN = (
    "username",
    "password"
)
