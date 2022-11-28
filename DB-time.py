import sqlite3
drop_sql = "DROP TABLE IF EXISTS Time"
crt_sql = "CREATE TABLE IF NOT EXISTS Time (time NUMERIC, time2 TEXT, time3 BLOB, time4 REAL, time5 INTEGER )"
db = sqlite3.connect("MachineLearning_BeatMaker.db")
rows = db.execute(drop_sql)
rows = db.execute(crt_sql)
rows = db.execute("INSERT INTO Time VALUES(datetime('now'),datetime('now'),datetime('now'),datetime('now'),datetime('now'))")
cursor = db.cursor()
cursor.execute("SELECT * FROM Time")
for row in cursor:
    print("Time is " + row[0], "\nTime2 is " + row[1], "\nTime3 is " + row[2], "\nTime4 is " + row[3], "\nTime5 is " + row[4])
db.commit()
db.close()
