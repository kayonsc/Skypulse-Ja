from flask import Flask, request
import pymysql

app = Flask(__name__)

def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    drone_id = data.get("drone_id")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO drone_locations (drone_id, latitude, longitude) VALUES (%s, %s, %s)",
                   (drone_id, latitude, longitude))
    conn.commit()
    conn.close()
    return {"status": "success"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)