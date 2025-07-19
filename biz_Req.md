# 📝 이슬처럼 풋살 매니지먼트 시스템 요구사항 정의서

## 📌 프로젝트 개요

**프로젝트명:**  
이슬처럼 풋살 매니지먼트 시스템

**핵심 목표:**  
- 풋살 동호회 경기 및 선수 기록의 시스템화 및 자동화
- 운영자 수작업 감소
- 기록과 통계 공유
- 향후 AI 추천 및 예측 기능 확장 고려

---

## 🧩 주요 기능

✅ 선수 관리
- 선수 등록 및 수정

✅ 경기 관리
- Match 생성, Game 생성 및 기록 관리

✅ MOM 투표 관리
- 경기별 Man of the Match 투표 기능

✅ 기록 관리
- 시즌별, 전체 통계 조회
- 경기 동영상 링크 관리

✅ 인증 및 보안
- SNS(카카오) 인증 로그인
- OAuth2 + JWT 기반 API 인증

---

## 🗂️ 주요 엔티티

- **Player** (선수)
- **Season** (시즌)
- **Match** (경기일)
- **Game** (팀 간 경기)
- **Team** (경기별 팀)
- **GameRecord** (게임 기록)
- **MOM** (MOM 투표)
- **AwardHistory** (수상 기록)
- **PersonalStat** (선수별 통계)

---

## 🔒 권한/역할 정의

**운영자 (Admin)**
- 전체 데이터 관리
- 선수, 경기, 기록, MOM 관리

**선수 (Player)**
- 본인 기록 열람
- MOM 투표

---

## 🏛️ 아키텍처

| 구성요소       | 기술 스택                       |
|----------------|--------------------------------|
| **Frontend**   | Vue 3                          |
| **Backend**    | FastAPI + OAuth2 + JWT        |
| **DB**         | Supabase PostgreSQL           |
| **Storage**    | Supabase Storage              |
| **배포**       | Docker Compose                |

---

## 🌐 API 설계

- RESTful API
- Swagger / OpenAPI 문서화
- JWT 인증
- 카카오 SNS 로그인 연계

---

## 🧾 향후 고려사항

- AI 추천 기능 (선수 매칭, 포지션 추천)
- 경기 예측 모델
- 고도화된 통계 대시보드
- Slack/카카오톡 알림 연동

---

## ✨ 특이사항 및 결정사항

- MOM 투표 24시간 제한은 제외
- SNS 인증은 카카오로 사용
- Supabase DB와 Storage 채택
- 메뉴/화면은 선수용, 운영자용 메뉴 분리 설계

---

## 📋 버전 관리 및 배포

- GitHub 저장소: [https://github.com/AdamssJung/futsalon](https://github.com/AdamssJung/futsalon)
- Docker Compose 기반 배포
- 환경 변수 관리 `.env`

---

## 📅 개발 단계 (로드맵)

1. 프로젝트 환경 세팅 (Git, Docker, FastAPI)
2. Supabase DB 테이블 생성
3. SQLAlchemy 모델 작성
4. CRUD API 구현
5. JWT 인증 연동
6. Vue3 프론트엔드 구성
7. 통합 테스트 및 베타 배포
8. AI 및 통계 기능 고도화

---