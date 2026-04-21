
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

select m.Title, m.Year, m.DirectorID
FROM intersecter_Movies m
inner join intersecter_LetterboxdUsers u on u.MovieID = m.id
INNER JOIN intersecter_Genres g ON m.GENREID = g.NAME
WHERE u.NickName in ({users_list}) and
g.Name = {selected_genre} 
group by m.Title, m.Year, m.DirectorID
order by count(u.Name) desc
Limit {n}

