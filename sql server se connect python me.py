from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# SQL Server कनेक्शन सेट करने का फंक्शन
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'          # अगर सर्वर इसी लैपटॉप पर है तो localhost रखें
        'DATABASE=MyWebDB;'          # हमारे डेटाबेस का नाम
        'Trusted_Connection=yes;'    # Windows Authentication के लिए
    )
    return conn

# 1. मुख्य होम पेज
@app.route('/')
def home():
    return render_template('index.html')

# 2. नया लॉगिन पेज
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']
        
        # SQL Server से डेटा चेक करना
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (input_username, input_password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return "<h1>SQL Server: लॉगिन सफल! आपका स्वागत है।</h1>"
        else:
            return "<h1>गलत यूजरनेम या पासवर्ड! दोबारा कोशिश करें।</h1>"
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)