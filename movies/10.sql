SELECT DISTINCT(name)
FROM people
WHERE id in (SELECT person_id FROM directors WHERE movie_id IN (SELECT movie_id FROM ratings WHERE rating >= 9.0));