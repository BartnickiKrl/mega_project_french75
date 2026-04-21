
-- select m.Title
-- from (SELECT m.Title,m.id   
--     FROM intersecter_Movies m
--     inner join intersecter_LetterboxdUsers u on u.MovieID = m.id
--     INNER JOIN intersecter_Genres g ON m.GENREID = g.NAME
--     WHERE u.NickName in ({users_list}) and
--     WHERE g.Name = {selected_genre}) movie
-- inner join intersecter_LetterboxdUsers u on u.MovieID = movie.id
-- group by m.Title
-- order by count(u.Name) desc
-- Limit {n}

select m.Title, m.Year, d.Name
FROM intersecter_Movies as m
inner join intersecter_letterboxdusers_movieid as um on um.movies_id = m.id
inner join intersecter_LetterboxdUsers as u on u.NickName = um.letterboxdusers_id
inner join intersecter_movies_directorid as md on md.movies_id = m.id
inner join intersecter_movies_genreid as mg on mg.movies_id = m.id
INNER JOIN intersecter_Genres as g ON g.Name = mg.genres_id
inner join intersecter_Directors as d on d.Name = md.directors_id
WHERE u.NickName in ({users_list}) and
g.Name = {selected_genre} 
group by m.Title, m.Year, d.Name
order by count(u.NickName) desc
Limit 1 OFFSET {n}

