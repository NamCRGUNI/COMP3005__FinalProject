-- Create the tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO usr1;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO usr1;

CREATE TABLE Users (
    UserType VARCHAR(20) NOT NULL CHECK (UserType IN ('Member', 'Trainer', 'Admin')),
    UserID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Age INT,
    Weight DECIMAL(5, 2),
    Height DECIMAL(5, 2),
    Gender VARCHAR(10),
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE FitnessGoals (
    GoalID SERIAL PRIMARY KEY,
    UserID INT NOT NULL REFERENCES Users(UserID),
    GoalName VARCHAR(100) NOT NULL,
    GoalStatus VARCHAR(20) NOT NULL CHECK (GoalStatus IN ('Active', 'Completed', 'Not Started')),
    GoalDescription TEXT,
    StartDate DATE,
    EndDate DATE
);

CREATE TABLE ExerciseRoutines (
    RoutineID SERIAL PRIMARY KEY,
    RoutineName VARCHAR(50) NOT NULL,
    RoutineDescription TEXT,
    RoutineType VARCHAR(20) NOT NULL CHECK (RoutineType IN ('Upper Body', 'Lower Body', 'Core', 'Cardio'))
);

CREATE TABLE Rooms (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(50) NOT NULL,
    Capacity INT NOT NULL
);

CREATE TABLE EquipmentTypes (
    EquipmentTypeID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(50) NOT NULL
);

CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentTypeID INT NOT NULL REFERENCES EquipmentTypes(EquipmentTypeID),
    EquipmentStatus VARCHAR(20) NOT NULL CHECK (EquipmentStatus IN ('Good', 'Broken'))
);

CREATE TABLE TrainerAvailability (
    AvailabilityID SERIAL PRIMARY KEY,
    UserID INT NOT NULL REFERENCES Users(UserID),
    TimeFrame VARCHAR(20) NOT NULL CHECK (TimeFrame IN ('Morning', 'Afternoon')),
    Day VARCHAR(10) NOT NULL
);

CREATE TABLE Timeslots (
    TimeslotID SERIAL PRIMARY KEY,
    BookingFee DECIMAL(10, 2) NOT NULL,
    RoomID INT NOT NULL REFERENCES Rooms(RoomID),
    TrainerID INT NOT NULL REFERENCES Users(UserID),
    TimeFrame VARCHAR(20) NOT NULL CHECK (TimeFrame IN ('Morning', 'Afternoon')),
    Day VARCHAR(10) NOT NULL,
    IsBooked BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Payments (
    PaymentID SERIAL PRIMARY KEY,
    UserID INT NOT NULL REFERENCES Users(UserID),
    BookingFee DECIMAL(10, 2) NOT NULL,
    PaymentStatus VARCHAR(1) NOT NULL CHECK (PaymentStatus IN ('Y', 'N')),
    BillDescription TEXT,
    DateIssued DATE NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);