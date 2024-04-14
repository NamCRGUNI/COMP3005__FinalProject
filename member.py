from database import execute_query, fetch_data
from models import *
from datetime import datetime

def register_member():
    print("Member Registration")
    user_type = input("Enter the user type (Member/Trainer/Admin): ")
    while user_type not in ['Member', 'Trainer', 'Admin']:
        print("Invalid user type. Please enter 'Member', 'Trainer', or 'Admin'.")
        user_type = input("Enter the user type (Member/Trainer/Admin): ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (in kg): "))
    height = float(input("Enter your height (in cm): "))
    gender = input("Enter your gender: ")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    email = input("Enter your email: ")
    user = User.create_user(user_type, first_name, last_name, age, weight, height, gender, username, password, email)
    print("Member registered successfully!")
    print(user)

def update_profile(user_id):
    user = User.get_user_by_id(user_id)
    if user:
        print("Profile Overiew")
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"Age: {user.age}")
        print(f"Weight: {user.weight} kg")
        print(f"Height: {user.height} cm")
        print(f"Gender: {user.gender}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")

        update_choice = input("Do you want to update your profile? (y/n): ")
        if update_choice.lower() == 'y':
            user.age = int(input(f"Enter your age ({user.age}): ") or user.age)
            user.weight = float(input(f"Enter your weight (in kg) ({user.weight}): ") or user.weight)
            user.height = float(input(f"Enter your height (in cm) ({user.height}): ") or user.height)
            # Update other profile fields as needed

            # Update the user record in the database
            query = "UPDATE Users SET Age = %s, Weight = %s, Height = %s WHERE UserID = %s"
            params = (user.age, user.weight, user.height, user.user_id)
            execute_query(query, params)
            print("Profile updated successfully!")
        elif update_choice.lower() == 'n':
            print("No changes made to the profile.")
        else:
            print("Invalid choice. No changes made to the profile.")
    else:
        print("User not found.")

def display_dashboard(user_id):
    user = User.get_user_by_id(user_id)
    if user:
        print("Member Routines and Health Dashboard")
        print(f"Current User, {user.first_name} {user.last_name}!")
        print("Fitness Goals:")
        fitness_goals = FitnessGoal.get_fitness_goals_by_user_id(user_id)
        for goal in fitness_goals:
            print(goal)
        print("Exercise Routines Recommended by Trainers:")
        routines = ExerciseRoutine.get_all_routines()
        for routine in routines:
            print(routine)
        print("Health Statistics:")
        print(f"Age: {user.age}")
        print(f"Weight: {user.weight} kg")
        print(f"Height: {user.height} cm")
    else:
        print("User not found.")

def schedule_session(user_id):
    available_timeslots = Timeslot.get_available_timeslots()
    if available_timeslots:
        print("Available Timeslots:")
        for timeslot in available_timeslots:
            room = [room for room in Room.get_all_rooms() if room.room_id == timeslot.room_id][0]
            trainer = User.get_user_by_id(timeslot.trainer_id)
            print(f"Timeslot ID: {timeslot.timeslot_id}")
            print(f"Day: {timeslot.day}")
            print(f"Time Frame: {timeslot.time_frame}")
            print(f"Room: {room.room_name}")
            print(f"Trainer: {trainer.first_name} {trainer.last_name}")
            print(f"Booking Fee: {timeslot.booking_fee}")
            print("---")

        timeslot_id = int(input("Enter the Timeslot ID to book: "))
        timeslot = next((ts for ts in available_timeslots if ts.timeslot_id == timeslot_id), None)
        if timeslot:
            bill_description = input("Enter the bill description: ")
            date_issued = datetime.now().date()
            pay_now = input("Do you want to pay for the timeslot now? (y/n): ")
            if pay_now.lower() == 'y':
                payment_status = 'Y'
            else:
                payment_status = 'N'
            payment = Payment.create_payment(user_id, timeslot.booking_fee, payment_status, bill_description, date_issued)
            if payment:
                Timeslot.book_timeslot(timeslot_id)
                print("Timeslot booked successfully!")
                if pay_now.lower() == 'y':
                    print(f"Payment Bill: {payment.bill_description} created with status 'Y' (Paid)")
                else:
                    print(f"Payment Bill: {payment.bill_description} created with status 'N' (Unpaid)")
            else:
                print("Failed to create payment.")
        else:
            print(f"Timeslot with ID {timeslot_id} not found or already booked.")
    else:
        print("No available timeslots found.")
        
