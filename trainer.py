from database import execute_query, fetch_data
from models import *

def set_trainer_availability(trainer_id):
    print("Trainer Availability Management")
    trainer_availabilities = TrainerAvailability.get_trainer_availability_by_user_id(trainer_id)

    if trainer_availabilities:
        print(f"Current Trainer Availability for User ID: {trainer_id}")
        for availability in trainer_availabilities:
            print(f"Availability ID: {availability.availability_id}, {availability}")
    else:
        print(f"No current availabilities found for UserId which is a Trainer: {trainer_id}")

    choice = input("Enter your choice (1. Add, 2. Delete, 3. Exit): ")

    if choice == "1":
        time_frame = input("Enter the time frame (Morning/Afternoon): ")
        day = input("Enter the day: ")
        availability = TrainerAvailability(None, trainer_id, time_frame, day)
        query = "INSERT INTO TrainerAvailability (UserID, TimeFrame, Day) VALUES (%s, %s, %s) RETURNING AvailabilityID"
        params = (availability.user_id, availability.time_frame, availability.day)
        availability_id = execute_query(query, params)
        availability.availability_id = availability_id
        print("Trainer availability added successfully!")

    elif choice == "2":
        if trainer_availabilities:
            availability_id = int(input("Enter the Availability ID to delete: "))
            availability = next((a for a in trainer_availabilities if a.availability_id == availability_id), None)
            if availability:
                query = "DELETE FROM TrainerAvailability WHERE AvailabilityID = %s"
                params = (availability_id,)
                execute_query(query, params)
                print("Trainer availability deleted successfully!")
            else:
                print(f"Availability ID {availability_id} not found.")
        else:
            print("No availabilities to delete.")

    elif choice == "3":
        print("Exiting Trainer Availability Management.")
        return

    else:
        print("Invalid choice. Please try again.")
        set_trainer_availability(trainer_id)

def view_member_profile():
    search_choice = input("Do you want to search by name or username? (n/u): ")
    if search_choice.lower() == 'n':
        first_name = input("Enter the member's first name: ")
        last_name = input("Enter the member's last name: ")
        members = User.get_users_by_name(first_name, last_name)
        if members:
            print("Members Found:")
            for member in members:
                print(f"Name: {member.first_name} {member.last_name}")
                print(f"Age: {member.age}")
                print(f"Height: {member.height} cm")
                print(f"Weight: {member.weight} kg")
                print("Fitness Goals:")
                fitness_goals = FitnessGoal.get_fitness_goals_by_user_id(member.user_id)
                if fitness_goals:
                    for goal in fitness_goals:
                        print(f"- {goal.goal_name}: {goal.goal_description}")
                else:
                    print("No fitness goals found.")
                print("-" * 20)
        else:
            print("No members found with the given name.")
    elif search_choice.lower() == 'u':
        username = input("Enter the member's username: ")
        member = User.get_user_by_username(username)
        if member:
            print("Member Profile")
            print(f"Name: {member.first_name} {member.last_name}")
            print(f"Age: {member.age}")
            print(f"Height: {member.height} cm")
            print(f"Weight: {member.weight} kg")
            print("Fitness Goals:")
            fitness_goals = FitnessGoal.get_fitness_goals_by_user_id(member.user_id)
            if fitness_goals:
                for goal in fitness_goals:
                    print(f"- {goal.goal_name}: {goal.goal_description}")
            else:
                print("No fitness goals found.")
        else:
            print("Member not found.")
    else:
        print("Invalid choice.")

def view_trainer_schedule(trainer_id):
    timeslots = Timeslot.get_timeslots_by_trainer_id(trainer_id)
    if timeslots:
        print(f"Trainer Schedule for Trainer ID: {trainer_id}")
        for timeslot in timeslots:
            room = Room.get_all_rooms()[timeslot.room_id - 1]  # Assuming room_id starts from 1
            print(f"Timeslot ID: {timeslot.timeslot_id}")
            print(f"Booked: {timeslot.is_booked}")
            print(f"Day: {timeslot.day}")
            print(f"Time Frame: {timeslot.time_frame}")
            print(f"Room: {room.room_name}")
            print(f"Booking Fee: {timeslot.booking_fee}")
            print("---")
    else:
        print(f"No scheduled timeslots found for Trainer ID: {trainer_id}")

