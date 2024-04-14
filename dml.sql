-- Insert test data for Users
INSERT INTO Users (UserType, FirstName, LastName, Age, Weight, Height, Gender, Username, Password, Email)
VALUES
    ('Member', 'John', 'Doe', 32, 75.5, 178.0, 'Male', 'johndoe', 'password123', 'john.doe@example.com'),
    ('Member', 'Jane', 'Smith', 28, 60.0, 165.0, 'Female', 'janesmith', 'password456', 'jane.smith@example.com'),
    ('Trainer', 'Michael', 'Johnson', 40, 80.0, 182.0, 'Male', 'mjohnson', 'trainer123', 'michael.johnson@example.com'),
    ('Trainer', 'Emily', 'Davis', 35, 65.0, 170.0, 'Female', 'emilydavis', 'trainer456', 'emily.davis@example.com'),
    ('Admin', 'Robert', 'Wilson', 45, 85.0, 180.0, 'Male', 'rwilson', 'admin123', 'robert.wilson@example.com');

-- Insert test data for FitnessGoals
INSERT INTO FitnessGoals (UserID, GoalName, GoalStatus, GoalDescription, StartDate, EndDate)
VALUES
    (1, 'Weight Loss', 'Active', 'Lose 10 kg in 3 months', '2023-05-01', '2023-07-31'),
    (2, 'Build Muscle', 'Not Started', 'Gain 5 kg of muscle mass in 6 months', '2023-06-01', '2023-11-30'),
    (1, 'Improve Endurance', 'Completed', 'Run a half marathon', '2022-09-01', '2023-03-31');

-- Insert test data for ExerciseRoutines
INSERT INTO ExerciseRoutines (RoutineName, RoutineDescription, RoutineType)
VALUES
    ('Chest and Triceps Workout', 'A routine for building upper body strength', 'Upper Body'),
    ('Leg Day', 'A routine for building lower body strength', 'Lower Body'),
    ('Core Blast', 'A routine for strengthening the core muscles', 'Core'),
    ('HIIT Cardio', 'A high-intensity interval training routine for cardio', 'Cardio');

-- Insert test data for Rooms
INSERT INTO Rooms (RoomName, Capacity)
VALUES
    ('Studio A', 20),
    ('Studio B', 15),
    ('Spin Room', 25);

-- Insert test data for EquipmentTypes
INSERT INTO EquipmentTypes (EquipmentName)
VALUES
    ('Treadmill'),
    ('Dumbbells'),
    ('Yoga Mats');

-- Insert test data for Equipment
INSERT INTO Equipment (EquipmentTypeID, EquipmentStatus)
VALUES
    (1, 'Good'),
    (1, 'Broken'),
    (2, 'Good'),
    (3, 'Good');

-- Insert test data for TrainerAvailability
INSERT INTO TrainerAvailability (UserID, TimeFrame, Day)
VALUES
    (3, 'Morning', 'Monday'),
    (3, 'Afternoon', 'Wednesday'),
    (3, 'Afternoon', 'Saturday'),
    (4, 'Morning', 'Tuesday'),
    (4, 'Morning', 'Thursday'),
    (4, 'Afternoon', 'Friday');

-- Insert test data for Timeslots
INSERT INTO Timeslots (BookingFee, RoomID, TrainerID, TimeFrame, Day, IsBooked)
VALUES
    (25.00, 1, 3, 'Morning', 'Monday', TRUE),
    (30.00, 2, 3, 'Afternoon', 'Wednesday', TRUE),
    (35.00, 3, 4, 'Morning', 'Tuesday', FALSE),
    (40.00, 1, 4, 'Afternoon', 'Friday', FALSE);

-- Insert test data for Payments
INSERT INTO Payments (UserID, BookingFee, PaymentStatus, BillDescription, DateIssued)
VALUES
    (1, 25.00, 'Y', 'Personal Training Session', '2023-05-15'),
    (2, 30.00, 'N', 'Group Fitness Class', '2023-05-20'),
    (1, 35.00, 'Y', 'Personal Training Session', '2023-06-01');