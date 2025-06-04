from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import datetime
import random

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
            margin-bottom: 15px; color: #333;
        }
        button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white; border: none; padding: 15px 30px;
            border-radius: 10px; font-size: 16px; cursor: pointer;
            width: 100%; margin: 10px 0;
            transition: all 0.3s ease;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(255, 107, 107, 0.4); }
        .result {
            margin-top: 20px; padding: 20px; border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            display: none; transition: all 0.3s ease;
        }
        .success { 
            background: rgba(76, 175, 80, 0.3); 
            border: 2px solid rgba(76, 175, 80, 0.6);
        }
        .warning { 
            background: rgba(255, 152, 0, 0.3); 
            border: 2px solid rgba(255, 152, 0, 0.6);
        }
        .danger { 
            background: rgba(244, 67, 54, 0.3); 
            border: 2px solid rgba(244, 67, 54, 0.6);
        }
        .error { 
            background: rgba(158, 158, 158, 0.3); 
            border: 2px solid rgba(158, 158, 158, 0.6);
        }
        .admin-link {
            position: fixed; top: 20px; right: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px; border-radius: 10px;
            text-decoration: none; color: white;
            transition: all 0.3s ease;
        }
        .admin-link:hover { background: rgba(255, 255, 255, 0.3); }
        .status-icon { font-size: 2em; margin-bottom: 10px; }
        .product-info { 
            margin-top: 15px; 
            background: rgba(255, 255, 255, 0.1); 
            padding: 15px; 
            border-radius: 8px; 
        }
        .scan-count { font-size: 0.9em; opacity: 0.8; margin-top: 10px; }
    </style>
</head>
<body>
    <a href="/admin" class="admin-link">📊 관리자</a>
    <div class="container">
        <h1>🍢 스마트 대시보드</h1>
        <p>QR 코드를 스캔하여 안전성을 확인하세요</p>
        
        <div class="input-group">
            <input type="text" id="qrInput" placeholder="QR 코드를 입력하세요 (예: SKC-123)" />
            <button onclick="scanQR()">🔍 스캔하기</button>
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
                const response = await fetch('/scan?code=' + encodeURIComponent(qrCode));
                const data = await response.json();
                
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                
                if (data.status === 'success') {
                    let className = 'success';
                    let icon = '✅';
                    let statusText = '안전';
                    
                    if (data.scan_result === 'potential_reuse') {
                        className = 'warning';
                        icon = '⚠️';
                        statusText = '주의';
                    } else if (data.scan_result === 'multiple_reuse') {
                        className = 'danger';
                        icon = '❌';
                        statusText = '위험';
                    }
                    
                    resultDiv.className = 'result ' + className;
                    resultDiv.innerHTML = `
                        <div class="status-icon">${icon}</div>
                        <h3>${statusText} - ${data.message}</h3>
                        <div class="product-info">
                            <p><strong>제품 ID:</strong> ${data.product_id}</p>
                            <p><strong>사용 횟수:</strong> ${data.usage_count}회</p>
                            <p><strong>최근 검사:</strong> ${new Date().toLocaleString('ko-KR')}</p>
                        </div>
                        <div class="scan-count">검사 완료 시간: ${data.scan_time}</div>
                    `;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `
                        <div class="status-icon">❓</div>
                        <h3>오류 - ${data.message}</h3>
                        <p>올바른 QR 코드를 입력해주세요</p>
                    `;
                }
            } catch (error) {
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `
                    <div class="status-icon">⚠️</div>
                    <h3>연결 오류</h3>
                    <p>네트워크 연결을 확인해주세요</p>
                `;
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
        .stats {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 15px;
            padding: 20px; text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number { font-size: 3em; font-weight: bold; margin-bottom: 10px; }
        .stat-card.total { border: 2px solid rgba(52, 152, 219, 0.5); }
        .stat-card.used { border: 2px solid rgba(46, 204, 113, 0.5); }
        .stat-card.reuse { border: 2px solid rgba(231, 76, 60, 0.5); }
        .stat-card.recent { border: 2px solid rgba(241, 196, 15, 0.5); }
        
        .create-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 15px;
            padding: 30px; margin-bottom: 30px;
        }
        .form-group { display: flex; align-items: center; margin-bottom: 20px; gap: 15px; }
        input, select {
            padding: 15px; border: none; border-radius: 10px;
            font-size: 16px; background: rgba(255, 255, 255, 0.9);
            flex: 1; min-width: 200px; color: #333;
        }
        button {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
            color: white; cursor: pointer; padding: 15px 30px;
            border: none; border-radius: 10px; font-size: 16px;
            transition: all 0.3s ease;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(231, 76, 60, 0.4); }
        .qr-display {
            margin-top: 20px; text-align: center;
            background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px;
            display: none; color: #333;
        }
        .home-link {
            position: fixed; top: 20px; left: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px; border-radius: 10px;
            text-decoration: none; color: white;
            transition: all 0.3s ease;
        }
        .home-link:hover { background: rgba(255, 255, 255, 0.3); }
        
        .recent-activity {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 15px;
            padding: 30px; margin-bottom: 30px;
        }
        .activity-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px; border-radius: 8px; margin-bottom: 10px;
            display: flex; justify-content: between; align-items: center;
        }
        .activity-status { 
            padding: 5px 10px; border-radius: 15px; font-size: 0.8em; 
            margin-left: auto;
        }
        .status-safe { background: rgba(76, 175, 80, 0.7); }
        .status-warning { background: rgba(255, 152, 0, 0.7); }
        .status-danger { background: rgba(244, 67, 54, 0.7); }
    </style>
