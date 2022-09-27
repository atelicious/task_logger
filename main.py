"""
App Name: Task Logger v1
Author: @atelicious
Description:
The first functional version of the "tasklistapp", which is an app where the user could
create a user profile and create, edit and delete tasks specific to that user.
"""

import login_api, db_api, os
from time import sleep
from datetime import datetime
from cryptography.fernet import Fernet

def banner():
  print('='.ljust(59,'='))
  print('Task Logger v1.0'.center(60))
  print('='.ljust(59,'='))
  
def main_menu(current_user):
  fullname = db_api.get_fullname(current_user)[0]
  date_today = datetime.now().strftime("%B %d, %Y")
  print(f'\nWelcome {fullname.title()}')
  print(f'Today is {date_today}')
  print('\n1. View current tasks\n2. Create new task\n3. Modify existing tasks\n4. Delete task(s)\n5. Logout\n6. Exit program\n')

def validate_yn_input(input):
  input = input.strip().lower()
  if input == 'y':
    return 'y'
  elif input == 'n':
    return 'n'
  else:
    return 'invalid'

def validate_num_input(input, range):
  try:
    input = int(input.strip())
    if range[0] <= input <= range[1]:
      return input
    else:
      return 'invalid'
  except:
    return 'invalid'
    
def clear_screen():
  #os.system('cls') - for windows
  #os.system('clear') = for mac/linux
  os.system('clear')

def get_current_tasks(current_user):
  current_tasks = db_api.get_current_task(current_user)[0]

  if current_tasks == None:
    return []
  else:
    key = db_api.get_user_key(current_user)[0]
    fernet = Fernet(key)
    current_tasks = fernet.decrypt(current_tasks).decode()
    return current_tasks.split('***')
  
  
def display_tasks(current_user):
  current_tasks = get_current_tasks(current_user)
  
  if not current_tasks:
    print('\nThere are no current tasks for you today.')
  else:
    index = 0
    print('\nThese are your tasks for today: \n')
    for tasks in current_tasks:
      print(f'{index + 1}. {tasks}')
      index += 1
    print('\n='.ljust(29,'='))
    
def update_tasks(current_user, tasks):
  modified_tasks = tasks

  if not modified_tasks:
    db_api.update_task(current_user, None)
  else:
    new_modified_tasks = [f'{items}***' for items in modified_tasks if modified_tasks.index(items) in range(0, len(modified_tasks)-1)]
    new_modified_tasks.append(f'{modified_tasks[len(modified_tasks)-1]}')
    new_modified_tasks = ''.join(new_modified_tasks)

    if db_api.get_user_key(current_user)[0] == None:
      key = Fernet.generate_key()
      fernet = Fernet(key)
      new_modified_tasks = fernet.encrypt(new_modified_tasks.encode())
      db_api.update_keys(current_user, key)
      db_api.update_task(current_user, new_modified_tasks)
    else:
      key = db_api.get_user_key(current_user)[0]
      fernet = Fernet(key)
      new_modified_tasks = fernet.encrypt(new_modified_tasks.encode())
      db_api.update_task(current_user, new_modified_tasks)
      
