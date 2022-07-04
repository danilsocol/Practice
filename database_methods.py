import sqlite3
import json

conn = sqlite3.connect('BuyBot.db')
cur = conn.cursor()
cur.execute("""
CREATE TRIGGER price_update
AFTER UPDATE ON Favourites
WHEN :OLD.price<>:NEW.price
BEGIN
    INSERT INTO Favourites_price_updates(fav_id, updated, price)
    VALUES (id, datetime(now), :NEW.price)
END;
""")

cur.execute("""
CREATE TRIGGER add_fav_row
AFTER INSERT ON Favourites
BEGIN
    INSERT INTO Favourites_price_updates(fav_id, updated, price, action)
    VALUES (id, datetime(now), price, 'start')
END;
""")

conn.commit()