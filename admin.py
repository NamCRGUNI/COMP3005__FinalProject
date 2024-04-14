from database import execute_query, fetch_data
from models import *

def manage_room_bookings():
    print("Room Booking Management")
    rooms = Room.get_all_rooms()
    if rooms:
        print()
        print("Available Rooms:")
        print()
        for room in rooms:
            # Check if the room is booked
            booked_timeslots = Timeslot.get_booked_timeslots_by_room_id(room.room_id)
            if booked_timeslots:
                booked_status = "Booked"
            else:
                booked_status = "Available"
            print(f"Room ID: {room.room_id}, Name: {room.room_name}, Capacity: {room.capacity}, Status: {booked_status}")
        print()
        add_room_choice = input("Do you want to add a new room? (y/n): ")
        if add_room_choice.lower() == 'y':
            room_name = input("Enter the room name: ")
            room_capacity = int(input("Enter the room capacity: "))
            new_room = Room.create_room(room_name, room_capacity)
            print(f"New room created successfully!")
        else:
            print("No new room added.")
    else:
        print("No rooms found.")
        add_room_choice = input("Do you want to add a new room? (y/n): ")
        if add_room_choice.lower() == 'y':
            room_name = input("Enter the room name: ")
            room_capacity = int(input("Enter the room capacity: "))
            new_room = Room.create_room(room_name, room_capacity)
            print(f"New room created successfully!")
        else:
            print("No new room added.")

def monitor_equipment_maintenance():
    print()
    print("Equipment Maintenance Monitoring")
    equipment_list = Equipment.get_all_equipment()
    if equipment_list:
        for equipment in equipment_list:
            equipment_type = EquipmentType.get_all_equipment_types()[equipment.equipment_type_id - 1]
            print(f"Equipment ID: {equipment.equipment_id}, Name: {equipment_type.equipment_name}, Status: {equipment.equipment_status}")
        equipment_id = input("Enter the equipment ID to update status, 'a' to add new equipment, or 'q' to quit: ")
        if equipment_id.lower() == 'q':
            print("Exiting without making any changes.")
            print()
            return
        elif equipment_id.lower() == 'a':
            add_new_equipment()
        else:
            equipment_id = int(equipment_id)
            equipment = next((eq for eq in equipment_list if eq.equipment_id == equipment_id), None)
            if equipment:
                print()
                new_status = input("Enter the new status (Good/Broken): ")
                Equipment.update_equipment_status(equipment_id, new_status)
                print("Equipment status updated successfully!")
            else:
                print("Invalid equipment ID.")
    else:
        print("No equipment found.")
        add_new_equipment_choice = input("Do you want to add new equipment? (y/n): ")
        if add_new_equipment_choice.lower() == 'y':
            add_new_equipment()
        else:
            print("No new equipment added.")

def add_new_equipment():
    equipment_types = EquipmentType.get_all_equipment_types()
    if equipment_types:
        print("Available Equipment Types:")
        for equipment_type in equipment_types:
            print(f"Equipment Type ID: {equipment_type.equipment_type_id}, Name: {equipment_type.equipment_name}")
        equipment_type_id = input("Enter the Equipment Type ID, or 'n' to add a new type: ")
        if equipment_type_id.lower() == 'n':
            equipment_name = input("Enter the new equipment type name: ")
            new_equipment_type = EquipmentType.create_equipment_type(equipment_name)
            equipment_type_id = new_equipment_type.equipment_type_id
            print(f"New equipment type added successfully!")
        else:
            equipment_type_id = int(equipment_type_id)
            equipment_type = next((et for et in equipment_types if et.equipment_type_id == equipment_type_id), None)
            if equipment_type:
                initial_status = input("Enter the initial status (Good/Broken): ")
                new_equipment = Equipment.create_equipment(equipment_type_id, initial_status)
                print(f"New equipment added successfully!")
            else:
                print("Invalid Equipment Type ID.")
    else:
        equipment_name = input("Enter the new equipment type name: ")
        new_equipment_type = EquipmentType.create_equipment_type(equipment_name)
        equipment_type_id = new_equipment_type.equipment_type_id
        print(f"New equipment type added successfully!")
        initial_status = input("Enter the initial status (Good/Broken): ")
        new_equipment = Equipment.create_equipment(equipment_type_id, initial_status)
        print(f"New equipment added successfully!")