</head>
<body>
    <a href="/" class="home-link">🏠 홈</a>
    <div class="container">
        <h1>🍢 스마트 젓가락 관리자</h1>
        
        <div class="stats">
            <div class="stat-card total">
                <div class="stat-number">1,247</div>
                <div>총 제품 수</div>
                <div style="font-size: 0.8em; opacity: 0.7;">등록된 제품</div>
            </div>
            <div class="stat-card used">
                <div class="stat-number">892</div>
                <div>사용된 제품</div>
                <div style="font-size: 0.8em; opacity: 0.7;">71.5% 사용률</div>
            </div>
            <div class="stat-card reuse">
                <div class="stat-number">23</div>
                <div>재사용 감지</div>
                <div style="font-size: 0.8em; opacity: 0.7;">2.6% 위험도</div>
            </div>
            <div class="stat-card recent">
                <div class="stat-number">156</div>
                <div>24시간 스캔</div>
                <div style="font-size: 0.8em; opacity: 0.7;">실시간 모니터링</div>
            </div>
        </div>
        
        <div class="create-section">
            <h2>🏭 새 제품 배치 등록</h2>
            <div class="form-group">
                <input type="text" id="productName" placeholder="제품명 (예: 프리미엄 젓가락 A형)" />
                <input type="text" id="companyName" placeholder="제조사명" />
                <select id="expiryDays">
                    <option value="30">30일 유효</option>
                    <option value="60">60일 유효</option>
                    <option value="90">90일 유효</option>
                    <option value="180">6개월 유효</option>
                </select>
            </div>
            <div class="form-group">
                <input type="number" id="quantity" placeholder="생산 수량" min="1" max="10000" />
                <button onclick="generateBatch()">📱 배치 생성 및 QR 생성</button>
            </div>
            
            <div id="qrDisplay" class="qr-display">
                <h3>✅ 배치 생성 완료!</h3>
                <div id="qrCode">
                    <div style="width: 200px; height: 200px; background: #f0f0f0; 
                                border: 2px dashed #666; display: flex; align-items: center; 
                                justify-content: center; margin: 20px auto; font-size: 14px; color: #666;">
                        QR 코드 이미지<br>
                        <small>(실제 배포시 생성)</small>
                    </div>
                </div>
                <p id="batchInfo">배치 ID: SKC-2024-001</p>
            </div>
        </div>
        
        <div class="recent-activity">
            <h2>📊 최근 활동 로그</h2>
            <div class="activity-item">
                <div>
                    <strong>SKC-123456</strong> 스캔됨
                    <br><small>2분 전 • IP: 192.168.1.100</small>
                </div>
                <span class="activity-status status-safe">✅ 안전</span>
            </div>
            <div class="activity-item">
                <div>
                    <strong>SKC-789012</strong> 재사용 감지!
                    <br><small>15분 전 • IP: 10.0.0.50</small>
                </div>
                <span class="activity-status status-warning">⚠️ 주의</span>
            </div>
            <div class="activity-item">
                <div>
                    <strong>SKC-345678</strong> 다중 재사용 위험
                    <br><small>1시간 전 • IP: 172.16.1.25</small>
                </div>
                <span class="activity-status status-danger">❌ 위험</span>
            </div>
            <div class="activity-item">
                <div>
                    <strong>배치 SKC-2024-001</strong> 생성됨
                    <br><small>3시간 전 • 관리자</small>
                </div>
                <span class="activity-status status-safe">📦 생성</span>
            </div>
        </div>
    </div>

    <script>
        function generateBatch() {
            const productName = document.getElementById('productName').value || '기본 제품';
            const companyName = document.getElementById('companyName').value || '기본 제조사';
            const quantity = document.getElementById('quantity').value || '100';
            const expiryDays = document.getElementById('expiryDays').value;
            
            const batchId = 'SKC-' + new Date().getFullYear() + '-' + String(Math.floor(Math.random() * 1000)).padStart(3, '0');
            
            // Show batch creation result
            document.getElementById('qrDisplay').style.display = 'block';
            document.getElementById('batchInfo').innerHTML = `
                <strong>배치 ID:</strong> ${batchId}<br>
                <strong>제품명:</strong> ${productName}<br>
                <strong>제조사:</strong> ${companyName}<br>
                <strong>수량:</strong> ${quantity}개<br>
                <strong>유효기간:</strong> ${expiryDays}일<br>
                <strong>생성시간:</strong> ${new Date().toLocaleString('ko-KR')}
            `;
            
            // Simulate statistics update
            setTimeout(() => {
                document.querySelector('.stat-card.total .stat-number').textContent = 
                    (1247 + parseInt(quantity)).toLocaleString();
                alert('✅ 배치 생성 완료!\\n' + quantity + '개의 QR 코드가 생성되었습니다.');
            }, 1000);
        }
        
        // Simulate real-time updates
        setInterval(() => {
            const recentScans = document.querySelector('.stat-card.recent .stat-number');
            const currentCount = parseInt(recentScans.textContent);
            if (Math.random() > 0.7) { // 30% chance
                recentScans.textContent = currentCount + 1;
            }
        }, 10000);
    </script>
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
            # Simulate different usage scenarios
            usage_scenarios = [
                {'count': 1, 'result': 'first_use', 'message': '최초 사용 확인'},
                {'count': 2, 'result': 'potential_reuse', 'message': '재사용 의심'},
                {'count': 5, 'result': 'multiple_reuse', 'message': '다중 사용 위험'}
            ]
            
            # Simulate based on code
            if 'TEST' in code or '999' in code:
                scenario = usage_scenarios[2]  # Multiple reuse
            elif code.endswith(('7', '8', '9')):
                scenario = usage_scenarios[1]  # Potential reuse  
            else:
                scenario = usage_scenarios[0]  # First use
                
            response = {
                'status': 'success',
                'message': scenario['message'],
                'product_id': code,
                'usage_count': scenario['count'],
                'scan_result': scenario['result'],
                'scan_time': datetime.datetime.now().isoformat(),
                'safety_level': scenario['result']
            }
        else:
            response = {'status': 'error', 'message': '유효하지 않은 QR 코드입니다'}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8')) 
