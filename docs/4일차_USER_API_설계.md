초기 요구사항 정의서를 기반으로 설계한 **유저 및 인증 관리 API 명세서**입니다. 마크다운(MD) 파일 형식으로 정밀하게 작성되어 개발 실무에 바로 활용하실 수 있습니다.

이 명세서는 RESTful 프린시플을 준수하며, JWT 보안 규칙(`http_only` 쿠키, `Authorization` 헤더 등)과 부분 수정(Partial Update, `PATCH`) 요구사항을 명밀하게 반영했습니다.

---

# 유저 및 인증 관리 API 명세서 (User & Authentication API Specification)

## 1. 공통 사항

* **Base URL**: `https://api.chest-xray.internal/v1`
* **Content-Type**: `application/json`
* **인증 방식**: HTTP Bearer Authentication (JWT 엑세스 토큰)
* 로그인/재발급을 제외한 모든 API는 Header에 `Authorization: Bearer {Access Token}`을 포함해야 합니다.


* **공통 에러 응답**:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "에러에 대한 상세한 설명문구",
    "target": "필드 에러인 경우 해당 필드명 (Optional)"
  }
}

```



---

## 2. API 요약 정의

| 기능 구분 | 요구사항 ID | HTTP Method | URI | 기능 요약 | 권한 |
| --- | --- | --- | --- | --- | --- |
| **인증/유저** | REQ-USER-001 | `POST` | `/auth/signup` | 회원가입 | 전체 (비로그인) |
| **인증/유저** | REQ-USER-002 | `POST` | `/auth/login` | 로그인 (JWT 발급) | 전체 (비로그인) |
| **인증/유저** | NFR-USER-001 | `POST` | `/auth/refresh` | 토큰 재발급 | 전체 (Cookie 사용) |
| **인증/유저** | REQ-USER-003 | `POST` | `/auth/logout` | 로그아웃 | 로그인 유저 |
| **마이페이지** | REQ-USER-006 | `GET` | `/users/me` | 본인 정보 조회 | 로그인 유저 |
| **마이페이지** | REQ-USER-007 | `PATCH` | `/users/me` | 본인 정보 수정 (Partial) | 로그인 유저 |
| **마이페이지** | REQ-USER-008 | `PUT` | `/users/me/password` | 비밀번호 변경 | 로그인 유저 |
| **마이페이지** | REQ-USER-009 | `DELETE` | `/users/me` | 회원 탈퇴 (즉시 삭제) | 로그인 유저 |
| **어드민** | REQ-USER-004 | `GET` | `/admin/users` | 회원 목록 조회 (검색/필터) | 어드민 (`Admin`) |
| **어드민** | REQ-USER-005 | `PATCH` | `/admin/users/roles` | 회원 권한 일괄 변경 | 어드민 (`Admin`) |

---

## 3. 상세 API 명세

### 3.1 회원가입 (REQ-USER-001)

* **Description**: 사내 의료인, 연구진, 개발 실무진이 서비스를 이용하기 위해 계정을 등록합니다.
* **Method & Path**: `POST` `/auth/signup`
* **Authentication**: None
* **Request Body**:
```json
{
  "email": "developer01@company.com",
  "password": "Password123!",
  "name": "홍길동",
  "department": "개발", 
  "gender": "M",
  "phone_number": "010-1234-5678"
}

```


* `department`: `연구`, `의료`, `개발` 중 택일
* `gender`: `M` (남성) 또는 `F` (여성)


* **Response (201 Created)**:
```json
{
  "success": true,
  "message": "회원가입이 완료되었습니다. 관리자 승인 후 서비스 이용이 가능합니다."
}

```



---

### 3.2 로그인 (REQ-USER-002, NFR-USER-001)

* **Description**: 이메일과 비밀번호를 검증하여 JWT Access Token과 Refresh Token을 발급합니다.
* **Method & Path**: `POST` `/auth/login`
* **Authentication**: None
* **Request Body**:
```json
{
  "email": "developer01@company.com",
  "password": "Password123!"
}

```


* **Response (200 OK)**:
* **Set-Cookie (Response Header)**: `refresh_token={JWT}; Max-Age=604800; HttpOnly; Secure; SameSite=Strict` (클라이언트 스크립트 접근 불가)
* **Response Body**:
```json
{
  "success": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}

```


* `access_token` 페이로드에는 최소 식별 정보인 `user_id`만 포함됩니다.
* `expires_in`: 만료 주기 (30분 = 1800초)





---

### 3.3 토큰 재발급 (NFR-USER-001)

* **Description**: Access Token이 만료된 경우, Cookie에 저장된 Refresh Token을 검증하여 새로운 Access Token을 발급합니다.
* **Method & Path**: `POST` `/auth/refresh`
* **Authentication**: Cookie 기반 (`refresh_token`)
* **Request Body**: None
* **Response (200 OK)**:
```json
{
  "success": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}

```


* **Error Response (401 Unauthorized)**:
* 리프레시 토큰이 만료되었거나 변조된 경우, 재로그인을 유도합니다.



---

### 3.4 로그아웃 (REQ-USER-003)

* **Description**: 현재 세션을 종료하고 발급된 토큰을 무효화합니다. 클라이언트는 로그아웃 성공 후 로그인 페이지로 전환되어야 합니다.
* **Method & Path**: `POST` `/auth/logout`
* **Authentication**: Required (`Bearer Access Token`)
* **Request Body**: None
* **Response (200 OK)**:
* **Set-Cookie (Response Header)**: `refresh_token=; Max-Age=0; HttpOnly; ...` (쿠키 삭제)


```json
{
  "success": true,
  "message": "로그아웃 되었습니다."
}

