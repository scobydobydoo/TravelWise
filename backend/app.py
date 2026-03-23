from flask import Flask, request, jsonify
import sqlite3

app= Flask(__name__)

def get_db():
    conn=sqlite3.connect("travel.db")
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/signup', methods=['POST'])
def signup():
    data= request.json
    username=data['username']
    password=data['password']
    
    conn=get_db()
    cur=conn.cursor()
    
    try:
        cur.execute("INSERT INTO Users (username, password)VALUES(?,?)",(username,password))
        conn.commit()
        return jsonify({"message": "signup successfull"})
    except:
        return jsonify({"message": "User already exist"})
    finally:
        conn.close()
        
@app.route('/login',methods=['POST'])
def login():
    data=request.json
    username=data['username']
    password=data['password']
    
    conn=get_db()
    cur=conn.cursor()
    
    cur.execute("SELECT * FROM Users WHERE username=? AND password=?",(username,password))
    user=cur.fetchone()
    conn.close()
    
    if user:
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"fail"})
    
if __name__ == "__main__":
    app.run(debug=True)
