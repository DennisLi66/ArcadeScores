drop database if exists arcadeScoresDB;
create database arcadeScoresDB;
use arcadeScoresDB;

create table users (
	userID int primary key auto_increment,
    username varchar(50),
    email varchar(255) NOT NULL UNIQUE,
    salt varchar(255) NOT NULL,
    passcode varchar(255)
);
create table times (
	timeScoreID int primary key auto_increment,
	userID int,
    gameID int,
    timeInMilliseconds int,
    submissionTime datetime
);
create table scores (
	scoreID int primary key auto_increment,
    userID int,
    gameID int,
    score int,
    submissionTime datetime
);
create table sessions(
	sessionID varchar(255) NOT NULL,
    userID int NOT NULL,
	sessionDate datetime NOT NULL,
    timeduration varchar(255) -- 1 HOUR or PERMANENT
);
create table forgottenPasswordCodes(
	email varchar(255) NOT NULL UNIQUE,
    fcode varchar(10) NOT NULL
);