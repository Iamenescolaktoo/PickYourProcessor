Delimiter //
START TRANSACTION;
SELECT @Username  := Username FROM Person;
SELECT @Budget := Budget FROM Person;

UPDATE Cart SET CPUName = (SELECT CPUName 
      FROM CPU 
      WHERE Cost< @Budget
      LIMIT 1);

UPDATE Cart SET GPUName = (SELECT GPUName 
      FROM GPU 
      WHERE Cost< @Budget
      LIMIT 1);

	SET @Budget = @Budget - (SELECT SUM(Cost) FROM Cart NATURAL JOIN CPU NATURAL JOIN GPU WHERE Username = @Username GROUP BY GPU.ProductName, CPU.ProductName);
	
	IF (@Budget < 0) THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF//
Delimiter ;