def main():
  banner()
  login_state = False
  login_counter = 5
  current_user = None

  print('\nAvailable options:\n1. Login\n2. Register a new account\n3. Exit application')
  ask_input = validate_num_input(input('\nYour choice: '), [1,3])

  if ask_input == 1:
    while login_state == False and login_counter != 0:
      credentials = login_api.ask_credentials()
      if login_api.check_correct_credentials(credentials) == True:
        login_state = True
        print('Login successful, redirecting to main page.')
        current_user = credentials[0]
        sleep(5)
        clear_screen()
        break
      else:
        login_counter = login_counter -1
        print('Wrong credentials.')
        continue
        
      if login_state == False and login_counter == 0:
        print('You are blocked for 5 minutes')
        sleep(300)
        break

    while login_state == True:
      clear_screen()
      banner()
      main_menu(current_user)
      ask_input = input('Your choice? (1-6): ')
      ask_input = validate_num_input(ask_input, [0,6])


      if ask_input == 1:
        while True:
          clear_screen()
          banner()
          display_tasks(current_user)
          print('\nAvailable options:\n1. Return to main menu')
          ask_input = validate_num_input(input('\nYour choice: '), [1,1])
          
          if ask_input == 1:
            break
          else:
            print('Invalid choice, please try again')
            sleep(1)
            continue

      elif ask_input == 2:
        while True:
          clear_screen()
          banner()
          display_tasks(current_user)
          print('\nAvailable options:\n1. Add a new task\n2. Return to main menu')
          ask_input = validate_num_input(input('\nYour choice: '), [1,2])
          
          current_tasks = get_current_tasks(current_user)
          
          if ask_input == 1:
            while True:
              new_task = input('\nAdd your new task here: ')
              ask_input = validate_yn_input(input(f'\nAdd "{new_task}" in your tasks? (y/n): '))
        
              if ask_input == 'y':
                current_tasks.append(new_task)
                update_tasks(current_user, current_tasks)
                print(f'\nYou have successfully added "{new_task}" in your list.')
                sleep(3)
                break
              elif ask_input == 'n':
                break
              else:
                print('Invalid choice, please try again.')
                sleep(1)
                continue
          
          elif ask_input == 2:
            break
          else:
            print('Invalid choice, please try again.')
            sleep(1)
            continue
        
      elif ask_input == 3:
        while True:
          clear_screen()
          banner()
          display_tasks(current_user)
          print('\nAvailable options:\n1. Modify a task\n2. Return to main menu')
          ask_input = validate_num_input(input('\nYour choice: '), [1,2])
        
          current_tasks = get_current_tasks(current_user)
          
          if ask_input == 1:
            while True:
              try:
                index = validate_num_input(input(f'\nPick a task you want to modify (1-{len(current_tasks)}): '), [1,len(current_tasks)])
                new_task = input('\nEnter your new task here: ')
                ask_input = validate_yn_input(input(f'\nChange "{current_tasks[index-1]}" to "{new_task}" ? (y/n):'))
        
                if ask_input == 'y':
                  current_tasks = current_tasks[:index-1] + [new_task] + current_tasks[index:]
                  update_tasks(current_user, current_tasks)
        
                  print(f'\nYou have succesfully modified your previous task to "{new_task}"')
                  sleep(5)
                  break
                elif ask_input == 'n':
                  break
                else:
                  print('Invalid choice, please try again.')
                  sleep(1)
              except:
                print('Invalid choice, please try again.')
                sleep(1)
                break
  
          elif ask_input == 2:
            break
          else:
            print('Invalid choice, please try again.')

      elif ask_input == 4:
        while True:
          clear_screen()
          banner()
          display_tasks(current_user)
          print('\nAvailable options:\n1. Delete a task\n2. Return to main menu')
          ask_input = validate_num_input(input('\nYour choice: '), [1,2])
        
          current_tasks = get_current_tasks(current_user)
          
          if ask_input == 1:
            while True:
              try:
                index = validate_num_input(input(f'\nPick a task you want to delete (1-{len(current_tasks)}): '), [1,len(current_tasks)])
                ask_input = validate_yn_input(input(f'\nDelete "{current_tasks[index-1]}" ? (y/n):'))
        
                if ask_input == 'y':
                  current_tasks.pop(index-1)
                  update_tasks(current_user, current_tasks)
                  print('\nYou have succesfully deleted your task')
                  sleep(5)
                  break
                elif ask_input == 'n':
                  break
                else:
                  print('Invalid choice, please try again.')
                  sleep(1)
              except:
                print('Invalid choice, please try again.')
                sleep(1)
                break
                
          elif ask_input == 2:
            break
          else:
            sleep(1)
            print('Invalid choice, please try again.')
    
      elif ask_input == 5:
        ask_input = validate_yn_input(input('Do you want to log out? (y/n): '))

        if ask_input == 'y':
          login_state = False
          login_counter = 5
          current_user = None
          clear_screen()
        elif ask_input == 'n':
          clear_screen()
          continue
        else:
          print('Invalid input, please try again')
          sleep(1)
          continue
        
      elif ask_input == 6:
        os.sys.exit()
        
      else:
        print('Invalid choice, plaease try again')
        sleep(1)
        
  elif ask_input == 2:
    while True:
      clear_screen()
      banner()
      print('\nRegister a new account'.center(60))
      
      new_username = input('\nEnter your username: ')
      
      if login_api.check_for_unique_username(new_username) == True:
        new_pw = input('\nEnter your password: ')
        new_fname = input('\nEnter your first name: ')
        new_lname = input('\nEnter your last name: ')
        login_api.add_new_credentials(new_username, new_pw, new_fname, new_lname)
        print('\nRegistration succesfull, returning to main menu')
        sleep(3)
        clear_screen()
        break
      else:
        print(f'\n{new_username} is taken, please use another username')
        sleep(3)

  elif ask_input == 3:
    os.sys.exit()
  else:
    print('Invalid choice, please try again')
    sleep(1)
    clear_screen()
  
# for the main loop of the application

main_loop = True 

while main_loop == True:
  main()

