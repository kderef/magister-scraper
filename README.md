# magister-scraper
scraper for Magister 6.  
if you encounter any issues or errors, post them in [the issues tab](https://github.com/x-kvoid-x/magister-scraper/issues).

**NOTE**: before you can run this, you need to install *selenium*

in order to install selenium, open a terminal and type:  
```bash
python -m pip install selenium
```

or download it from [here](https://pypi.org/project/selenium/).  


---
## download instructions  
click on [this](https://github.com/x-kvoid-x/magister-scraper/archive/refs/heads/main.zip). 

---
## how to use.  
first, go the directory where you downloaded the zip. (see download instructions).  
unzip it.  
then open the file 'config.py' with notepad or another text editor.  
specify your browser, example:    
```python
BROWSER = Browsers.chrome
```

then specify your school name, example:  
```python 
SCHOOL = "osghengelo"
```   

then specify your login info, example:  
```python
LOGIN = (
  "12345",
  "weakPassword"
)
```

## NOTE: this project is on hold and not being worked on
