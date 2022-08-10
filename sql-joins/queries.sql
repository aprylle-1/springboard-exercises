-- write your queries here

SELECT * FROM owners o 
LEFT JOIN vehicles v 
ON o.id = v.owner_id;

SELECT o.first_name, o.last_name, count(*) as count FROM owners o 
JOIN vehicles v 
ON o.id = v.owner_id 
GROUP BY o.id ORDER BY count, o.first_name ASC;

SELECT o.first_name, o.last_name, ROUND(AVG(price)) AS average_price, COUNT(*) as count
FROM owners o
JOIN vehicles v 
ON o.id = v.owner_id
GROUP BY o.id
HAVING ROUND(AVG(price)) > 10000 AND COUNT(*) > 1
ORDER BY o.first_name DESC;