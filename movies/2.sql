SELECT birth FROM people
WHERE id IN (SELECT id FROM people WHERE name = "Emma Stone");