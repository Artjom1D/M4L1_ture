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