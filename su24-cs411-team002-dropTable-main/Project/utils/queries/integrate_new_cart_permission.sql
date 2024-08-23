CREATE TRIGGER `AddNewCartPermissions` AFTER INSERT ON `Cart` FOR EACH ROW BEGIN
  SET @new_permission = (
    SELECT
      Permission.`Scope`
    FROM
      Permission
    WHERE
      Permission.CartId = NEW.CartId
      AND Permission.Username = NEW.Creator
  );

  IF @new_permission IS NULL THEN
    INSERT INTO
      Permission
    VALUES
      (@new_cart_id, @new_cart_creator, 'Manage', NOW());
  END IF;
END