def manage_fitness_goals(user_id):
    print("Fitness Goal Management")
    fitness_goals = FitnessGoal.get_fitness_goals_by_user_id(user_id)
    if fitness_goals:
        print("Current Fitness Goals:")
        for goal in fitness_goals:
            print(f"Goal ID: {goal.goal_id}, {goal}")
        
        goal_id = int(input("Enter the goal ID to update (0 to add a new goal): "))
        
        if goal_id == 0:
            add_new_goal = input("Do you want to add a new fitness goal? (y/n): ")
            if add_new_goal.lower() == 'y':
                goal_name = input("Enter the goal name: ")
                goal_description = input("Enter the goal description: ")
                start_date = input("Enter the start date (YYYY-MM-DD): ")
                end_date = input("Enter the end date (YYYY-MM-DD): ")
                goal_status = "Not Started"
                fitness_goal = FitnessGoal.create_fitness_goal(user_id, goal_name, goal_status, goal_description, start_date, end_date)
                print(f"Fitness goal created successfully!")
            else:
                print("No changes made to fitness goals.")
        else:
            goal = next((g for g in fitness_goals if g.goal_id == goal_id), None)
            if goal:
                update_choice = input("What would you like to update? (name/status/description/start_date/end_date): ")
                if update_choice.lower() == 'name':
                    new_name = input(f"Enter the new goal name (current: {goal.goal_name}): ")
                    goal.update_goal_name(new_name)
                    print("Goal name updated successfully!")
                elif update_choice.lower() == 'status':
                    new_status = input(f"Enter the new goal status (current: {goal.goal_status}) (Active/Not Started/Completed): ")
                    while new_status not in ['Active', 'Not Started', 'Completed']:
                        print("Invalid goal status. Please enter 'Active', 'Not Started', or 'Completed'.")
                        new_status = input(f"Enter the new goal status (current: {goal.goal_status}) (Active/Not Started/Completed): ")
                    goal.update_goal_status(new_status)
                    print("Goal status updated successfully!")
                elif update_choice.lower() == 'description':
                    new_description = input(f"Enter the new goal description (current: {goal.goal_description}): ")
                    goal.update_goal_description(new_description)
                    print("Goal description updated successfully!")
                elif update_choice.lower() == 'start_date':
                    new_start_date = input(f"Enter the new start date (current: {goal.start_date}) (YYYY-MM-DD): ")
                    goal.update_start_date(new_start_date)
                    print("Start date updated successfully!")
                elif update_choice.lower() == 'end_date':
                    new_end_date = input(f"Enter the new end date (current: {goal.end_date}) (YYYY-MM-DD): ")
                    goal.update_end_date(new_end_date)
                    print("End date updated successfully!")
                else:
                    print("Invalid choice. No changes made to fitness goals.")
            else:
                print("Invalid goal ID. No changes made to fitness goals.")
    else:
        print("No fitness goals found.")
        add_new_goal = input("Do you want to add a new fitness goal? (y/n): ")
        if add_new_goal.lower() == 'y':
            goal_name = input("Enter the goal name: ")
            goal_description = input("Enter the goal description: ")
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            goal_status = "Not Started"
            fitness_goal = FitnessGoal.create_fitness_goal(user_id, goal_name, goal_status, goal_description, start_date, end_date)
            print(f"Fitness goal created successfully!")
        else:
            print("No changes made to fitness goals.")