from db_api import get_user_pw, get_user_by_username, create_user
from user import User
from bcrypt import gensalt, hashpw, checkpw



def ask_credentials():
  username = input('\nusername: ')
  password = input('password: ')

  return (username, password)

def get_new_credentials(new_username,new_password):
  new_username = new_username
  new_password = new_password

  return (new_username, new_password)

#check for username uniqueness, if unique = true, otherwise false
def check_for_unique_username(new_username):
  if not get_user_by_username(new_username):
    return True
  else:
    return False

def add_new_credentials(new_username,new_password, new_fname, new_lname):
  salt = gensalt()
  new_password = new_password.encode()
  hashed_pw = hashpw(new_password, salt)
  
  new_user = User(new_username,hashed_pw, new_fname, new_lname, None)
  
  create_user(new_user)

def check_correct_credentials(credentials):
  if not get_user_by_username(credentials[0]):
    return False
  else:
    if checkpw(credentials[1].encode(), get_user_pw(credentials[0])[0]):
        return True
    else:
      return False