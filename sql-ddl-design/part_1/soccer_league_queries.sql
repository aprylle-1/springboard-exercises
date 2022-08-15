-------Select all players and their respective team names------
SELECT concat(p.first_name, ' ', p.last_name) as player,
t.team_name
FROM players p
JOIN teams t
ON p.team_id = t.id
ORDER BY player;


------ Count the number of players per team ------
SELECT team_name, count(*) as team_players
FROM players p
JOIN teams t
ON p.team_id = t.id
GROUP BY team_name
ORDER BY team_players DESC, team_name;