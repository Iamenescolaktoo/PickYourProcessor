SELECT
  COALESCE(Cart.Title, 'Untitled Cart'),
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
  AND (
  Permission.Scope = 'Write'
  OR Permission.Scope = 'Manage'
  )
ORDER BY
  Cart.LastModified DESC;
