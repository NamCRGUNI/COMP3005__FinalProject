from database import execute_query, fetch_data

class User:
    def __init__(self, user_type, user_id, first_name, last_name, age, weight, height, gender, username, password, email):
        self.user_type = user_type
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}"

    @staticmethod
    def create_user(user_type, first_name, last_name, age, weight, height, gender, username, password, email):
        query = "INSERT INTO Users (UserType, FirstName, LastName, Age, Weight, Height, Gender, Username, Password, Email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING UserID"
        params = (user_type, first_name, last_name, age, weight, height, gender, username, password, email)
        user_id = execute_query(query, params)
        return User(user_type, user_id, first_name, last_name, age, weight, height, gender, username, password, email)

    @staticmethod
    def get_user_by_id(user_id):
        query = "SELECT UserType, UserID, FirstName, LastName, Age, Weight, Height, Gender, Username, Password, Email FROM Users WHERE UserID = %s"
        params = (user_id,)
        result = fetch_data(query, params)
        if result:
            user_data = result[0]
            return User(*user_data)
        return None

    @staticmethod
    def get_user_by_username(username):
        query = "SELECT UserType, UserID, FirstName, LastName, Age, Weight, Height, Gender, Username, Password, Email FROM Users WHERE Username = %s"
        params = (username,)
        result = fetch_data(query, params)
        if result:
            user_data = result[0]
            return User(*user_data)
        return None
    
    @staticmethod
    def get_all_trainers():
        query = "SELECT UserType, UserID, FirstName, LastName, Age, Weight, Height, Gender, Username, Password, Email FROM Users WHERE UserType = 'Trainer'"
        results = fetch_data(query)
        trainers = []
        for result in results:
            trainer = User(*result)
            trainers.append(trainer)
        return trainers
    @staticmethod
    def get_users_by_name(first_name, last_name):
        query = "SELECT UserType, UserID, FirstName, LastName, Age, Weight, Height, Gender, Username, Password, Email FROM Users WHERE FirstName = %s AND LastName = %s"
        params = (first_name, last_name)
        results = fetch_data(query, params)
        users = []
        for result in results:
            user = User(*result)
            users.append(user)
        return users

class FitnessGoal:
    def __init__(self, goal_id, user_id, goal_name, goal_status, goal_description, start_date, end_date):
        self.goal_id = goal_id
        self.user_id = user_id
        self.goal_name = goal_name
        self.goal_status = goal_status
        self.goal_description = goal_description
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"Fitness Goal: {self.goal_name}"

    @staticmethod
    def create_fitness_goal(user_id, goal_name, goal_status, goal_description, start_date, end_date):
        query = "INSERT INTO FitnessGoals (UserID, GoalName, GoalStatus, GoalDescription, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s, %s) RETURNING GoalID"
        params = (user_id, goal_name, goal_status, goal_description, start_date, end_date)
        goal_id = execute_query(query, params)
        return FitnessGoal(goal_id, user_id, goal_name, goal_status, goal_description, start_date, end_date)

    @staticmethod
    def get_fitness_goals_by_user_id(user_id):
        query = "SELECT GoalID, UserID, GoalName, GoalStatus, GoalDescription, StartDate, EndDate FROM FitnessGoals WHERE UserID = %s"
        params = (user_id,)
        results = fetch_data(query, params)
        fitness_goals = []
        for result in results:
            fitness_goal = FitnessGoal(*result)
            fitness_goals.append(fitness_goal)
        return fitness_goals

    def update_goal_name(self, new_name):
        query = "UPDATE FitnessGoals SET GoalName = %s WHERE GoalID = %s"
        params = (new_name, self.goal_id)
        execute_query(query, params)

    def update_goal_status(self, new_status):
        query = "UPDATE FitnessGoals SET GoalStatus = %s WHERE GoalID = %s"
        params = (new_status, self.goal_id)
        execute_query(query, params)

    def update_goal_description(self, new_description):
        query = "UPDATE FitnessGoals SET GoalDescription = %s WHERE GoalID = %s"
        params = (new_description, self.goal_id)
        execute_query(query, params)

    def update_start_date(self, new_start_date):
        query = "UPDATE FitnessGoals SET StartDate = %s WHERE GoalID = %s"
        params = (new_start_date, self.goal_id)
        execute_query(query, params)

    def update_end_date(self, new_end_date):
        query = "UPDATE FitnessGoals SET EndDate = %s WHERE GoalID = %s"
        params = (new_end_date, self.goal_id)
        execute_query(query, params)

