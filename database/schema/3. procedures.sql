USE `marites`;

-- Create stored procedure to generate payments
DROP PROCEDURE IF EXISTS `GenerateMonthlyPayments`;
DELIMITER //
CREATE PROCEDURE `GenerateMonthlyPayments`()
BEGIN
    DECLARE `lastDayOfMonth` DATE;
    SET `lastDayOfMonth` = LAST_DAY(CURDATE());

    INSERT INTO `payments` (`leaseId`, `paymentAmount`, `paymentDate`)
		SELECT `leaseId`, `monthlyRentAmount`, `lastDayOfMonth`
		FROM `leases`
        WHERE CURDATE() BETWEEN `leaseStart` AND `leaseEnd`;
END //
DELIMITER ;