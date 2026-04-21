


SELECT m.id, m.Title,  
FROM intersecter_Movies m
inner join intersecter_LetterboxdUsers u on u.MovieID = m.id
INNER JOIN intersecter_Genres g ON m.GENREID = g.NAME
WHERE u.NickName in (users_list)
WHERE g.Name = {selected_genre}