class ExerciseRoutine:
    def __init__(self, routine_id, routine_name, routine_description, routine_type):
        self.routine_id = routine_id
        self.routine_name = routine_name
        self.routine_description = routine_description
        self.routine_type = routine_type

    def __str__(self):
        return f"Exercise Routine: {self.routine_name}"

    @staticmethod
    def get_all_routines():
        query = "SELECT RoutineID, RoutineName, RoutineDescription, RoutineType FROM ExerciseRoutines"
        results = fetch_data(query)
        routines = []
        for result in results:
            routine = ExerciseRoutine(*result)
            routines.append(routine)
        return routines

    @staticmethod
    def create_exercise_routine(routine_name, routine_description, routine_type):
        query = "INSERT INTO ExerciseRoutines (RoutineName, RoutineDescription, RoutineType) VALUES (%s, %s, %s) RETURNING RoutineID"
        params = (routine_name, routine_description, routine_type)
        routine_id = execute_query(query, params)
        return ExerciseRoutine(routine_id, routine_name, routine_description, routine_type)
    
class Room:
    def __init__(self, room_id, room_name, capacity):
        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity

    def __str__(self):
        return f"Room: {self.room_name}"

    @staticmethod
    def get_all_rooms():
        query = "SELECT RoomID, RoomName, Capacity FROM Rooms"
        results = fetch_data(query)
        rooms = []
        for result in results:
            room = Room(*result)
            rooms.append(room)
        return rooms
    
    @staticmethod
    def create_room(room_name, capacity):
        query = "INSERT INTO Rooms (RoomName, Capacity) VALUES (%s, %s) RETURNING RoomID"
        params = (room_name, capacity)
        room_id = execute_query(query, params)
        return Room(room_id, room_name, capacity)

class EquipmentType:
    def __init__(self, equipment_type_id, equipment_name):
        self.equipment_type_id = equipment_type_id
        self.equipment_name = equipment_name

    def __str__(self):
        return f"Equipment Type: {self.equipment_name}"

    @staticmethod
    def get_all_equipment_types():
        query = "SELECT EquipmentTypeID, EquipmentName FROM EquipmentTypes"
        results = fetch_data(query)
        equipment_types = []
        for result in results:
            equipment_type = EquipmentType(*result)
            equipment_types.append(equipment_type)
        return equipment_types

    @staticmethod
    def create_equipment_type(equipment_name):
        query = "INSERT INTO EquipmentTypes (EquipmentName) VALUES (%s) RETURNING EquipmentTypeID"
        params = (equipment_name,)
        equipment_type_id = execute_query(query, params)
        return EquipmentType(equipment_type_id, equipment_name)

class Equipment:
    def __init__(self, equipment_id, equipment_type_id, equipment_status):
        self.equipment_id = equipment_id
        self.equipment_type_id = equipment_type_id
        self.equipment_status = equipment_status

    def __str__(self):
        return f"Equipment ID: {self.equipment_id}"

    @staticmethod
    def get_all_equipment():
        query = "SELECT EquipmentID, EquipmentTypeID, EquipmentStatus FROM Equipment"
        results = fetch_data(query)
        equipment_list = []
        for result in results:
            equipment = Equipment(*result)
            equipment_list.append(equipment)
        return equipment_list

    @staticmethod
    def update_equipment_status(equipment_id, equipment_status):
        query = "UPDATE Equipment SET EquipmentStatus = %s WHERE EquipmentID = %s"
        params = (equipment_status, equipment_id)
        execute_query(query, params)
    
    @staticmethod
    def create_equipment(equipment_type_id, equipment_status):
        query = "INSERT INTO Equipment (EquipmentTypeID, EquipmentStatus) VALUES (%s, %s) RETURNING EquipmentID"
        params = (equipment_type_id, equipment_status)
        equipment_id = execute_query(query, params)
        return Equipment(equipment_id, equipment_type_id, equipment_status)    

class TrainerAvailability:
    def __init__(self, availability_id, user_id, time_frame, day):
        self.availability_id = availability_id
        self.user_id = user_id
        self.time_frame = time_frame
        self.day = day

    def __str__(self):
        return f"Trainer Availability: {self.day} - {self.time_frame}"

    @staticmethod
    def get_trainer_availability_by_user_id(user_id):
        query = "SELECT AvailabilityID, UserID, TimeFrame, Day FROM TrainerAvailability WHERE UserID = %s"
        params = (user_id,)
        results = fetch_data(query, params)
        availability_list = []
        for result in results:
            availability = TrainerAvailability(*result)
            availability_list.append(availability)
        return availability_list

