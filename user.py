# create a class for users wiht property of username, pw, firstname, lastname, and tasks

class User:

  def __init__(self, username, password, fname, lname, tasks):
    self.username = username
    self.password = password
    self.fname = fname
    self.lname = lname
    self.tasks = tasks
    self.keys = None

  @property
  def user_fullname(self):
    return f'{self.fname} {self.lname}'