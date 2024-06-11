--Задание 2.
-- 1. Название и продолжительность самого длительного трека.
--Выбираем название и продолжительность треков (t)
SELECT t.track_name, t.duration
FROM track t
ORDER BY t.duration DESC
-- отсорировать по убыванию
LIMIT 1;
-- ограничить выбору - самый длинный

--2. Название треков, продолжительность которых не менее 3,5 минут
--Выбираем название треков
SELECT t.track_name
FROM track t
WHERE t.duration >= 210;
--Фильтруем треки, продолжительность которых не менее 3,5 минут

--3. Названия сборников, вышедших в период с 2018 по 2020 год включительно
--Выбираем названия сборников
SELECT c.collection_name
FROM collection_of_songs c
WHERE c.year_of_release BETWEEN 2018 AND 2020;
--Фильтруем сборники, вышедшие в период с 2018 по 2020 год включительно

--4. Исполнители, чьё имя состоит из одного слова.
--Выбираем исполнителей
SELECT a.artist_name
FROM artist a
WHERE a.artist_name NOT LIKE '% %';
--Фильтруем исполнителей, чье имя состоит из одного слова

--5. Название треков, которые содержат слово «мой» или «my».
--Выбираем название треков из таблицы track
SELECT t.track_name
FROM track t
WHERE LOWER(
    t.track_name) LIKE '%my%' OR LOWER(t.track_name) LIKE '%мой%';
--перед запросом фильтрации все символы в столбце переведены в нижний регистр

-- Задание 3.
--1. Количество исполнителей в каждом жанре
-- выбираем жанр и количество исполнителей в этом жанре (g) 
SELECT g.genre_name, COUNT(ga.artist_id) 
FROM genre g
JOIN genre_artist ga ON g.id = ga.genre_id
--Соединяем таблицу genre с genre_artist по ID жанра
GROUP BY g.genre_name;
--Группируем результаты по названию жанра, 
--чтобы подсчитать количество исполнителей в каждом жанре.

--2. Количество треков, вошедших в альбомы 2019-2020 годов
--Выбираем количество треков, вошедших в альбомы 2019-2020 годов (a) 
SELECT COUNT(t.album_id)
FROM album a
JOIN track t ON a.id = t.album_id
--Соединяем таблицу album с track по ID альбома
WHERE a.year_of_release BETWEEN 2019 AND 2020;
--Фильтруем альбомы 2019-2020 годов

--3. Средняя продолжительность треков по каждому альбому
--Выбираем среднюю продолжительность треков по каждому альбому (t)
SELECT a.album_name, AVG(t.duration)
FROM album a
JOIN track t ON a.id = t.album_id
--Соединяем таблицу album с track по ID альбома
GROUP BY a.album_name;
--Группируем результаты по названию альбома

--4. Количество исполнителей, которые не выпустили альбомы в 2019-2020 годах
--Выбираем количество исполнителей 
SELECT COUNT(DISTINCT alb_art.artist_id)
FROM album AS alb
JOIN artist_album AS alb_art ON alb.id = alb_art.album_id
-- Соединяем таблицу album с artist_album по ID альбома
JOIN artist AS art ON alb_art.artist_id = art.id
-- Соединяем таблицу artist_album с artist по ID исполнителя
WHERE alb.year_of_release NOT BETWEEN 2019 AND 2020;
--Фильтруем исполнителей, которые не выпустили альбомы в 2019-2020 годах

--5. Названия сборников, в которых присутствует исполнитель Григорий Лепс
--Выбираем названия сборников
SELECT DISTINCT c.collection_name 
FROM collection_of_songs c
JOIN collection_track ct ON c.id = ct.collection_id
-- Соединяем таблицу collection_of_songs с collection_track по ID сборника
JOIN track t ON ct.track_id = t.id
-- Соединяем таблицу collection_track с track по ID трека
JOIN album a ON t.album_id = a.id
-- Соединяем таблицу track с album по ID альбома
JOIN artist_album aa ON a.id = aa.album_id
-- Соединяем таблицу album с artist_album по ID альбома
JOIN artist a2 ON aa.artist_id = a2.id
-- Соединяем таблицу artist_album с artist по ID исполнителя
WHERE a2.artist_name = 'Григорий Лепс';
--Фильтруем сборники, в которых присутствует исполнитель Григорий Лепс

--Задание 4. 
--1.Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
--Выбираем названия альбомов
SELECT a.album_name
FROM album a
JOIN artist_album aa ON a.id = aa.album_id
--Соединяем таблицу album с artist_album по ID альбома
JOIN artist a2 ON aa.artist_id = a2.id
--Соединяем таблицу artist_album с artist по ID исполнителя
JOIN genre_artist ga ON a2.id = ga.artist_id
--Соединяем таблицу artist с genre_artist по ID исполнителя
JOIN genre g ON ga.genre_id = g.id
--Соединяем таблицу genre_artist с genre по ID жанра
GROUP BY a.album_name
--Группируем результаты по названию альбома
HAVING COUNT(ga.genre_id) > 1;
--Фильтруем альбомы, в которых присутствуют исполнители более чем одного жанра

--2.Наименования треков, которые не входят в сборники.
--Выбираем названия треков
SELECT t.track_name
FROM track t
LEFT JOIN track_collection tc ON t.id = tc.track_id
-- Соединяем таблицу track с track_collection по ID трека
WHERE tc.track_id IS NULL;
--Фильтруем треки, которые не входят в сборники

--3. Исполнитель или исполнители, написавшие 
--самый короткий по продолжительности трек, — 
--теоретически таких треков может быть несколько.
--Выбираем исполнителя или исполнителей
SELECT a.artist_name
FROM artist a
JOIN artist_album aa ON a.id = aa.artist_id
--Соединяем таблицу artist с artist_album по ID исполнителя
JOIN album a2 ON aa.album_id = a2.id
--Соединяем таблицу artist_album с album по ID альбома
JOIN track t ON a2.id = t.album_id
--Соединяем таблицу album с track по ID альбома
WHERE t.duration = (SELECT MIN(duration) FROM track);

--4.Названия альбомов, содержащих наименьшее количество треков
--Выбираем названия альбомов
SELECT a.album_name
FROM album a
-- Соединяем таблицу album с подзапросом, который считает количество треков для каждого альбома
JOIN (
    SELECT album_id, COUNT(*) as tracks_count
    FROM track
    -- Группируем треки по album_id, чтобы получить количество треков для каждого альбома
    GROUP BY album_id
) subquery ON a.id = subquery.album_id
-- Фильтруем альбомы, оставляя только те, количество треков в которых совпадает 
--с минимальным значением среди всех альбомов
WHERE subquery.tracks_count = (
    -- Подзапрос для нахождения минимального количества треков среди всех альбомов
    SELECT MIN(tracks_count)
    FROM (
        -- Считываем количество треков для каждого альбома
        SELECT COUNT(*) as tracks_count
        FROM track
        -- Группируем треки по album_id, чтобы получить количество треков для каждого альбома
        GROUP BY album_id
    )
);
