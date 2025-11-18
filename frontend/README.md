# Frontend

React + Material UI 기반의 단일 페이지 뉴스 조회 화면입니다.  
날짜 기반으로 수집된 뉴스의 토픽 목록과 요약을 제공합니다.

---

## 디렉토리 구조

```
frontend/
├── src/
│ └── App.js
└── public/
```

---

## 주요 기능
- 날짜 선택 DatePicker
- 해당 날짜의 뉴스 조회
- Anchor 기사 + 관련 뉴스 리스트
- 반응형 Material UI 구성

## 개발 실행
```
npm install
npm run start
```

## 기술 스택
- React
- Material UI
- Axios

## 설계 포인트
- 백엔드 API 스키마에 맞춘 단순/명확한 UI 구조
- 비동기 처리·데이터 캐싱 최소화로 경량화
- Material UI의 재사용 가능한 UI 컴포넌트 활용

## Screenshots
![news-browsing](/docs/screenshots/news-browsing.png)