def update_trainer_schedule(trainer_id):
    timeslots = Timeslot.get_timeslots_by_trainer_id(trainer_id)
    if timeslots:
        print(f"Trainer Schedule for Trainer ID: {trainer_id}")
        for timeslot in timeslots:
            room = Room.get_all_rooms()[timeslot.room_id - 1]  # Assuming room_id starts from 1
            print()
            print(f"Timeslot ID: {timeslot.timeslot_id}")
            print(f"Booked: {timeslot.is_booked}")
            print(f"Day: {timeslot.day}")
            print(f"Time Frame: {timeslot.time_frame}")
            print(f"Room: {room.room_name}")
            print(f"Booking Fee: {timeslot.booking_fee}")
            print("---")
        timeslot_id = int(input("Enter the Timeslot ID to update: "))
        timeslot = next((ts for ts in timeslots if ts.timeslot_id == timeslot_id), None)
        if timeslot:
            new_is_booked = input(f"Enter the new booking status (current: {timeslot.is_booked}): ")
            new_time_frame = input(f"Enter the new time frame (current: {timeslot.time_frame}): ")
            new_day = input(f"Enter the new day (current: {timeslot.day}): ")
            new_room_id = int(input(f"Enter the new room ID (current: {timeslot.room_id}): "))
            new_booking_fee = float(input(f"Enter the new booking fee (current: {timeslot.booking_fee}): "))
            query = "UPDATE Timeslots SET IsBooked = %s, TimeFrame = %s, Day = %s, RoomID = %s, BookingFee = %s WHERE TimeslotID = %s"
            params = (new_is_booked, new_time_frame, new_day, new_room_id, new_booking_fee, timeslot_id)
            execute_query(query, params)
            print("Timeslot updated successfully!")
        else:
            print(f"Timeslot with ID {timeslot_id} not found.")
    else:
        print(f"No scheduled timeslots found for Trainer ID: {trainer_id}")
        
def create_new_timeslot(trainer_id):
    print("Create New Timeslot")

    # Get the available rooms
    rooms = Room.get_all_rooms()
    if not rooms:
        print("No rooms available. Please add rooms first.")
        return

    # Display available rooms
    print("Available Rooms:")
    for room in rooms:
        print(f"Room ID: {room.room_id}, Room Name: {room.room_name}")

    # Get the room ID from the user
    room_id = int(input("Enter the Room ID: "))

    # Check if the room ID is valid
    room = next((r for r in rooms if r.room_id == room_id), None)
    if not room:
        print("Invalid Room ID.")
        return

    # Get the other timeslot details from the user
    booking_fee = float(input("Enter the Booking Fee: "))
    time_frame = input("Enter the Time Frame (Morning/Afternoon): ")
    day = input("Enter the Day: ")

    # Create the new timeslot
    timeslot = Timeslot.create_timeslot(booking_fee, room_id, trainer_id, time_frame, day)
    print(f"Timeslot created successfully!")

def add_exercise_routine(trainer_id):
    existing_routines = ExerciseRoutine.get_all_routines()
    if existing_routines:
        print("Existing Exercise Routines:")
        for routine in existing_routines:
            print(f"Routine Name: {routine.routine_name}")
            print(f"Description: {routine.routine_description}")
            print(f"Routine Type: {routine.routine_type}")
            print("-" * 20)

    add_new_routine = input("Do you want to add a new exercise routine? (y/n): ")
    if add_new_routine.lower() == 'y':
        print("Add Exercise Routine")
        routine_name = input("Enter the routine name: ")
        routine_description = input("Enter the routine description: ")
        routine_type = input("Enter the routine type (Upper Body/Lower Body/Core/Cardio): ")
        while routine_type not in ['Upper Body', 'Lower Body', 'Core', 'Cardio']:
            print("Invalid routine type. Please enter 'Upper Body', 'Lower Body', 'Core', or 'Cardio'.")
            routine_type = input("Enter the routine type (Upper Body/Lower Body/Core/Cardio): ")

        new_routine = ExerciseRoutine.create_exercise_routine(routine_name, routine_description, routine_type)
        print(f"New exercise routine added successfully! Routine Name: {new_routine.routine_name}")
    elif add_new_routine.lower() == 'n':
        print("Exiting without adding a new routine.")
    else:
        print("Invalid choice.")