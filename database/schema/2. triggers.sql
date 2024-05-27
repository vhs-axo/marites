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