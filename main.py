import menu_functions as f
import os

os.chdir(os.path.dirname(__file__))

while True:
    command = input("Choose a menu option (Enter a command):\n"
                    "1. Show current funds\n"
                    "2. Expenses per month\n"
                    "3. Exit from the program\n")
    if command == '1':
        f.show_current_funds()
    elif command == '2':
        f.expenses_per_month()
    elif command == '3':
        break
    else:
        print("Error: incorrect command")
