import requests
import json
import mysql.connector
from prettytable import PrettyTable

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
dbcursor = db.cursor()

try:
    dbcursor.execute("CREATE DATABASE gacha")
except mysql.connector.errors.DatabaseError:
    pass

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="gacha"
)
dbcursor = db.cursor()

try:
    dbcursor.execute("""CREATE TABLE characters (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    rarity INT,
                    vision VARCHAR(255),
                    weapon VARCHAR(255),
                    gender VARCHAR(255),
                    nation VARCHAR(255)
                    )""")
except mysql.connector.errors.ProgrammingError:
    rewrite = input("rewrite? y/n")
    print(rewrite)
    if rewrite == 'y':
        dbcursor.execute("DROP TABLE characters")
        dbcursor.execute("""CREATE TABLE characters (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        rarity INT,
                        vision VARCHAR(255),
                        weapon VARCHAR(255),
                        gender VARCHAR(255),
                        nation VARCHAR(255)
                        )""")

if rewrite == 'y':
    request = requests.get('https://genshin.jmp.blue/characters')
    characters_data = json.loads(request.text)
    for character_data in characters_data:
        print(character_data)
        request = requests.get('https://genshin.jmp.blue/characters/' + character_data)
        character = json.loads(request.text)
        sql = "INSERT INTO characters (name, rarity, vision, weapon, gender, nation) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            val = (character['name'],
                    character['rarity'],
                    character['vision'],
                    character['weapon'],
                    character['gender'],
                    character['nation'])
        except KeyError:
            if character_data.startswith('traveler'):
                val = (character['name'],
                        character['rarity'],
                        character['vision'],
                        character['weapon'],
                        'Male/Female',
                        character['nation'])
            else:
                val = (character['name'],
                        character['rarity'],
                        character['vision'],
                        character['weapon'],
                        'Female',
                        character['nation'])
        dbcursor.execute(sql, val)
    db.commit()

try:
    dbcursor.execute("""CREATE TABLE weapons (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    rarity INT,
                    type VARCHAR(255),
                    baseAttack INT,
                    subStat VARCHAR(255),
                    location VARCHAR(255)
                    )""")
except mysql.connector.errors.ProgrammingError:
    rewrite = input("rewrite? y/n")
    if rewrite == 'y':
        dbcursor.execute("DROP TABLE weapons")
        dbcursor.execute("""CREATE TABLE weapons (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        rarity INT,
                        type VARCHAR(255),
                        baseAttack INT,
                        subStat VARCHAR(255),
                        location VARCHAR(255)
                        )""")

if rewrite == 'y':
    request = requests.get('https://genshin.jmp.blue/weapons')
    weapons_data = json.loads(request.text)
    for weapon_data in weapons_data:
        print(weapon_data)
        request = requests.get('https://genshin.jmp.blue/weapons/' + weapon_data)
        weapon = json.loads(request.text)
        sql = "INSERT INTO weapons (name, rarity, type, baseAttack, subStat, location) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            val = (weapon['name'],
                    weapon['rarity'],
                    weapon['type'],
                    weapon['baseAttack'],
                    weapon['subStat'],
                    weapon['location'])
        except KeyError:
            val = (weapon['name'],
                    weapon['rarity'],
                    weapon['type'],
                    weapon['BaseAttack'],
                    weapon['subStat'],
                    weapon['location'])
        dbcursor.execute(sql, val)
    db.commit()

dbcursor.execute("SELECT name, rarity, vision, weapon, gender, nation FROM characters ORDER BY name")
fetched = dbcursor.fetchall()
table1 = PrettyTable(['name', 'rarity', 'vision', 'weapon', 'gender', 'nation'])
for row in fetched:
    table1.add_row(row)
print(table1)

dbcursor.execute("SELECT name, rarity, type, baseAttack, subStat, location FROM weapons ORDER BY name")
fetched = dbcursor.fetchall()
table2 = PrettyTable(['name', 'rarity', 'type', 'baseAttack', 'subStat', 'location'])
for row in fetched:
    table2.add_row(row)
print(table2)