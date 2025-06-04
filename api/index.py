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
        
        # Set common headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        if path == '/admin':
            self.admin_page()
        elif path == '/scan':
            self.scan_api(query)
        else:
            self.main_page()
    
    def main_page(self):
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Chopstick QR Scanner</title>
    <style>
        body { font-family: Arial, sans-serif; background: #667eea; color: white; padding: 20px; }
        .container { max-width: 500px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; text-align: center; }
        input { width: 100%; padding: 15px; margin: 10px 0; border: none; border-radius: 8px; font-size: 16px; }
        button { width: 100%; padding: 15px; background: #ff6b6b; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; border-radius: 8px; display: none; }
        .success { background: rgba(76,175,80,0.5); }
        .error { background: rgba(244,67,54,0.5); }
        a { color: white; text-decoration: none; position: fixed; top: 20px; right: 20px; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <a href="/admin">관리자</a>
    <div class="container">
        <h1>스마트 젓가락 QR 스캐너</h1>
        <p>QR 코드를 스캔하여 안전성을 확인하세요</p>
        <input type="text" id="qrInput" placeholder="QR 코드 입력 (예: SKC-123)" />
        <button onclick="scanQR()">스캔하기</button>
        <div id="result" class="result"></div>
    </div>
    
    <script>
        async function scanQR() {
            const code = document.getElementById('qrInput').value.trim();
            if (!code) { alert('QR 코드를 입력하세요'); return; }
            
            try {
                const response = await fetch('/scan?code=' + encodeURIComponent(code));
                const data = await response.json();
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                
                if (data.status === 'success') {
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = '<h3>' + data.message + '</h3><p>제품: ' + data.product_id + '</p>';
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = '<h3>' + data.message + '</h3>';
                }
            } catch (e) {
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'result error';
                resultDiv.innerHTML = '<h3>오류가 발생했습니다</h3>';
            }
        }
    </script>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def admin_page(self):
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>관리자 대시보드</title>
    <style>
        body { font-family: Arial, sans-serif; background: #2c3e50; color: white; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; text-align: center; }
        .success { background: rgba(76,175,80,0.5); padding: 20px; border-radius: 10px; margin: 20px 0; }
        a { color: white; text-decoration: none; position: fixed; top: 20px; left: 20px; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <a href="/">← 홈</a>
    <div class="container">
        <h1>관리자 대시보드</h1>
        <div class="success">
            <h2>🎉 Vercel 배포 성공!</h2>
            <p>Python 서버리스 함수가 정상 작동합니다</p>
            <p><strong>테스트 코드:</strong> SKC-123, SKC-456</p>
        </div>
    </div>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def scan_api(self, query):
        # Change response to JSON for API endpoint
        self.send_header('Content-type', 'application/json')
        
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