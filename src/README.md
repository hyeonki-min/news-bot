# Backend + Collector

FastAPI 기반의 뉴스 조회 API와  
Sentence Transformer 기반의 뉴스 수집·중복제거·토픽 분류 파이프라인으로 구성된 백엔드입니다.

---

## 패키지 구조

```
src/
├── app/ # FastAPI 초기화 및 라우터
├── collector/ # 수집 + 중복 제거 + 토픽 분류
├── core/ # 공용 설정, 로깅, config
├── domain/ # 엔티티
├── infra/ # 외부 API, DB connector
├── models/ # SQLAlchemy ORM 모델
├── repositories/ # DB CRUD 추상화 계층
└── services/ # 비즈니스 로직
```
---

## 주요 컴포넌트

### `collector/` 뉴스 수집 및 토픽 분류
- **Naver News API** 다건 수집
- **Sentence Transformer 임베딩 생성**
- **코사인 유사도 기반 중복 뉴스 제거**
  - 코사인 유사도(Cosine Similarity)는 두 임베딩 벡터가 이루는 각도를 기반으로
    “의미적 유사성”을 측정하는 방식으로, 문장 길이와 상관없이 의미 비교에 적합하기 때문에
    NLP 분야에서 가장 널리 사용되는 유사도 지표입니다
- **대표 기사(Anchor) 선정 후 토픽 단위 분류**
  - Sentence Transformer 기반 토픽 분류 모델을 사용하며,
    각 토픽의 Anchor Embedding과 입력 문장의 유사도를 비교하는 방식으로 분류합니다.
    임베딩 생성에는 LRU Cache를 적용하여 성능을 최적화했습니다 
- 결과는 SQLite DB에 저장
- SLACK 채널에 전송

### 실행 예:
```bash
python -m src.collectors.news_collector
```

### `app/` 뉴스 조회 API
GET /api/news?date=2025-11-16
```
{
  [
    {
      "id": "1",
      "title": "쿠팡, 상품 회수없는 '셀프 환불' 도입…판매자는 블랙컨슈머 우...",
      "description": "쿠팡이 마켓플레이스(오픈마켓) 상품을 대상으로 회수하지 않고도 반품을 승인하는 '셀프 환불'...",
      "link": "https://",
      "topic": "logistics",
      "pub_date": "2025-11-16 14:48:00.000000"
    }
  ]
}
```

### ORM 모델
```
class NewsItemModel(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    link = Column(String)
    original_link = Column(String)
    pub_date = Column(DateTime)
    topic = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

```

### API 서버 실행
```
uvicorn src.app.main:app --timeout-graceful-shutdown 30
```

### 설계 포인트
- Domain Layer / Repository Layer / Service Layer를 분리하며 유지보수성을 확보
- Collector와 API 서버를 완전 분리하여 Batch / api 서비스 독립성 확보
- 임베딩 기반 뉴스 정제 → 임베딩 기반 토픽 분류
