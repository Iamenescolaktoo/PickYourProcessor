SELECT
	Manufacturer.BrandName
FROM
	Manufacturer
INNER JOIN
	CPU
	ON Manufacturer.BrandName = CPU.Brand
INNER JOIN
	GPU
	ON Manufacturer.BrandName = GPU.Brand
WHERE
	CPU.Cost > (
    	SELECT
        	AVG(c.Cost)
    	FROM
        	CPU AS c
	)
	OR GPU.Cost > (
    	SELECT
        	AVG(g.Cost)
    	FROM
        	GPU AS g
	)
GROUP BY
	Manufacturer.BrandName
ORDER BY
	Manufacturer.YearEstablished DESC
LIMIT 15;
