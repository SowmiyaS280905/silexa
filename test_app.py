from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "SILEXA Web App is working!"

if __name__ == '__main__':
    print("Testing Flask...")
    app.run(debug=True, host='localhost', port=5000)
