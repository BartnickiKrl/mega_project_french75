
-- nalezy stosowac tabele przejsciowe!!!!!

select m.Title, m.Year, d.Name, count(DISTINCT u.NickName)
FROM intersecter_Movies as m
inner join intersecter_letterboxdusers_movieid as um on um.movies_id = m.id
inner join intersecter_LetterboxdUsers as u on u.NickName = um.letterboxdusers_id
inner join intersecter_movies_directorid as md on md.movies_id = m.id
inner join intersecter_movies_genreid as mg on mg.movies_id = m.id
INNER JOIN intersecter_Genres as g ON g.Name = mg.genres_id
inner join intersecter_Directors as d on d.Name = md.directors_id
WHERE u.NickName in ({u_placeholders}) and
m.Title not in ({m_placeholders}) and
g.Name = %s
group by m.Title, m.Year, d.Name
having count(DISTINCT u.NickName)>=%s
order by count(DISTINCT u.NickName) desc
Limit 1 

