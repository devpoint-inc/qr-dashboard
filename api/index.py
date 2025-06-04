from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json

app = Flask(__name__)

# Main page template
MAIN_PAGE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍢 Smart Chopstick QR Scanner</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            color: white; padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 20px;
            padding: 30px; max-width: 500px; width: 100%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        h1 { margin-bottom: 20px; font-size: 2em; }
        .input-group { margin: 20px 0; }
        input {
            width: 100%; padding: 15px; border: none; border-radius: 10px;
            font-size: 16px; background: rgba(255, 255, 255, 0.9);
            margin-bottom: 15px;
        }
        button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white; border: none; padding: 15px 30px;
            border-radius: 10px; font-size: 16px; cursor: pointer;
            width: 100%; margin: 10px 0;
        }
        button:hover { transform: translateY(-2px); }
        .result {
            margin-top: 20px; padding: 20px; border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            display: none;
        }
        .success { background: rgba(76, 175, 80, 0.3); }
        .warning { background: rgba(255, 152, 0, 0.3); }
        .error { background: rgba(244, 67, 54, 0.3); }
        .admin-link {
            position: fixed; top: 20px; right: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px; border-radius: 10px;
            text-decoration: none; color: white;
        }
    </style>
</head>
<body>
    <a href="/admin" class="admin-link">관리자</a>
    <div class="container">
        <h1>🍢 스마트 젓가락</h1>
        <p>QR 코드를 스캔하여 안전성을 확인하세요</p>
        
        <div class="input-group">
            <input type="text" id="qrInput" placeholder="QR 코드를 입력하세요 (예: SKC-123)" />
            <button onclick="scanQR()">스캔하기</button>
        </div>
        
        <div id="result" class="result"></div>
    </div>

    <script>
        async function scanQR() {
            const qrCode = document.getElementById('qrInput').value.trim();
            if (!qrCode) {
                alert('QR 코드를 입력해주세요');
                return;
            }
            
            try {
                const response = await fetch(`/scan?code=${qrCode}`);
                const data = await response.json();
                
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                
                if (data.status === 'success') {
                    let className = 'success';
                    if (data.scan_result === 'potential_reuse') className = 'warning';
                    if (data.scan_result === 'multiple_reuse') className = 'error';
                    
                    resultDiv.className = `result ${className}`;
                    resultDiv.innerHTML = `
                        <h3>${data.message_kr}</h3>
                        <p>제품 ID: ${data.product_id}</p>
                        <p>사용 횟수: ${data.usage_count}회</p>
                        <p>검사 시간: ${new Date().toLocaleString('ko-KR')}</p>
                    `;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `<h3>${data.message_kr || '오류가 발생했습니다'}</h3>`;
                }
            } catch (error) {
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'result error';
                resultDiv.innerHTML = '<h3>오류가 발생했습니다</h3>';
            }
        }
        
        // Enter key support
        document.getElementById('qrInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') scanQR();
        });
    </script>
</body>
</html>
'''

ADMIN_PAGE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍢 관리자 대시보드</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            min-height: 100vh; color: white; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .demo-note {
            background: rgba(76, 175, 80, 0.3);
            border: 1px solid rgba(76, 175, 80, 0.5);
            border-radius: 10px; padding: 20px; margin-bottom: 20px;
            text-align: center;
        }
        .home-link {
            position: fixed; top: 20px; left: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px; border-radius: 10px;
            text-decoration: none; color: white;
        }
    </style>
</head>
<body>
    <a href="/" class="home-link">← 홈</a>
    <div class="container">
        <h1>🍢 관리자 대시보드</h1>
        
        <div class="demo-note">
            <h2>🎉 Flask + Vercel 배포 성공!</h2>
            <p>단일 Flask 앱으로 모든 라우팅이 정상 작동합니다.</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(MAIN_PAGE)

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_PAGE)

@app.route('/scan')
def scan():
    qr_code = request.args.get('code', '')
    
    if not qr_code:
        return jsonify({
            'status': 'error',
            'message': 'QR code parameter missing',
            'message_kr': 'QR 코드가 없습니다'
        }), 400
    
    if qr_code.startswith('SKC-'):
        return jsonify({
            'status': 'success',
            'product_id': qr_code,
            'usage_count': 1,
            'scan_result': 'first_use',
            'message_kr': '안전합니다 - 최초 사용',
            'icon': 'success',
            'scan_time': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid QR Code',
            'message_kr': '유효하지 않은 QR 코드입니다'
        }), 404

# Vercel serverless function handler
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True) 