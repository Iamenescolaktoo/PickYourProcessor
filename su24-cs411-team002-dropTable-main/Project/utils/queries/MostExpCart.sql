SELECT 
    c.Creator,
    SUM(g.Cost + cp.Cost) AS TotalCartCost
FROM 
    Cart AS c
INNER JOIN 
    GPU g ON c.GPUName = g.ProductName
INNER JOIN 
    CPU cp ON c.CPUName = cp.ProductName
GROUP BY 
    c.Creator
ORDER BY 
    TotalCartCost DESC
LIMIT 15;
