USE `marites`;

DROP EVENT IF EXISTS `GeneratePayments`;
CREATE EVENT IF NOT EXISTS `GeneratePayments`
ON SCHEDULE EVERY 1 MONTH
STARTS '2024-05-01 00:00:00'
DO 
	CALL `GenerateMonthlyPayments`;

SET GLOBAL event_scheduler = ON;