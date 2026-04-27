import requests
import mysql.connector
import winsound
import urllib.parse
import webbrowser

# API
response = requests.get("https://fakestoreapi.com/products")
data = response.json()

# DB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Himanshu@SQL",
    database="price_monitor"
)

cursor = conn.cursor()

for item in data:
    pid = item['id']
    title = item['title']
    new_price = item['price']

    cursor.execute("SELECT price FROM products WHERE id=%s", (pid,))
    result = cursor.fetchone()

    if result:
        old_price = result[0]

        if new_price != old_price:
            print(f"🔥 Price changed: {title}")
            print(f"{old_price} → {new_price}")

            # 🔊 sound
            winsound.Beep(1000, 5000)

            # 📱 WhatsApp message
            msg = f"🔥 Price changed!\n{title}\n{old_price} → {new_price}"
            encoded_msg = urllib.parse.quote(msg)

            url = f"https://wa.me/918273366684?text={encoded_msg}"
            webbrowser.open(url)

            # DB update
            cursor.execute("""
                UPDATE products 
                SET price=%s 
                WHERE id=%s
            """, (new_price, pid))
    else:
        cursor.execute("""
            INSERT INTO products (id, title, price)
            VALUES (%s, %s, %s)
        """, (pid, title, new_price))

conn.commit()
conn.close()