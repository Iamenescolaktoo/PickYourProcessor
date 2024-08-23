(SELECT
	Person.Username
FROM
	Person
INNER JOIN
	Permission
	ON Person.Username = Permission.Username
INNER JOIN
	Cart
	ON Permission.CartId = Cart.CartId
INNER JOIN
	CPU
	ON Cart.CPUName = CPU.ProductName
INNER JOIN
	Manufacturer
	ON CPU.Brand = Manufacturer.BrandName
WHERE
	Manufacturer.CountryCode = 'US'
	AND Permission.Scope = 'manage'
LIMIT 15
) UNION (
SELECT
	Person.Username
FROM
	Person
INNER JOIN
	Permission
	ON Person.Username = Permission.Username
INNER JOIN
	Cart
	ON Permission.CartId = Cart.CartId
INNER JOIN
	GPU
	ON Cart.GPUName = GPU.ProductName
INNER JOIN
	Manufacturer
	ON GPU.Brand = Manufacturer.BrandName
WHERE
	Manufacturer.CountryCode = 'US'
	AND Permission.Scope = 'manage'
LIMIT 15
);
