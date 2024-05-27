-- Drop and create the database
DROP DATABASE IF EXISTS `marites`;
CREATE DATABASE `marites`;

USE `marites`;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS `rooms`;
DROP TABLE IF EXISTS `tenants`;
DROP TABLE IF EXISTS `leases`;
DROP TABLE IF EXISTS `payments`;

-- Create rooms table
CREATE TABLE `rooms` (
    `roomNumber` INT UNSIGNED NOT NULL,
    `maxCapacity` INT UNSIGNED NOT NULL,
    `tenantCount` INT UNSIGNED NOT NULL DEFAULT 0,
    
    PRIMARY KEY (`roomNumber`),
    CONSTRAINT `chk_tenantCount` CHECK (`tenantCount` <= `maxCapacity`)
);

-- Create tenants table
CREATE TABLE `tenants` (
    `tenantId` INT UNSIGNED AUTO_INCREMENT,
    `lastName` VARCHAR(255) NOT NULL,
    `firstName` VARCHAR(255) NOT NULL,
    `middleName` VARCHAR(127) NOT NULL DEFAULT '',
    `birthDate` DATE NOT NULL,
    `contactNumber` CHAR(11) NOT NULL,
    `roomNumber` INT UNSIGNED NOT NULL,
    
    PRIMARY KEY (`tenantId`),
    CONSTRAINT `fk_tenants_rooms_roomNumber`
        FOREIGN KEY (`roomNumber`)
        REFERENCES `rooms` (`roomNumber`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT `chk_contactNumber` 
		CHECK (REGEXP_LIKE(`contactNumber`, _utf8mb4'^09[0-9]{9}$')),
    INDEX (`roomNumber`),
    INDEX (`lastName`, `firstName`)
);

-- Create leases table
CREATE TABLE `leases` (
    `leaseId` INT UNSIGNED AUTO_INCREMENT,
    `leaserId` INT UNSIGNED NOT NULL,
    `roomNumber` INT UNSIGNED NOT NULL,
    `leaseStart` DATE NOT NULL,
    `leaseEnd` DATE NOT NULL,
    `depositAmount` DECIMAL(10, 2) NOT NULL,
    `monthlyRentAmount` DECIMAL(10, 2) NOT NULL,
    
    PRIMARY KEY (`leaseId`),
    CONSTRAINT `fk_leases_tenants_leaserId`
        FOREIGN KEY (`leaserId`)
        REFERENCES `tenants` (`tenantId`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT `fk_leases_rooms_roomNumber`
        FOREIGN KEY (`roomNumber`)
        REFERENCES `rooms` (`roomNumber`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT `leases_chk_leaseEnd` 
		CHECK (`leaseStart` < `leaseEnd`),
	CONSTRAINT `uq_leaserId`
		UNIQUE (`leaserId`),
	CONSTRAINT `uq_roomNumber`
		UNIQUE (`roomNumber`),
    INDEX (`leaserId`),
    INDEX (`roomNumber`)
);

-- Create payments table
CREATE TABLE `payments` (
    `paymentId` INT UNSIGNED AUTO_INCREMENT,
    `leaseId` INT UNSIGNED NOT NULL,
    `paymentAmount` DECIMAL(10, 2) NOT NULL,
    `paymentDate` DATE NOT NULL,
    `paid` BOOLEAN NOT NULL,
    
    PRIMARY KEY (`paymentId`),
    CONSTRAINT `fk_payments_leases_leaseId`
        FOREIGN KEY (`leaseId`)
        REFERENCES `leases` (`leaseId`)
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `uq_paymentDate_leaseId`
		UNIQUE (`leaseId`, `paymentDate`),
    INDEX (`leaseId`)
);