import sqlite3


def setup_db():
    con = sqlite3.connect("games.db")

    cursor = con.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS 
    matches(battle_time TEXT PRIMARY KEY, opponent_name TEXT, result INTEGER)""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS 
    opponent_cards(battle_time, card_id INTEGER)""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS 
    my_cards(battle_time, card_id INTEGER)""")
    
    con.commit()
    con.close()


def update_game(battle, opponent, enemy_cards_local, my_cards_local, game_result):
    con = sqlite3.connect("games.db")
    cursor = con.cursor()

    cursor.execute("SELECT battle_time FROM matches WHERE battle_time = ?", (battle,))
    gefundenes_spiel = cursor.fetchone()

    if gefundenes_spiel is None:
        cursor.execute("INSERT INTO matches VALUES(?, ?, ?)", (battle, opponent, game_result))
        for card in enemy_cards_local:
            cursor.execute("INSERT INTO opponent_cards VALUES(?, ?)", (battle, card))
        for card in my_cards_local:
            cursor.execute("INSERT INTO my_cards VALUES(?, ?)", (battle, card))
            
    con.commit()
    con.close()


def enemy_card_stats():
    con = sqlite3.connect("games.db")
    cursor = con.cursor()

    stats_request =("""
    SELECT
        opponent_cards.card_id,
        COUNT (*) AS games_total,
        SUM(CASE WHEN matches.result = 1 THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN matches.result = 0 THEN 1 ELSE 0 END) AS draws 
    FROM opponent_cards
    JOIN matches ON opponent_cards.battle_time = matches.battle_time
    GROUP BY opponent_cards.card_id
    ORDER BY 
            games_total DESC,
            wins DESC;                 
    """)

    cursor.execute(stats_request)
    stats = cursor.fetchall()
    
    con.close()
    
    return stats
    
def my_card_stats():
    con = sqlite3.connect("games.db")
    cursor = con.cursor()

    stats_request =("""
    SELECT
        my_cards.card_id,
        COUNT (*) AS games_total,
        SUM(CASE WHEN matches.result = 1 THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN matches.result = 0 THEN 1 ELSE 0 END) AS draws 
    FROM my_cards
    JOIN matches ON my_cards.battle_time = matches.battle_time
    GROUP BY my_cards.card_id
    ORDER BY 
            games_total DESC,
            wins DESC;                 
    """)

    cursor.execute(stats_request)
    stats = cursor.fetchall()
    
    con.close()
    
    return stats
    
