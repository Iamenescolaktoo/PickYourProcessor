SELECT
  COALESCE(Cart.Title, 'Untitled Cart'),
  Permission.Scope,
  ROUND(COALESCE(GPU.Cost, 0) + COALESCE(CPU.Cost, 0), 2) AS Cost,
  Permission.CartId
FROM
  Permission
INNER JOIN
  Cart
  ON Permission.CartId = Cart.CartId
LEFT OUTER JOIN
  GPU
  ON Cart.GPUName = GPU.ProductName
LEFT OUTER JOIN
  CPU
  ON Cart.CPUName = CPU.ProductName
WHERE
  Permission.Username = %s
ORDER BY
  Cart.LastModified DESC;