```



---

### 3.5 마이페이지 조회 (REQ-USER-006)

* **Description**: 로그인된 유저가 본인의 프로필 및 권한 상태를 조회합니다.
* **Method & Path**: `GET` `/users/me`
* **Authentication**: Required (`Bearer Access Token`)
* **Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "name": "홍길동",
    "email": "developer01@company.com",
    "department": "개발",
    "gender": "M",
    "phone_number": "010-1234-5678",
    "role": "스태프"
  }
}

```


* `role`: `대기자`, `스태프`, `어드민` 중 하나



---

### 3.6 회원 정보 수정 (REQ-USER-007)

* **Description**: 마이페이지에서 본인의 부서 또는 휴대폰 번호를 부분 수정(Partial Update)합니다.
* **Method & Path**: `PATCH` `/users/me`
* **Authentication**: Required (`Bearer Access Token`)
* **Request Body** (변경을 원하는 필드만 선택하여 전송 가능):
```json
{
  "department": "연구",
  "phone_number": "010-9876-5432"
}

```


* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "회원 정보가 성공적으로 수정되었습니다.",
  "data": {
    "department": "연구",
    "phone_number": "010-9876-5432"
  }
}

```



---

### 3.7 비밀번호 변경 (REQ-USER-008)

* **Description**: 마이페이지에서 기존 비밀번호 일치 여부를 검증한 후, 신규 비밀번호로 변경합니다.
* **Method & Path**: `PUT` `/users/me/password`
* **Authentication**: Required (`Bearer Access Token`)
* **Request Body**:
```json
{
  "old_password": "Password123!",
  "new_password": "NewPassword567!"
}

```


* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "비밀번호가 안전하게 변경되었습니다."
}

```


* **Error Response (400 Bad Request)**: 기존 비밀번호가 일치하지 않는 경우 에러를 반환합니다.

---

### 3.8 회원 탈퇴 (REQ-USER-009)

* **Description**: 본인 계정을 즉시 탈퇴 처리하며, 데이터베이스 내 유저와 연관된 데이터를 즉시 영구 삭제(Hard Delete)합니다.
* **Method & Path**: `DELETE` `/users/me`
* **Authentication**: Required (`Bearer Access Token`)
* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "회원 탈퇴가 완료되었으며, 개인정보가 즉시 삭제되었습니다."
}

```



---

### 3.9 어드민 - 회원 목록 조회 (REQ-USER-004)

* **Description**: 관리자가 가입된 전체 회원을 목록 조회하며, 검색 및 부서별 필터링을 지원합니다.
* **Method & Path**: `GET` `/admin/users`
* **Authentication**: Required (`Admin` 권한 필수)
* **Query Parameters**:
* `search`: 검색어 (이메일 혹은 이름 매칭, Optional)
* `department`: 부서 필터 (`연구`, `의료`, `개발`, Optional)
* `page`: 페이지 번호 (Default: 1, Optional)
* `limit`: 페이지당 로우 수 (Default: 20, Optional)


* **Example Request**: `/admin/users?search=홍길동&department=개발`
* **Response (200 OK)**:
```json
{
  "success": true,
  "total_count": 1,
  "page": 1,
  "limit": 20,
  "data": [
    {
      "user_id": "usr_82319481",
      "email": "developer01@company.com",
      "name": "홍길동",
      "department": "개발",
      "gender": "M",
      "phone_number": "010-1234-5678",
      "is_active": true,
      "role": "스태프"
    }
  ]
}

```



---

### 3.10 어드민 - 회원 권한 변경 (REQ-USER-005)

* **Description**: 관리자가 선택한 회원들의 서비스 접근 권한을 대기자, 스태프, 어드민 중 하나로 일괄 변경합니다.
* **Method & Path**: `PATCH` `/admin/users/roles`
* **Authentication**: Required (`Admin` 권한 필수)
* **Request Body**:
```json
{
  "user_ids": ["usr_82319481", "usr_99182311"],
  "target_role": "스태프"
}

```


* `target_role`: `대기자`, `스태프`, `어드민` 중 택일


* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "선택한 유저의 권한이 '스태프'로 변경되었습니다.",
  "updated_count": 2
}

```



---

## 4. 비기능적 요구사항(NFR) 이행 표준 안내

### 4.1 비밀번호 입력 보안 (NFR-USER-002)

* 본 요구사항은 **프론트엔드(Client Side) UI 구현 사항**입니다.
* 모든 패스워드 입력 폼(`input`)은 기본 `type="password"` 설정을 통해 마스킹 처리해야 하며, 눈 모양 토글 아이콘을 배치하여 `type="text"`로 유동 전환할 수 있도록 구현되어야 합니다.

### 4.2 성능 및 가용성 기준 (NFR-USER-003)

* **Back-end SLA**: 위 명세서에 정의된 모든 유저 API 인프라는 비즈니스 로직 처리 및 DB I/O를 포함하여 **최대 3초(3,000ms) 이내**에 클라이언트에 HTTP 응답을 반환(E2E Latency)하는 것을 보장하도록 설계 및 인덱싱되어야 합니다.

### 4.3 인가 상세 정책 (REQ-USER-005 비고 참조)

* **대기자**: 마이페이지(`GET/PATCH/PUT/DELETE /users/me`) 이외의 흉부 X-Ray 진단 및 어드민 기능 전면 접근 불가 (`403 Forbidden` 처리)
* **스태프**: 흉부 X-ray 서비스 관련 모든 Read/Write/Update 권한 허용, 어드민 기능 접근 불가
* **어드민**: 시스템 관리자로서 모든 API 데이터 엑세스 및 회원 관리 기능 수행 가능