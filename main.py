from magister import *

def main():
  m = Magister()
  m.login()
  
  cijfers = m.cijfers()
  
  print("laatste cijfers:\n")
  print(cijfers)
 
if __name__ == "__main__":
  main()
