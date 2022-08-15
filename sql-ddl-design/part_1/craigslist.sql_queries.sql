----Select all users and their respective preferred region, order by user

SELECT concat (u.first_name, ' ', u.last_name), r.region
FROM user_region ur
JOIN users u
ON ur.user_id = u.id
JOIN regions r
ON ur.region_id = r.id
ORDER BY u.first_name;

------Select the User Name, Region - Location of all POSTS------

SELECT concat (u.first_name, ' ', u.last_name) as user,
concat (r.region, ' - ', p.post_location) as region_location
FROM posts p
JOIN user_region ur
ON p.user_region_id = ur.id
JOIN users u
ON ur.user_id = u.id
JOIN regions r
ON ur.region_id = r.id
ORDER BY u.first_name ASC;

---------SELECT all user name, region-location, title, text and category from posts----------------

SELECT concat (u.first_name, ' ', u.last_name) as user,
concat (r.region, ' - ', p.post_location) as region_location,
c.category, p.post_title, p.post_text
FROM posts p
JOIN user_region ur
ON ur.id = p.user_region_id
JOIN regions r
ON ur.region_id = r.id
JOIN users u
ON ur.user_id = u.id
JOIN categories c
ON c.id = p.category_id;