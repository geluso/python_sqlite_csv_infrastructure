import sqlite3
import pandas
import csv

df = pandas.read_csv("iris.csv")
#df.insert(0, "ID", range(0, len(df)))

#print(df)
cnx = sqlite3.connect("iris.db")
with cnx:
    df.to_sql("irises", cnx, if_exists = 'replace', index=False)

def increment(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS irises_copy')
    cur.execute("CREATE TABLE IF NOT EXISTS irises_copy(id integer primary key autoincrement, SepL real,SepW real ,PetL real ,PetW real, Class text)")
    cur.execute('INSERT INTO irises_copy (SepL, SepW, PetL, PetW, Class) SELECT SepL, SepW, PetL, PetW, Class from irises')
#    cur.execute('DROP TABLE irises')
#    cur. execute ('ALTER TABLE irises_copy rename to irises')
    conn.commit()
#    conn.close()

def view(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM irises_copy")
    rows= cur.fetchall()
    conn.close
    return rows

def print_names(conn):
    cur = conn.cursor()
    cur.execute('PRAGMA TABLE_INFO({})'.format('irises_copy'))
    names = [tup[1] for tup in cur.fetchall()]
    print(names)
    conn.close

def delete(id, conn):
    with conn:
        dele = 'DELETE FROM irises_copy WHERE id = ?'
        conn.execute(dele,(id, ))

def insert(SepL, SepW, PetL, PetW, Class, conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO irises_copy (SepL, SepW, PetL, PetW, Class) VALUES (?,?,?,?,?)", (SepL, SepW, PetL, PetW, Class))
    conn.commit()

def update(id, SepL, SepW, PetL, PetW, Class, conn):
    cur = conn.cursor()
    cur.execute("UPDATE irises_copy SET SepL=?, SepW=?, PetL=?, PetW=?,Class=? WHERE id=?", (SepL, SepW,PetL, PetW, Class, id))
    conn.commit()

def search2(conn, SepL="", SepW="", PetL="", PetW="", Class=""):
    cur=conn.cursor()
    #cur.execute('SELECT SepL, SepW FROM irises_copy WHERE SepL=? AND SepW=? AND PetL=? AND PetW=? AND Class=?', (SepL, SepW, PetL, PetW,Class))
    cur.execute('SELECT * FROM irises_copy WHERE SepL=? AND SepW=?', [5.1, 3.5])
    rows=cur.fetchall()
    return rows

def search(conn, SepL="", SepW="", PetL="", PetW="", Class=""):
  cur=conn.cursor()

  query = 'SELECT * FROM irises_copy'
  columns = []
  values = []
  if SepL != "":
    columns.append("SepL=?")
    values.append(SepL)

  if SepW != "":
    columns.append("SepW=?")
    values.append(SepW)

  if PetL != "":
    columns.append("PetL=?")
    values.append(PetL)

  if PetW != "":
    columns.append("PetW=?")
    values.append(PetW)

  if Class != "":
    columns.append("Class=?")
    values.append(Class)

  if len(columns) > 0:
    where_str = " WHERE "
    where_str += " AND ".join(columns)
    query += where_str

  print(query)
  cur.execute(query, values)
  rows=cur.fetchall()
  return rows

def close(conn):
    cur = conn.cursor()
    cur = conn.close()


increment(cnx)

#delete(149, cnx)
#insert(2,3,4,5,"viringina", cnx)
#update(151,3,4,5,6,"virginia", cnx)
#print(view(cnx))
#print(print_names(cnx))

print(search(cnx))
close(cnx)
