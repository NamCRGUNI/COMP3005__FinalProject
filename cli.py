from database import execute_query, fetch_data
from models import *
from member import *
from trainer import *
from admin import *
import os
import time

def clear_screen():
    time.sleep(2)  # Delay for 2 seconds
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/macOS
    else:
        os.system('clear')

def change_password():
    username = input("Enter your username: ")
    user = User.get_user_by_username(username)
    if user:
        current_password = input("Enter your current password: ")
        if current_password == user.password:
            new_password = input("Enter your new password: ")
            confirm_password = input("Confirm your new password: ")
            if new_password == confirm_password:
                query = "UPDATE Users SET Password = %s WHERE UserID = %s"
                params = (new_password, user.user_id)
                execute_query(query, params)
                print("Password changed successfully!")
                print()
            else:
                print("New password and confirmation do not match. Password not changed.")
                
        else:
            print("Incorrect current password. Password not changed.")
            print()
    else:
        print("Invalid username. Password not changed.")
        print()

def main_menu():
    while True:
        clear_screen()
        print("=" * 33)
        print("==== Welcome to Fitness Club ====")
        print("=" * 33)
        print("1. Register")
        print("2. Login")
        print("3. Change Password")
        print("4. Exit")
        print("-" * 33)
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            register_member()
        elif choice == "2":
            login()
        elif choice == "3":
            change_password()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    query = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
    params = (username, password)
    user_data = fetch_data(query, params)

    if user_data:
        user = User(*user_data[0])
        print()
        print(f"User type: {user.user_type}")  
        if user.user_type == "Member":
            print("Switching to member menu...")  
            member_menu(user)
        elif user.user_type == "Trainer":
            print("Switching to trainer menu...")  
            trainer_menu(user)
        elif user.user_type == "Admin":
            print("Switching to admin menu...")  
            admin_menu(user)
    else:
        print("Invalid username or password.")

def member_menu(user):
    while True:
        clear_screen()
        header_len = len(f"Welcome, {user.first_name} {user.last_name}") + 10
        header = "=" * header_len
        print(header)
        print(f"==== Welcome, {user.first_name} {user.last_name} ====")
        print(header)
        print("1. Profile Management")
        print("2. Dashboard Display")
        print("3. Schedule Booking and Timeslots Management")
        print("4. Fitness Goal Management")
        print("5. Exit")
        print("-" * 32)
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            update_profile(user.user_id)
        elif choice == "2":
            display_dashboard(user.user_id)
        elif choice == "3":
            schedule_session(user.user_id)
        elif choice == "4":
            manage_fitness_goals(user.user_id)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def trainer_menu(user):
    while True:
        clear_screen()
        header_len = len(f"Welcome, Trainer {user.first_name} {user.last_name}") + 10
        header = "=" * header_len
        print(header)
        print(f"==== Welcome, Trainer {user.first_name} {user.last_name} ====")
        print(header)
        print("1. Weekday Availability Schedule Management")
        print("2. Member Profile Viewing")
        print("3. View Trainer Schedule")
        print("4. Update Trainer Schedule")
        print("5. Create New Timeslot")
        print("6. Exercise Routine Management")
        print("7. Exit")
        print("-" * 40)
        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            set_trainer_availability(user.user_id)
        elif choice == "2":
            view_member_profile()
        elif choice == "3":
            view_trainer_schedule(user.user_id)
        elif choice == "4":
            update_trainer_schedule(user.user_id)
        elif choice == "5":
            create_new_timeslot(user.user_id)
        elif choice == "6":
            add_exercise_routine(user.user_id)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def admin_menu(user):
    while True:
        clear_screen()
        header_len = len(f"Welcome, Admin {user.first_name} {user.last_name}") + 10
        header = "=" * header_len
        print(header)
        print(f"==== Welcome, Admin {user.first_name} {user.last_name} ====")
        print(header)
        print("1. Room Booking Management")
        print("2. Equipment Management and Maintenance Monitoring")
        print("3. Trainer Weekday Availability Schedule Updating")
        print("4. Billing and Payment Processing")
        print("5. Update Timeslot Details")
        print("6. Exit")
        print("-" * 40)
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            manage_room_bookings()
        elif choice == "2":
            monitor_equipment_maintenance()
        elif choice == "3":
            update_admin_schedule()
        elif choice == "4":
            process_billing_and_payments()
        elif choice == "5":
            update_timeslot_details()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")