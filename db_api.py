import sqlite3
from user import User

conn = sqlite3.connect('user_db.db')

#for testing purposes only, will be changed to static db once testin is finished
# conn = sqlite3.connect(':memory:')

c = conn.cursor()

#initialize main user table with 5 columns (username, password, firstname, lastname, tasks)

try:
  c.execute("""CREATE TABLE user_table (username text, password text, fname text, lname text, tasks text, fullname text, keys text) """)
except sqlite3.OperationalError:
  pass

#create methods for user registration

#search db by username
def get_user_by_username(username):
  with conn:
    c.execute("SELECT * FROM user_table WHERE username =:username",{'username':username})
  return c.fetchall()

#create a new user

def create_user(user):
  with conn:
    c.execute("INSERT INTO user_table VALUES (:username, :password, :fname, :lname, :tasks, :fullname, :keys)", {'username':user.username, 'password':user.password, 'fname':user.fname, 'lname':user.lname, 'tasks':user.tasks, 'fullname':user.user_fullname, 'keys':user.keys})

#for testing purposes only, creating an inital user with tasks loaded

a = User('user0', 'password0', 'User01Fname', 'User01Lname','first task ***second task ***third task ')

create_user(a)

#search user by username (will be used for username checking)

def get_user_username(username):
  with conn:
    c.execute("SELECT * FROM user_table WHERE username =:username", {'username':username})
  return c.fetchone()

#get fullname of user
def get_fullname(username):
  with conn:
    c.execute("SELECT fullname FROM user_table WHERE username =:username", {'username':username})
  return c.fetchone()

#get key for user
def get_user_key(username):
  with conn:
    c.execute("SELECT keys FROM user_table WHERE username =:username", {'username':username})
  return c.fetchone()

#get user password for login verification

def get_user_pw(username):
  with conn:
    c.execute("SELECT password FROM user_table WHERE username =:username", {'username':username})
  return c.fetchone()

#methods for updating data in profile
  
#for updating user's first name
def update_fname(username, new_fname):
  with conn:
    c.execute("UPDATE user_table SET fname =:new_fname WHERE username =:username ", {'username':username, 'fname':new_fname})

#for updating user's last name
def update_lname(username, new_lname):
  with conn:
    c.execute("UPDATE user_table SET lname =:new_lname WHERE username =:username ", {'username':username, 'new_lname':new_lname})

#for updating user tasks

def get_current_task(username):
  with conn:
    c.execute("SELECT tasks FROM user_table WHERE username =:username", {'username':username})
  return c.fetchone()

def update_task(username, new_tasks):
  with conn:
    c.execute("UPDATE user_table SET tasks = :new_tasks WHERE username = :username", {'username':username, 'new_tasks':new_tasks})

#update user key
def update_keys(username, keys):
  with conn:
    c.execute("UPDATE user_table SET keys = :keys WHERE username = :username", {'username':username, 'keys':keys})