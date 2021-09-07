import os
import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "dbname=foodtruck")

def sql_fetch(query, parameters=[]):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, parameters)
  results = cur.fetchall()
  conn.close()
  return results

def sql_fetch_one(query, parameters=[]):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, parameters)
  results = cur.fetchone()
  conn.close()
  return results

def sql_write(query, parameters=[]):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, parameters)
  print(query)
  conn.commit()
  conn.close()