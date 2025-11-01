import sqlite3

con = sqlite3.connect("movie.db")
cur = con.cursor()

cur.execute("SELECT title, popularity FROM movies ORDER BY popularity DESC LIMIT 1")
print(cur.fetchall())

cur.execute("SELECT title, budget FROM movies WHERE release_date LIKE '2009-12%' ORDER BY budget DESC LIMIT 1")
print(cur.fetchall())

cur.execute("""SELECT title FROM movies WHERE tagline LIKE '%The battle within%' """)
print(cur.fetchall())

cur.execute("SELECT vote_count FROM movies WHERE release_date < '1980' and vote_average > 8 ORDER BY vote_count DESC LIMIT 1")
print(cur.fetchall())

cur.execute("""SELECT directors.name, MAX(movies.release_date) as last_movie_date 
        FROM movies
        INNER JOIN directors ON movies.director_id = directors.id
        WHERE directors.name IS NOT NULL
        GROUP BY directors.name
        ORDER BY last_movie_date DESC
            """)
print(cur.fetchall())

cur.execute("""SELECT directors.name, SUM(movies.budget) as total_budget
        FROM movies
        INNER JOIN directors ON movies.director_id = directors.id
        WHERE directors.name IS NOT NULL
        GROUP BY directors.name""")

cur.execute("""SELECT directors.name, COUNT(movies.id) as times_directed 
    FROM movies 
    INNER JOIN directors ON movies.director_id = directors.id 
    WHERE directors.name IS NOT NULL 
    GROUP BY directors.name 
    ORDER BY times_directed DESC""")

cur.execute("""SELECT movies.title, COUNT(movies_genres.genre_id) as genre_count
        FROM movies_genres
        INNER JOIN movies ON movies.id = movies_genres.movie_id
        WHERE movies_genres.movie_id IS NOT NULL
        GROUP BY movies.title
        ORDER BY genre_count DESC """)

cur.execute("""SELECT directors.name, COUNT(movies_genres.genre_id) as genre_count
            FROM movies_genres
            INNER JOIN movies ON movies.id = movies_genres.movie_id
            INNER JOIN directors ON movies.director_id = directors.id
            WHERE directors.name IS NOT NULL
            GROUP BY directors.name
            ORDER BY genre_count DESC""")