# News Bot  
**키워드 기반 일간 뉴스 자동 수집 · 중복 제거 · 토픽 분류 · 조회 서비스**

본 프로젝트는 매일 반복되는 뉴스 선별·정리 업무를 자동화하기 위해 개발된 **엔드투엔드 뉴스 수집·분류·조회·발송 플랫폼**입니다.  
백엔드는 FastAPI + SQLite 기반의 경량 API 서버로 구성되며, 뉴스 수집 파이프라인은 Sentence Transformer와 코사인 유사도를 이용해 중복 뉴스를 제거하고 토픽 단위로 앵커링합니다.  
프론트엔드는 React 기반의 단일 페이지로 날짜별·토픽별 뉴스를 조회할 수 있습니다.

---

## 주요 기능

### 1. 뉴스 수집 및 중복 제거 (Collector)
- Naver News API를 사용한 키워드 기반 뉴스 수집
- Sentence Transformer 임베딩 기반 코사인 유사도 중복 제거
- 대표 뉴스를 앵커로 선정 후 토픽별 클러스터링
- Collector 주기 실행 가능 (cron / workflow 연동 가능)
- 슬랙 채널에 뉴스 요약 전송

### 2. 뉴스 조회 API (FastAPI)
- 날짜별·토픽별 뉴스 조회 API 제공
- SQLAlchemy ORM 기반
- SQLite 경량 DB 사용
- Swagger UI 및 Redoc 기반 API 문서 자동 생성

### 3. React 기반 프론트엔드
- Material UI 기반의 간결한 UI
- 날짜 선택 → 해당 날짜의 토픽 목록 → 뉴스 상세
- API 서버와 완전 분리된 SPA 구조

### 4. Dev Container 기반 개발 환경
- Docker + DevContainer로 Python 백엔드와 Node 프론트 템플릿 자동 세팅
- 팀/개인 환경 차이를 제거하며 reproducible 개발 가능

---

## 🏛 전체 아키텍처
```
              ┌────────────┐
              │  frontend  │  React SPA
              └──────┬─────┘
                     │ REST
                     ▼
            ┌─────────────────┐
            │   FastAPI App   │
            │  (src/app)      │
            └──────┬──────────┘
                   │ SQLAlchemy ORM
                   ▼
           ┌───────────────────┐
           │     SQLite DB     │
           └───────────────────┘

           (Batch / Cron)
           ┌───────────────────┐
           │  Collector (bot)  │
           │  src/collector    │
           └───────────────────┘
```
---

## 기술 스택

### Backend
- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Sentence Transformers
- Naver News API
- Slack API
- DevContainer / Docker

### Frontend
- React
- Material UI

### Infra / Tooling
- DevContainer
- Docker
- uv / pip / npm

---

## 로컬 실행 방법

### 1. Dev Container로 실행 (권장)
VS Code → `Reopen in Container`  
백엔드 + 프론트엔드 개발 환경 자동 세팅.

### 2. 백엔드 실행
```bash
# collector
python -m src.collectors.news_collector

# api
uvicorn src.app.main:app --timeout-graceful-shutdown 30
```

### 3. 프론트엔드 실행
```
cd frontend
npm install
npm run dev
```

### 디렉토리 구조
```
project/
 ├── src/
 │   ├── app/            # FastAPI 엔트리포인트
 │   ├── collector/      # 뉴스 수집 및 토픽 분석
 │   ├── core/           # 설정, 공용 유틸
 │   ├── domain/         # 도메인 엔티티 모델
 │   ├── infra/          # 외부 API, DB 연결
 │   ├── models/         # SQLAlchemy 모델
 │   ├── repositories/   # 데이터 저장소 계층
 │   ├── services/       # 비즈니스 로직 계층
 │   └── ...
 ├── frontend/           # React SPA
 ├── .devcontainer/      # 개발환경 컨테이너
 ├── keywords.csv        # 뉴스 수집 키워드
 ├── logs/               # DEBUG 레벨 로그(실행 시 생성)
 ├── news.db             # SQLite DB(실행 시 생성)
 ├── .env                # 환경 변수 파일
 └── README.md
```

### .env 설정(필수)
```
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=
SLACK_WEBHOOK_URL=
CSV_FILE_PATH=keywords.csv
```

## 프로젝트 성과 및 지표
- 하루 평균 100건 기사 자동 수집
- 중복 제거 비율: 약 40~60%
- 토픽 분류 정확도: 임계값 0.45 기준 unknown 비율 ~20% 이하