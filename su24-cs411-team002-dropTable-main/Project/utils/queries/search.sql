SELECT
  GPU.Brand AS Brand,
  GPU.ProductName AS Name,
  ROUND(GPU.Cost, 2) AS Cost
FROM
  GPU
WHERE
  GPU.Brand REGEXP %s
  OR GPU.ProductName REGEXP %s
UNION
SELECT
  CPU.Brand AS Brand,
  CPU.ProductName AS Name,
  ROUND(CPU.Cost, 2) AS Cost
FROM
  CPU
WHERE
  CPU.Brand REGEXP %s
  OR CPU.ProductName REGEXP %s;
