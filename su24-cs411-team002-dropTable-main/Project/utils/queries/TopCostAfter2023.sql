SELECT p.ProductName, p.Brand, p.Cost, p.ReleaseYear
FROM (
    SELECT ProductName, Brand, Cost, ReleaseYear
    FROM CPU
    UNION
    SELECT ProductName, Brand, Cost, ReleaseYear
    FROM GPU
) AS p
WHERE
	p.ReleaseYear >= 2023
ORDER BY p.Cost DESC
LIMIT 15;
