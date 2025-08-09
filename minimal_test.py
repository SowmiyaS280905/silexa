from flask import Flask, jsonify
import webbrowser
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SILEXA Test</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; }
            .test-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; margin: 10px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>🎉 SILEXA Web App is Working!</h1>
        <p>Flask server is running successfully.</p>
        <button class="test-btn" onclick="testSpeech()">🔊 Test Speech</button>
        <button class="test-btn" onclick="testAPI()">🔗 Test API</button>
        <div id="result"></div>
        
        <script>
            function testSpeech() {
                if ('speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance('Hello from SILEXA!');
                    speechSynthesis.speak(utterance);
                    document.getElementById('result').innerHTML = '<p style="color: green;">✅ Speech test successful!</p>';
                } else {
                    document.getElementById('result').innerHTML = '<p style="color: red;">❌ Speech not supported</p>';
                }
            }
            
            async function testAPI() {
                try {
                    const response = await fetch('/api/test');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = '<p style="color: green;">✅ API test: ' + data.message + '</p>';
                } catch (error) {
                    document.getElementById('result').innerHTML = '<p style="color: red;">❌ API test failed</p>';
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/test')
def test_api():
    return jsonify({'success': True, 'message': 'API is working!'})

def open_browser():
    time.sleep(1)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Starting minimal SILEXA test...")
    threading.Thread(target=open_browser).start()
    app.run(debug=False, host='localhost', port=5000)
