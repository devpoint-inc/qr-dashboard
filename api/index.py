from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        if path == '/admin':
            self.admin_page()
        elif path == '/scan':
            self.scan_api(query)
        else:
            self.main_page()
    
    def main_page(self):
        # Send HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스마트 젓가락 QR 스캐너</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 20px; 
            margin: 0;
            min-height: 100vh;
        }
        .container { 
            max-width: 500px; 
            margin: 50px auto; 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px; 
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 { margin-bottom: 20px; font-size: 2em; }
        input { 
            width: 90%; 
            padding: 15px; 
            margin: 10px 0; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
        }
        button { 
            width: 95%; 
            padding: 15px; 
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            cursor: pointer; 
            margin: 10px 0;
        }
        button:hover { transform: translateY(-2px); }
        .result { 
            margin-top: 20px; 
            padding: 15px; 
            border-radius: 8px; 
            display: none; 
        }
        .success { background: rgba(76,175,80,0.7); }
        .error { background: rgba(244,67,54,0.7); }
        .admin-link { 
            color: white; 
            text-decoration: none; 
            position: fixed; 
            top: 20px; 
            right: 20px; 
            background: rgba(255,255,255,0.2); 
            padding: 10px 15px; 
            border-radius: 5px; 
        }
        .admin-link:hover { background: rgba(255,255,255,0.3); }
    </style>
</head>
<body>
    <a href="/admin" class="admin-link">관리자</a>
    <div class="container">
        <h1>🍢 스마트 젓가락</h1>
        <p>QR 코드를 스캔하여 안전성을 확인하세요</p>
        <br>
        <input type="text" id="qrInput" placeholder="QR 코드 입력 (예: SKC-123)" />
        <button onclick="scanQR()">스캔하기</button>
        <div id="result" class="result"></div>
    </div>
    
    <script>
        async function scanQR() {
            const code = document.getElementById('qrInput').value.trim();
            if (!code) { 
                alert('QR 코드를 입력하세요'); 
                return; 
            }
            
            try {
                const response = await fetch('/scan?code=' + encodeURIComponent(code));
                const data = await response.json();
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                
                if (data.status === 'success') {
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = '<h3>✅ ' + data.message + '</h3><p><strong>제품 ID:</strong> ' + data.product_id + '</p><p><strong>사용 횟수:</strong> ' + data.usage_count + '회</p>';
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = '<h3>❌ ' + data.message + '</h3>';
                }
            } catch (e) {
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'result error';
                resultDiv.innerHTML = '<h3>❌ 오류가 발생했습니다</h3>';
            }
        }
        
        // Enter key support
        document.getElementById('qrInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') scanQR();
        });
    </script>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def admin_page(self):
        # Send HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>관리자 대시보드</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white; 
            padding: 20px; 
            margin: 0;
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 50px auto; 
            text-align: center; 
        }
        .success { 
            background: rgba(76,175,80,0.7); 
            padding: 30px; 
            border-radius: 15px; 
            margin: 20px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .home-link { 
            color: white; 
            text-decoration: none; 
            position: fixed; 
            top: 20px; 
            left: 20px; 
            background: rgba(255,255,255,0.2); 
            padding: 10px 15px; 
            border-radius: 5px; 
        }
        .home-link:hover { background: rgba(255,255,255,0.3); }
        h1 { font-size: 2.5em; margin-bottom: 30px; }
        h2 { margin-bottom: 15px; }
    </style>
</head>
<body>
    <a href="/" class="home-link">← 홈</a>
    <div class="container">
        <h1>🍢 관리자 대시보드</h1>
        <div class="success">
            <h2>🎉 Vercel 배포 성공!</h2>
            <p>Python 서버리스 함수가 정상 작동하고 있습니다!</p>
            <br>
            <p><strong>테스트 QR 코드:</strong></p>
            <p>✅ SKC-123 (안전)</p>
            <p>✅ SKC-456 (안전)</p>
            <p>❌ ABC-123 (오류)</p>
        </div>
    </div>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def scan_api(self, query):
        # Send JSON response
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        code = query.get('code', [''])[0]
        
        if not code:
            response = {'status': 'error', 'message': 'QR 코드가 없습니다'}
        elif code.startswith('SKC-'):
            response = {
                'status': 'success',
                'message': '안전합니다 - 최초 사용',
                'product_id': code,
                'usage_count': 1,
                'scan_time': datetime.datetime.now().isoformat()
            }
        else:
            response = {'status': 'error', 'message': '유효하지 않은 QR 코드입니다'}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8')) 