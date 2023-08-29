import mysql.connector
import random
from prettytable import PrettyTable

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="gacha"
)
dbcursor = db.cursor()

count5 = 0
count4 = 0

def generate():
    global count5
    num = random.randint(1, 1000)
    rate5 = 6
    if count5 > 75:
        rate5 = 6 + 994/15*(count5-75)
    if num <= rate5:
        return 5
    elif num <= 51 + rate5:
        return 4
    else:
        return 3

def roll():
    global count5
    global count4
    rarity = generate()
    if count5 == 90:
        rarity = 5
        count5 = 0
        count4 = 0
    elif rarity == 5:
        count5 = 0
        count4 = 0
    elif count4 == 9:
        rarity = 4
        count5 += 1
        count4 = 0
    elif rarity == 4:
        count5 += 1
        count4 =0
    elif rarity == 3:
        count5 += 1
        count4 += 1
    return rarity

def pull(a5, a4):
    global count5
    global count4
    count5 = a5
    count4 = a4
    rarity = roll()
    dbcursor.execute("SELECT name, rarity FROM characters WHERE rarity = %s", [rarity])
    fetched1 = dbcursor.fetchall()
    dbcursor.execute("SELECT name, rarity FROM weapons WHERE rarity = %s AND location = %s", [rarity, 'Gacha'])
    fetched2 = dbcursor.fetchall()
    fetched = fetched1 + fetched2
    num = random.randrange(len(fetched))
    return fetched[num], count5, count4