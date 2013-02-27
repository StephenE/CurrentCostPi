-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 02, 2013 at 02:39 PM
-- Server version: 5.5.28
-- PHP Version: 5.4.4-12

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- User: `PowerMeter`
--

GRANT USAGE ON *.* TO 'PowerMeter'@'localhost' IDENTIFIED BY PASSWORD {password};

GRANT EXECUTE ON `PowerMeter`.* TO 'PowerMeter'@'localhost';

--
-- Database: `PowerMeter`
--
CREATE DATABASE `PowerMeter` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `PowerMeter`;

DELIMITER $$
--
-- Procedures
--
CREATE PROCEDURE `StoreMeterReading`(
    IN recordedAt DATETIME,
    IN temperature DECIMAL(5,1),
    IN watts INT
)
BEGIN
    INSERT INTO LiveData
        (TakenAt, Temperature, MeterReading)
        VALUES (recordedAt, temperature, watts);
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `LiveData`
--

CREATE TABLE IF NOT EXISTS `LiveData` (
  `TakenAt` datetime NOT NULL,
  `Temperature` decimal(5,1) NOT NULL,
  `MeterReading` int(10) unsigned NOT NULL,
  PRIMARY KEY (`TakenAt`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
