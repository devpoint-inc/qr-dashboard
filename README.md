# �� Smart Chopstick QR Dashboard

QR 코드 기반 스마트 젓가락 안전성 추적 시스템

## ✨ 주요 기능

- **🔍 QR 코드 스캔**: 제품 안전성 즉시 확인
- **⚠️ 재사용 감지**: 3단계 안전성 알림 (안전/경고/위험)
- **📊 관리자 대시보드**: 제품 등록 및 통계 관리
- **🌐 반응형 디자인**: 모바일/데스크톱 최적화
- **🇰🇷 한국어 지원**: 완전한 한국어 인터페이스

## 🚀 Vercel 배포 방법

### 1. GitHub 저장소 생성
```bash
# 새 저장소 생성
git init
git add .
git commit -m "Smart Chopstick QR Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qr-dashboard.git
git push -u origin main
```

### 2. Vercel 배포
1. [Vercel 웹사이트](https://vercel.com) 접속
2. GitHub 계정으로 로그인
3. "New Project" 클릭
4. `qr-dashboard` 저장소 선택
5. "Deploy" 클릭
6. 배포 완료!

### 3. 접속 URL
- **메인 페이지**: `https://your-project.vercel.app/api/`
- **관리자**: `https://your-project.vercel.app/api/admin`

## 💻 로컬 개발

```bash
# 프로젝트 클론
git clone https://github.com/YOUR_USERNAME/qr-dashboard.git
cd qr-dashboard

# 서버리스 함수 테스트 (로컬)
python api/index.py

# 접속 테스트
# 메인: http://localhost:5000/api/
# 관리자: http://localhost:5000/api/admin
```

## 📋 API 엔드포인트

- `GET /api/` - 메인 QR 스캐너 페이지
- `GET /api/admin` - 관리자 대시보드  
- `GET /api/scan?code=<qr_code>` - QR 코드 스캔
- `POST /api/products` - 새 제품 생성 (데모)
- `GET /api/statistics` - 시스템 통계 (데모)

## 🛠️ 기술 스택

- **Backend**: Python Serverless Functions
- **Database**: 시뮬레이션 (데모 버전)
- **Frontend**: HTML/CSS/JavaScript (Embedded)
- **Deploy**: Vercel Serverless Functions

## 📱 사용 방법

### 소비자 (QR 스캔)
1. 메인 페이지 접속 (`/api/`)
2. QR 코드 입력 (예: `SKC-123`)
3. 안전성 결과 확인:
   - ✅ **안전** (최초 사용)
   - ⚠️ **경고** (재사용 의심) 
   - ❌ **위험** (다회 사용)

### 관리자 (제품 관리)
1. `/api/admin` 페이지 접속
2. 새 제품 등록 (데모)
3. QR 코드 자동 생성 (시뮬레이션)
4. 실시간 통계 확인

## 🔒 보안 기능

- IP 주소 로깅
- 사용자 에이전트 추적
- 재사용 패턴 분석
- 서버리스 환경 보안

## 📊 통계 정보

- 총 제품 수
- 사용된 제품 수  
- 재사용 감지 건수
- 최근 24시간 스캔 수

## 🎯 데모 테스트

### QR 코드 테스트
- `SKC-123` → 안전 (최초 사용)
- `SKC-456` → 안전 (최초 사용)  
- `ABC-123` → 오류 (유효하지 않은 코드)

---

**개발자**: Smart Chopstick Team  
**버전**: 4.0 (Pure Serverless Functions)  
**배포**: Vercel Serverless  
**저장소**: [qr-dashboard](https://github.com/YOUR_USERNAME/qr-dashboard) 