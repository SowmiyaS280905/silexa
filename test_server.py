from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🎉 SILEXA Server Test</h1>
    <p>Flask server is working!</p>
    <a href="/detect">Go to Detection Page</a>
    '''

@app.route('/detect')
def detect():
    return '''
    <h1>Detection Page</h1>
    <p>This would be the detection interface.</p>
    <a href="/">Back to Home</a>
    '''

if __name__ == '__main__':
    print("🚀 Starting test server...")
    print("🌐 Server will be at: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)
