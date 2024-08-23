delimiter $$
CREATE TRIGGER 
IntegrateCPUManufacturer
BEFORE INSERT ON CPU
FOR EACH ROW
BEGIN
SET @brand = (SELECT BrandName FROM Manufacturer WHERE BrandName = new.Brand);
IF @brand IS NULL 
THEN 
INSERT INTO Manufacturer(BrandName, CountryCode, YearEstablished) VALUES (new.Brand, null, null); 
END IF;
END;$$
delimiter ;