def update_admin_schedule():
    print("Update Trainer Schedule")
    trainers = User.get_all_trainers()
    if trainers:
        for trainer in trainers:
            print(f"Trainer ID: {trainer.user_id}, Name: {trainer.first_name} {trainer.last_name}")
        trainer_id = int(input("Enter the Trainer ID: "))
        trainer = next((t for t in trainers if t.user_id == trainer_id), None)
        if trainer:
            availability = TrainerAvailability.get_trainer_availability_by_user_id(trainer_id)
            if availability:
                print(f"Trainer Availability for {trainer.first_name} {trainer.last_name}:")
                for av in availability:
                    print(f"Availability ID: {av.availability_id}, Day: {av.day}, Time Frame: {av.time_frame}")
                choice = input("Enter your choice (1. Update Availability, 2. Exit): ")
                if choice == "1":
                    availability_id = int(input("Enter the Availability ID to update: "))
                    av = next((a for a in availability if a.availability_id == availability_id), None)
                    if av:
                        new_time_frame = input(f"Enter the new time frame (Morning/Afternoon) (current: {av.time_frame}): ")
                        new_day = input(f"Enter the new day (current: {av.day}): ")
                        query = "UPDATE TrainerAvailability SET TimeFrame = %s, Day = %s WHERE AvailabilityID = %s"
                        params = (new_time_frame, new_day, availability_id)
                        execute_query(query, params)
                        print("Trainer availability updated successfully!")
                    else:
                        print("Invalid Availability ID.")
                elif choice == "2":
                    print("Exiting without updating availability.")
                else:
                    print("Invalid choice.")
            else:
                print("No availability found for this trainer.")
        else:
            print("Invalid Trainer ID.")
    else:
        print("No trainers found.")
        
def process_billing_and_payments():
    print("Billing and Payment Processing")
    payments = Payment.get_all_payments()
    if payments:
        print("Payments:")
        for payment in payments:
            user = User.get_user_by_id(payment.user_id)
            if user:
                print(f"Payment ID: {payment.payment_id}, User: {user.first_name} {user.last_name}, Amount: {payment.booking_fee}, Status: {payment.payment_status}")
            else:
                print(f"Payment ID: {payment.payment_id}, User ID: {payment.user_id}, Amount: {payment.booking_fee}, Status: {payment.payment_status}")
        update_payment_status = input("Do you want to update any payment status to 'Y'? (y/n): ")
        if update_payment_status.lower() == 'y':
            payment_id = int(input("Enter the Payment ID to update status: "))
            payment = next((p for p in payments if p.payment_id == payment_id), None)
            if payment:
                Payment.update_payment_status(payment_id, 'Y')
                print("Payment status updated successfully!")
            else:
                print("Invalid Payment ID.")
    else:
        print("No payments found.")
        
        
def update_timeslot_details():
    print("Update Timeslot Details")
    trainers = User.get_all_trainers()
    if trainers:
        for trainer in trainers:
            print(f"Trainer ID: {trainer.user_id}, Name: {trainer.first_name} {trainer.last_name}")
        trainer_id = int(input("Enter the Trainer ID: "))
        trainer = next((t for t in trainers if t.user_id == trainer_id), None)
        if trainer:
            timeslots = Timeslot.get_timeslots_by_trainer_id(trainer_id)
            if timeslots:
                print()
                print(f"Timeslots for Trainer {trainer.first_name} {trainer.last_name}:")
                for timeslot in timeslots:
                    room = Room.get_all_rooms()[timeslot.room_id - 1]
                    print(f"Timeslot ID: {timeslot.timeslot_id}")
                    print(f"Booked: {timeslot.is_booked}")
                    print(f"Day: {timeslot.day}")
                    print(f"Time Frame: {timeslot.time_frame}")
                    print(f"Room: {room.room_name}")
                    print(f"Booking Fee: {timeslot.booking_fee}")
                    print("---")
                    print()
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
        else:
            print("Invalid Trainer ID.")
    else:
        print("No trainers found.")