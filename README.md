# 병원 가격 투명성 프로토타입 (price-monitor)

## 프로젝트 소개

모두닥 지원을 준비하면서 "병원 가격 모니터링은 결국 백엔드·자동화 문제"라는 생각이 들었고, 그 가설을 말로만 하는 대신 직접 확인해보려고 만든 프로토타입입니다.

핵심 아이디어는 단순합니다. 병원이 게시하는 가격(`listed_price`)과 플랫폼이 보장하는 가격(`guaranteed_price`)을 데이터로 쌓아두면,

- 소비자에게는 치료항목별 가격 비교(최저가 포함)를 자동으로 제공할 수 있고,
- 운영자에게는 "게시가가 보장가를 초과한 병원" 목록을 사람이 일일이 확인하지 않아도 API 한 번으로 뽑아낼 수 있습니다.

즉, 가격 투명성은 크롤링/입력 파이프라인 위에 올라간 조회·비교·감시 API의 문제이고, 이 저장소는 그중 API 레이어를 최소 형태로 구현한 것입니다.

## 만든 과정

Java/Spring 백엔드 경험을 바탕으로, Claude Code를 활용해 Django를 처음 접한 상태에서 약 3시간 만에 완성했습니다. Spring의 Entity–Repository–Controller 구조가 Django의 Model–ORM–ViewSet에 대응된다는 것을 확인하며 진행했고, Spring에서 fetch join으로 N+1 문제를 해결해본 경험을 살려 조회 시 select_related를 적용했습니다. 백엔드 기본기가 있으면 프레임워크 전환은 빠르다는 가설을 직접 검증한 결과물입니다.

## 기술 스택

- Python / Django 6.0
- Django REST Framework 3.17
- SQLite (개발용 기본 DB)

## API 명세

Base URL: `http://127.0.0.1:8000`

### 1. 병원 CRUD — `/api/hospitals/`

| 메서드      | 경로                   | 설명      |
| ----------- | ---------------------- | --------- |
| GET         | `/api/hospitals/`      | 병원 목록 |
| POST        | `/api/hospitals/`      | 병원 생성 |
| GET         | `/api/hospitals/{id}/` | 병원 상세 |
| PUT / PATCH | `/api/hospitals/{id}/` | 병원 수정 |
| DELETE      | `/api/hospitals/{id}/` | 병원 삭제 |

요청/응답 필드: `id`, `name`, `region`

### 2. 치료 가격 CRUD — `/api/prices/`

| 메서드      | 경로                | 설명      |
| ----------- | ------------------- | --------- |
| GET         | `/api/prices/`      | 가격 목록 |
| POST        | `/api/prices/`      | 가격 등록 |
| GET         | `/api/prices/{id}/` | 가격 상세 |
| PUT / PATCH | `/api/prices/{id}/` | 가격 수정 |
| DELETE      | `/api/prices/{id}/` | 가격 삭제 |

요청 필드: `hospital`(병원 id), `treatment_name`, `listed_price`, `guaranteed_price`
응답에는 `hospital_name`이 추가로 포함됩니다.

### 3. 가격 비교 — `GET /api/compare/?treatment=라식`

해당 치료항목의 가격을 `listed_price` 오름차순으로 정렬해 반환하고, 최저가 항목에 `is_lowest: true`를 표시합니다.

```json
{
  "treatment": "라식",
  "count": 3,
  "lowest_price": 1650000,
  "results": [
    {
      "hospital": "굿아이안과",
      "region": "부산 해운대",
      "treatment_name": "라식",
      "listed_price": 1650000,
      "guaranteed_price": 1900000,
      "is_lowest": true
    }
  ]
}
```

`treatment` 파라미터가 없으면 400을 반환합니다.

### 4. 가격 모니터링 — `GET /api/monitor/`

`listed_price > guaranteed_price`인 항목(보장가 위반)을 초과액과 함께 반환합니다.

```json
{
  "count": 5,
  "results": [
    {
      "hospital": "굿아이안과",
      "treatment_name": "라섹",
      "listed_price": 1750000,
      "guaranteed_price": 1500000,
      "excess": 250000
    }
  ]
}
```

## 실행 방법

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

실행 후 브라우저에서 `http://127.0.0.1:8000/api/`로 접속하면 DRF Browsable API로 전체 엔드포인트를 확인할 수 있습니다.
