SELECT TerritoryID,ROUND(SUM(TotalDue),2) AS 'Total by Territory',RANK() OVER(ORDER BY SUM(TotalDue)DESC) AS Rank
FROM Sales.SalesOrderHeader
GROUP BY TerritoryID

SELECT SalesOrderID, ROW_NUMBER() OVER(ORDER BY ModifiedDate DESC) as row,ModifiedDate
FROM Sales.SalesOrderHeader


SELECT SalesOrderID, TotalDue, LAG(TotalDue,1) OVER(PARTITION BY TerritoryID ORDER BY SalesOrderID) AS 'Prior TotalDue',TerritoryID
FROM Sales.SalesOrderHeader
ORDER BY TerritoryID


SELECT SalesOrderID,TotalDue,FIRST_VALUE(TotalDue) OVER(ORDER BY SalesOrderID) AS 'First Value'
FROM Sales.SalesOrderHeader

WITH sales_table AS(SELECT SalesOrderID,TotalDue,LAST_VALUE(TotalDue) OVER(ORDER BY SalesOrderID RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING ) AS 'Last Value'
FROM Sales.SalesOrderHeader)

SELECT SalesOrderID, TotalDue,RANK() OVER(ORDER BY TotalDue DESC) AS ranking
FROM sales_table

SELECT SalesOrderID,TotalDue,ROW_NUMBER() OVER(ORDER BY TotalDue) AS ranking
FROM Sales.SalesOrderHeader

SELECT SalesOrderID, TerritoryID, AVG(TotalDue) OVER(PARTITION BY TerritoryID) AS average
FROM Sales.SalesOrderHeader
ORDER BY SalesOrderID;



WITH products_sold AS(SELECT ProductID,Name,(SELECT SUM(LineTotal) FROM Sales.SalesOrderDetail WHERE Production.Product.ProductID = SalesOrderDetail.ProductID) AS line_total
FROM Production.Product
WHERE ProductID IN (SELECT ProductID FROM Sales.SalesOrderDetail))

FROM products_sold


SELECT AVG(line_total)
FROM thirds
GROUP BY Third



SELECT SalesOrderID,TotalDue, AVG(TotalDue) OVER(ORDER BY SalesOrderID ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS '6 - ma'
FROM Sales.SalesOrderHeader

SELECT TerritoryID,TotalDue,SUM(TotalDue) OVER(PARTITION BY TerritoryID ORDER BY TerritoryID ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS 'sum'
FROM Sales.SalesOrderHeader

SELECT MAX(TotalDue)
FROM Sales.SalesOrderHeader
WHERE TerritoryID = 1

SELECT SalesOrderID,TotalDue, SUM(TotalDue) OVER(ORDER BY SalesOrderID ROWS BETWEEN 12 PRECEDING AND CURRENT ROW) AS 'moving total'
FROM Sales.SalesOrderHeader;



CREATE  EXTENSION IF NOT EXISTS tablefunc;
SELECT * FROM (
SELECT TerritoryID,SalesPersonID,SUM(TotalDue) as total
FROM Sales.SalesOrderHeader
WHERE SalesPersonID IN (276,279,282)
GROUP BY TerritoryID,SalesPersonID
)
AS ct (TerritoryID VARCHAR
"276" VARCHAR
"279" VARCHAR
"282" VARCHAR)


SELECT TerritoryID, SalesPersonID,SUM(TotalDue) AS total
FROM Sales.SalesOrderHeader
WHERE SalesPersonID IN (276.279,282)
GROUP BY ROLLUP(SalesPersonID,TerritoryID)

SELECT TerritoryID, ProductID,SUM(TotalDue) AS Total
FROM Sales.SalesOrderHeader H
INNER JOIN Sales.SalesOrderDetail D
ON H.SalesOrderID = D.SalesOrderID
WHERE ProductID IN (778,989,963) AND TerritoryID IN (1,2,3)
GROUP BY CUBE (TerritoryID,ProductID)
ORDER BY ProductID

WITH products AS(SELECT Name,SUM(LineTotal) as Total,Color
FROM Production.Product P
RIGHT JOIN Sales.SalesOrderDetail D
ON P.ProductID = D.ProductID
GROUP BY Name,Color),

ranking AS(SELECT Name,RANK()OVER(Order By Total) AS rank
FROM products)

SELECT STRING_AGG(Name, ",")
FROM ranking
WHERE rank <=5


WITH Products AS(SELECT Name FROM Production.Product)

SELECT STRING_AGG(Name,',') FROM Products


SELECT STRING_AGG(Name,' , ') AS country
FROM Sales.SalesTerritory


SELECT TerritoryID, SalesPersonID,SUM(TotalDue) AS total
FROM Sales.SalesOrderHeader
WHERE SalesPersonID IN (276.279,282)
GROUP BY ROLLUP(SalesPersonID,TerritoryID)


SELECT COALESCE(CAST(TerritoryID AS VARCHAR),'All territories'), COALESCE(CAST(ProductID AS VARCHAR),'All Products'),SUM(TotalDue) AS Total
FROM Sales.SalesOrderHeader H
INNER JOIN Sales.SalesOrderDetail D
ON H.SalesOrderID = D.SalesOrderID
WHERE ProductID IN (778,989,963) AND TerritoryID IN (1,2,3)
GROUP BY ROLLUP (TerritoryID,ProductID)
ORDER BY ProductID

SELECT SalesOrderID,TotalDue, SUM(TotalDue) OVER(ORDER BY SalesOrderID ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS 'Moving average'
FROM Sales.SalesOrderHeader
