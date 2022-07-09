SELECT name FROM people
JOIN stars on stars.person_id = people.id
JOIN movies on stars.movie_id = movies.id
WHERE movies.id IN (
SELECT movies.id FROM people
JOIN stars on stars.person_id = people.id
JOIN movies on stars.movie_id = movies.id
WHERE people.name = "Kevin Bacon"
AND people.birth = "1958")
AND people.name != "Kevin Bacon";
