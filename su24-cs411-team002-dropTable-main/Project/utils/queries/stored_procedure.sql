delimiter $$
create procedure UpdateTrending()
begin
	drop table if exists TrendingCPUs;
	drop table if exists TrendingGPUs;
	
	CREATE TABLE TrendingCPUs 
	AS
	(SELECT  
Brand, ProductName, count(CartId) AS CartCount
FROM
	Cart JOIN CPU ON CPU.ProductName = Carts.CPUName
	GROUP BY
		ProductName
	ORDER BY
		CartCount DESC
	LIMIT
		10);

CREATE TABLE TrendingGPUs 
	AS
	(SELECT  
Brand, ProductName, count(CartId) AS CartCount
FROM
	Cart JOIN GPU ON GPU.ProductName = Carts.GPUName
	GROUP BY
		ProductName
	ORDER BY
		CartCount DESC
	LIMIT
		10);

end;$$
delimiter ;
