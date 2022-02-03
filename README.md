# magister-scraper
scraper for Magister 6

**NOTE**: before you can run this, you need to install *selenium*

in order to install selenium, open a terminal and type:  
`python -m pip install selenium`  
or download it from [here](https://pypi.org/project/selenium/).  


---
## download instructions  
click on 'code' then 'download as zip'.  

---
## how to use.  
first, go the directory where you downloaded the zip. (see download instructions).  
unzip it.  
then open the file 'config.py' with notepad or another text editor.  
specify your browser, example:    
`BROWSER = Browsers.chrome`  

then specify your school name, example:  
`SCHOOL = "osghengelo"`  

then specify your login info, example:  
```
LOGIN = (
  "12345",
  "weakPassword"
)
```
