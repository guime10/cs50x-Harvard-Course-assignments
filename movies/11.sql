select movies.title from movies
join stars on stars.movie_id = movies.id
join people on stars.person_id = people.id
join ratings on ratings.movie_id = movies.id
where people.name ="Chadwick Boseman"
order by ratings.rating desc
limit 5;