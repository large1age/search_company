# Search Company

Updated: 2024-08-28

## Summary
* 해당 기술 과제에 대한 기능 구현 코딩은 개발의 편의성을 위해서 Flask 및 SQLite3를 이용해서 로컬 환경을 기준으로 개발했습니다.
* 회사와 회사 지사 정보를 1:N, 회사와 회사 태그 정보를 1:N 구조로 개발했습니다. 
  - 개발이 80% 이상 진행하고, 세부적인 테스트 코드를 봤을 때 회사와 태그 그룹이 1:N, 태그 그룹과 태그가 1:N구조로 되어야 한다는 사실을 알게 되었지만 제한된 기간 내의 설계를 바꿀 수 없어서 초기 설계대로 개발하고, 삭제 API 관련 테스트 코드의 결과값을 다르게 수정했습니다.) 
  - 과제 정보에 태그 그룹에 대한 요구사항에 대해 좀더 명시적으로 안내되었으면 하는 바램이 있습니다. 
* CSV에 원티드 정보가 없는 관게로 유닛 테스트에서 원티드에 대한 테스트 대신 다른 회사의 정보로 테스트 코드를 변경해서 진행했습니다.

## 디렉토리 구조
* application : 어플리케이션 코드 관리
  - models: ORM 정의
  - repositories: ORM을 통한 영속성 관리
  - service
    - 디렉토리
      - units : 서비스 함수의 인자 및 결과값에 대한 DTO 모음
      - services : models, repositories, units에 의존하여 기능 구현
    - 파일
      - usecase.py : 서비스 레이어의 External Interface
      - ports.py : usecase 함수의 인자 및 결과값에 대한 DTO 모음
  - routes.py : API 엔드포인트 관리 (개발 편의를 위해 함수로만 구현)
* tests : 유닛 테스트 관리

## 실행 방법
* 공통 : pip / pipenv를 통한 의존성 설치 및 파이썬 가상환경 ON
* 유닛 테스트 (CSV 데이터의 마이그레이션 포함)
    - python unit_test.py
* 서버 실행 (CSV 데이터의 마이그레이션 포함)
    - python bootstrap.py
