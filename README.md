# LG Composite Prompt Suite v5.9.0

3-Step 통합 프롬프트 생성 시스템

## 개요

Step 1 (Character) → Step 2 (Interior) → Step 3 (Composite) 를 하나의 앱에서 순차적으로 실행하고, 각 Step의 출력이 다음 Step으로 자동 전달됩니다.

## 구조

```
lg_composite_prompt_suite_v5.9.0/
├── app.py                      # 통합 Streamlit 앱 (탭 3개)
├── prompt.py                   # 3개 Step 프롬프트 로더
├── prompts/
│   ├── step1/                  # Character 프롬프트
│   │   ├── 00_core_contract.md
│   │   ├── 10_cast_variation_engine.md
│   │   └── 20_world_style_output.md
│   ├── step2/                  # Interior 프롬프트
│   │   ├── 00_step2_core_rules.md
│   │   ├── 10_step2_logic_physics.md
│   │   └── 20_step2_output_handoff_qa.md
│   └── step3/                  # Composite 프롬프트
│       ├── 00_step3_compose_rules.md
│       ├── 10_step3_output_templates.md
│       └── 20_step3_userflow_qa_advanced.md
├── schemas/
│   ├── LG_Step1_Schema_v1_1.json
│   ├── LG_Step2_Schema_v1_1.json
│   └── LG_Step3_Input_Schema_v1_1.json
├── .streamlit/
│   └── secrets.toml            # API 키 설정
├── requirements.txt
├── check.py
└── .gitignore
```

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
streamlit run app.py
```

## API Key 설정

`.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "your-api-key-here"
```

## 워크플로우

### Step 1: Character
- 인물/캐스팅 프롬프트 생성
- 성별, 나이, 인종, 지역, 직업 등 설정
- 출력: 인물 프롬프트 + JSON

### Step 2: Interior
- Step 1 JSON 자동 로드
- 인테리어/배경 프롬프트 생성
- 주거 유형, 스타일, 룸 타입, 엔트로피 설정
- 출력: 외관 + 4분할 인테리어 프롬프트 + JSON

### Step 3: Composite
- Step 1 + Step 2 JSON 자동 로드
- 제품 합성 프롬프트 생성
- 제품 정보, Room Target, Hand Policy 등 설정
- 출력: 5-SET 합성 프롬프트

## 데이터 플로우

```
Step 1 완료 → JSON 저장 → Step 2에서 자동 로드
Step 2 완료 → JSON 저장 → Step 3에서 자동 로드
```

## 버전업 방법

`prompts/` 하위 폴더의 md 파일만 교체하면 자동 반영됨
