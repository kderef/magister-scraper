from magister import *

def main():
  login = (
    "username",
    "password",
  )
  
  m = Magister("schoolname", login)
  m.login()
  
  cijfers = m.cijfers()
  print(m)

if __name__ == "__main__":
  main()
