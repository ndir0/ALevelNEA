import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

def createLoginTable():
    c.execute("""CREATE TABLE IF NOT EXISTS logins(
             username varchar(255),
             password varchar(255)
             )""")

def createDetailsTable():
    c.execute("""CREATE TABLE IF NOT EXISTS details(
             username varchar(255),
             age integer,
             gender varchar(6),
             height float,
             weight float
             )""")

def createClassTable():
    c.execute("""CREATE TABLE IF NOT EXISTS class(
             firstClass varchar(255),
             secondClass varchar(255),
             thirdClass varchar(255)
             )""")

def createUserClassTable():
    c.execute("""CREATE TABLE IF NOT EXISTS userclass(
             username varchar(255),
             firstClass varchar(255),
             secondClass varchar(255),
             thirdClass varchar(255)
             )""")

def createMatchedTable():
    c.execute("""CREATE TABLE IF NOT EXISTS matches(
             username varchar(255),
             class varchar(255)
             )""")
