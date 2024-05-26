USE `marites`;

-- Trigger to increment tenant count on insert
DROP TRIGGER IF EXISTS `increment_room_tenantCount_beforeInsert`;
CREATE TRIGGER `increment_room_tenantCount_beforeInsert` 
BEFORE INSERT ON `tenants`
FOR EACH ROW 
    UPDATE `rooms` 
    SET `tenantCount` = `tenantCount` + 1
    WHERE `rooms`.`roomNumber` = NEW.`roomNumber`;

-- Trigger to update tenant count on update
DROP TRIGGER IF EXISTS `update_room_tenantCount_beforeUpdate`;
DELIMITER //
CREATE TRIGGER `update_room_tenantCount_beforeUpdate` 
BEFORE UPDATE ON `tenants`
FOR EACH ROW
BEGIN
    IF NEW.`roomNumber` <> OLD.`roomNumber` THEN
        UPDATE `rooms` 
        SET `tenantCount` = `tenantCount` + 1
        WHERE `rooms`.`roomNumber` = NEW.`roomNumber`;
        UPDATE `rooms` 
        SET `tenantCount` = `tenantCount` - 1
        WHERE `rooms`.`roomNumber` = OLD.`roomNumber`;
    END IF;
END; //
DELIMITER ;

-- Trigger to decrement tenant count on delete
DROP TRIGGER IF EXISTS `decrement_room_tenantCount_afterDelete`;
CREATE TRIGGER `decrement_room_tenantCount_onDelete` 
AFTER DELETE ON `tenants`
FOR EACH ROW
    UPDATE `rooms` 
    SET `tenantCount` = `tenantCount` - 1
    WHERE `rooms`.`roomNumber` = OLD.`roomNumber`;

-- Trigger to set paymentAmount in payments table
DROP TRIGGER IF EXISTS `setpaymentAmount_beforeInsert`;
DELIMITER //
CREATE TRIGGER `setpaymentAmount_beforeInsert`
BEFORE INSERT ON `payments`
FOR EACH ROW
BEGIN
    DECLARE `rentAmount` DECIMAL(10, 2);

    -- Fetch the monthlyRentAmount from the leases table
    SELECT `monthlyRentAmount` INTO `rentAmount`
    FROM `leases`
    WHERE `leaseId` = NEW.`leaseId`;

    -- Set the payAmount to the fetched monthlyRentAmount
    SET NEW.`paymentAmount` = `rentAmount`;
END; //
DELIMITER ;

-- Trigger to automatically set tenant names to uppercase
DROP TRIGGER IF EXISTS `tenantNames_toUpperCase_afterInsert`;
CREATE TRIGGER `tenantNames_toUpperCase_afterInsert`
AFTER INSERT ON `tenants`
FOR EACH ROW
	UPDATE `tenants`
    SET `lastName` = UPPER(NEW.`lastName`),
        `firstName` = UPPER(NEW.`firstName`),
        `middleName` = UPPER(NEW.`middleName`)
    WHERE `tenantId` = NEW.`tenantId`;