class Timeslot:
    def __init__(self, timeslot_id, booking_fee, room_id, trainer_id, time_frame, day, is_booked):
        self.timeslot_id = timeslot_id
        self.booking_fee = booking_fee
        self.room_id = room_id
        self.trainer_id = trainer_id
        self.time_frame = time_frame
        self.day = day
        self.is_booked = is_booked

    def __str__(self):
        return f"Timeslot: {self.day} - {self.time_frame} (Booked: {self.is_booked})"

    @staticmethod
    def create_timeslot(booking_fee, room_id, trainer_id, time_frame, day):
        query = "INSERT INTO Timeslots (BookingFee, RoomID, TrainerID, TimeFrame, Day, IsBooked) VALUES (%s, %s, %s, %s, %s, FALSE) RETURNING TimeslotID"
        params = (booking_fee, room_id, trainer_id, time_frame, day)
        timeslot_id = execute_query(query, params)
        return Timeslot(timeslot_id, booking_fee, room_id, trainer_id, time_frame, day, False)

    @staticmethod
    def get_timeslots_by_trainer_id(trainer_id):
        query = "SELECT TimeslotID, BookingFee, RoomID, TrainerID, TimeFrame, Day, IsBooked FROM Timeslots WHERE TrainerID = %s"
        params = (trainer_id,)
        results = fetch_data(query, params)
        timeslots = []
        for result in results:
            timeslot = Timeslot(*result)
            timeslots.append(timeslot)
        return timeslots

    @staticmethod
    def get_available_timeslots():
        query = "SELECT TimeslotID, BookingFee, RoomID, TrainerID, TimeFrame, Day, IsBooked FROM Timeslots WHERE IsBooked = FALSE"
        results = fetch_data(query)
        available_timeslots = []
        for result in results:
            timeslot = Timeslot(*result)
            available_timeslots.append(timeslot)
        return available_timeslots

    @staticmethod
    def book_timeslot(timeslot_id):
        query = "UPDATE Timeslots SET IsBooked = TRUE WHERE TimeslotID = %s"
        params = (timeslot_id,)
        execute_query(query, params)
    
    @staticmethod
    def get_booked_timeslots_by_room_id(room_id):
        query = "SELECT * FROM Timeslots WHERE RoomID = %s AND IsBooked = TRUE"
        params = (room_id,)
        results = fetch_data(query, params)
        booked_timeslots = []
        for result in results:
            timeslot = Timeslot(*result)
            booked_timeslots.append(timeslot)
        return booked_timeslots


class Payment:
    def __init__(self, payment_id, user_id, booking_fee, payment_status, bill_description, date_issued, created_at):
        self.payment_id = payment_id
        self.user_id = user_id
        self.booking_fee = booking_fee
        self.payment_status = payment_status
        self.bill_description = bill_description
        self.date_issued = date_issued
        self.created_at = created_at

    def __str__(self):
        return f"Payment ID: {self.payment_id}"

    @staticmethod
    def create_payment(user_id, booking_fee, payment_status, bill_description, date_issued):
        query = "INSERT INTO Payments (UserID, BookingFee, PaymentStatus, BillDescription, DateIssued) VALUES (%s, %s, %s, %s, %s) RETURNING PaymentID"
        params = (user_id, booking_fee, payment_status, bill_description, date_issued)
        payment_id = execute_query(query, params)
        return Payment(payment_id, user_id, booking_fee, payment_status, bill_description, date_issued, None)

    @staticmethod
    def get_payments_by_user_id(user_id):
        query = "SELECT PaymentID, UserID, BookingFee, PaymentStatus, BillDescription, DateIssued, CreatedAt FROM Payments WHERE UserID = %s"
        params = (user_id,)
        results = fetch_data(query, params)
        payments = []
        for result in results:
            payment = Payment(*result)
            payments.append(payment)
        return payments
    
    @staticmethod
    def get_all_payments():
        query = "SELECT PaymentID, UserID, BookingFee, PaymentStatus, BillDescription, DateIssued, CreatedAt FROM Payments"
        results = fetch_data(query)
        payments = []
        for result in results:
            payment = Payment(*result)
            payments.append(payment)
        return payments
    
    @staticmethod
    def update_payment_status(payment_id, new_status):
        query = "UPDATE Payments SET PaymentStatus = %s WHERE PaymentID = %s"
        params = (new_status, payment_id)
        execute_query(query, params)