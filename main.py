from magister import *

def main():
  m = Magister()
  m.login()
  
  cijfers = m.cijfers()
  
  print("laatste cijfers:\n")
  for cijfer in cijfers:
    print(cijfer.vak, cijfer.description, cijfer.cijfer, cijfer.type)
 
if __name__ == "__main__":
  main()
