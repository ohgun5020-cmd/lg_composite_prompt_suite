import streamlit as st
import google.generativeai as genai
import json
import re
import os
import hashlib
import time
from datetime import datetime

try:
    from prompt import STEP1_SYSTEM_PROMPT, STEP2_SYSTEM_PROMPT, STEP3_SYSTEM_PROMPT, SYSTEM_VERSION
    PROMPT_AVAILABLE = True
except ImportError:
    STEP1_SYSTEM_PROMPT = "Step 1 System Prompt Placeholder"
    STEP2_SYSTEM_PROMPT = "Step 2 System Prompt Placeholder"
    STEP3_SYSTEM_PROMPT = "Step 3 System Prompt Placeholder"
    SYSTEM_VERSION = "5.9.0"
    PROMPT_AVAILABLE = False

APP_TITLE = "LG Composite Prompt Suite"
APP_SUBTITLE = "Structured Prompt Generation Engine"

MODEL_OPTIONS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

MODEL_EXCLUDE_TOKENS = (
    "image", "audio", "tts", "native", "preview", "exp",
    "embedding", "gemma", "nano", "aqa", "imagen", "veo", "robotics",
)

# ═══════════════════════════════════════════════════════════════
# STEP 1 OPTIONS
# ═══════════════════════════════════════════════════════════════
REGION_OPTIONS = ["EU", "LATAM"]
REGION_LABELS = {"EU": "EU(유럽)", "LATAM": "LATAM(라틴아메리카)"}

CITY_OPTIONS = {
    "EU": ["Paris", "London", "Rome", "Barcelona", "Amsterdam", "Berlin", "Prague", "Vienna", "Madrid", "Florence"],
    "LATAM": ["Mexico City", "São Paulo", "Buenos Aires", "Rio de Janeiro", "Bogotá", "Lima", "Santiago"],
}

GENDER_OPTIONS = ["FEMALE", "MALE", "NON_BINARY"]
GENDER_LABELS = {"FEMALE": "여성", "MALE": "남성", "NON_BINARY": "논바이너리"}

ETHNICITY_OPTIONS = [
    "Caucasian", "East Asian", "African", "South Asian", "Southeast Asian",
    "Hispanic/Latino", "Middle Eastern", "Mixed",
]

CAST_MODE_OPTIONS = ["SINGLE", "MULTI"]
CAST_MODE_LABELS = {"SINGLE": "1명", "MULTI": "가족구성원"}

DIVERSITY_MODE_OPTIONS = ["SAFE", "FULL", "MATCH"]
DIVERSITY_MODE_LABELS = {"SAFE": "안전", "FULL": "최대", "MATCH": "지역 매칭"}

ASPECT_RATIO_OPTIONS = ["9:16", "16:9", "4:5", "1:1"]

# ═══════════════════════════════════════════════════════════════
# STEP 2 OPTIONS
# ═══════════════════════════════════════════════════════════════
HOUSING_TYPE_OPTIONS = ["STUDIO", "APARTMENT", "LOFT", "VILLA", "PENTHOUSE"]
HOUSING_TYPE_LABELS = {
    "STUDIO": "스튜디오 (20-35㎡)",
    "APARTMENT": "아파트 (60-90㎡)",
    "LOFT": "로프트 (80-120㎡)",
    "VILLA": "빌라 (150㎡+)",
    "PENTHOUSE": "펜트하우스 (150㎡+)",
}

INTERIOR_STYLE_OPTIONS = [
    "PARIS_STYLE", "LONDON_STYLE", "MILAN_STYLE", "BERLIN_STYLE",
    "SCANDI_STYLE", "VIENNA_STYLE", "MEDITERRANEAN_EU", "DUTCH_STYLE",
]
INTERIOR_STYLE_LABELS = {
    "PARIS_STYLE": "파리 스타일",
    "LONDON_STYLE": "런던 스타일",
    "MILAN_STYLE": "밀라노 스타일",
    "BERLIN_STYLE": "베를린 스타일",
    "SCANDI_STYLE": "스칸디나비안",
    "VIENNA_STYLE": "비엔나 스타일",
    "MEDITERRANEAN_EU": "지중해 스타일",
    "DUTCH_STYLE": "더치 스타일",
}

ROOM_TYPE_OPTIONS = ["Kitchen", "Living", "Bedroom", "Laundry", "Bathroom", "Study", "Dining"]

ENTROPY_LEVELS = {
    1: "극미니멀", 3: "미니멀", 5: "큐레이티드 ⭐", 7: "풍성함", 10: "맥시멀리스트",
}

OUTPUT_PRESET_OPTIONS = ["BASIC", "DETAIL_PLUS", "NEGATIVE_PLUS", "COMPOSITE_READY"]

# ═══════════════════════════════════════════════════════════════
# STEP 3 OPTIONS
# ═══════════════════════════════════════════════════════════════
PRODUCT_CATEGORY_OPTIONS = ["TV", "Refrigerator", "Washer", "Dryer", "Styler", "Air Purifier", "AC", "Oven"]
PRODUCT_CATEGORY_LABELS = {
    "TV": "TV / 디스플레이", "Refrigerator": "냉장고", "Washer": "세탁기",
    "Dryer": "건조기", "Styler": "스타일러", "Air Purifier": "공기청정기",
    "AC": "에어컨", "Oven": "오븐/레인지",
}

PRODUCT_LINE_OPTIONS = ["Objet", "Signature", "Standard"]
HAND_POLICY_OPTIONS = ["OFF", "SAFE", "ON"]
HAND_POLICY_LABELS = {"OFF": "OFF - 손 프레임아웃", "SAFE": "SAFE - 안전 ⭐", "ON": "ON - 완전 상호작용"}
TV_STATE_OPTIONS = ["OFF", "AMBIENT", "CONTENT"]
LOGO_MODE_OPTIONS = ["AUTO", "OFF", "ON"]
OUTPUT_MODE_OPTIONS = ["STANDARD", "THREE_PASS", "AB_TEST"]
GRID_ZONE_OPTIONS = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]

JSON_BLOCK_RE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def fingerprint_key(api_key):
    if not api_key:
        return ""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12]


def load_model_options(api_key):
    if not api_key:
        return MODEL_OPTIONS
    fingerprint = fingerprint_key(api_key)
    cached = st.session_state.get("model_options_cache", {})
    if cached.get("fingerprint") == fingerprint and cached.get("options"):
        return cached["options"]
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        options = []
        for model in models:
            name = getattr(model, "name", "")
            methods = getattr(model, "supported_generation_methods", []) or []
            if "generateContent" not in methods:
                continue
            if name.startswith("models/"):
                name = name.split("/", 1)[1]
            options.append(name)
        options = [o for o in options if o.startswith("gemini-") and not any(t in o for t in MODEL_EXCLUDE_TOKENS)]
        options = sorted(set(options)) or MODEL_OPTIONS
    except Exception:
        options = MODEL_OPTIONS
    st.session_state["model_options_cache"] = {"fingerprint": fingerprint, "options": options}
    return options


def get_chat_session(api_key, model_name, system_prompt, history=None):
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 16384,  # 증가
    }
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=system_prompt,
    )
    return model.start_chat(history=history or [])


def generate_with_retry(api_key, model_name, system_prompt, prompt, max_retries=2):
    """재시도 로직 포함 생성 함수"""
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 16384,
    }
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=system_prompt,
    )
    
    for attempt in range(max_retries + 1):
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            if attempt == max_retries:
                raise e
            time.sleep(2)  # 재시도 전 대기
            continue
    return None


def parse_json_from_response(text):
    for match in JSON_BLOCK_RE.finditer(text):
        candidate = match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def parse_json_input(json_text):
    if not json_text or not json_text.strip():
        return None, "JSON이 비어있습니다."
    try:
        match = JSON_BLOCK_RE.search(json_text)
        if match:
            json_text = match.group(1)
        return json.loads(json_text.strip()), None
    except json.JSONDecodeError as e:
        return None, f"JSON 파싱 오류: {e}"


# ═══════════════════════════════════════════════════════════════
# STREAMLIT CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.5rem;
        color: #7C3AED;
    }
    .main-header .subtitle {
        font-size: 0.85rem;
        color: #666;
    }
    .main-header .version {
        font-size: 0.75rem;
        color: #999;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 500;
    }
    .step-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .step-card h3 {
        margin-top: 0;
        color: #333;
    }
    .output-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .status-validated {
        background: #D1FAE5;
        color: #065F46;
    }
    .status-pending {
        background: #FEF3C7;
        color: #92400E;
    }
    .json-output {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.85rem;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
col_header, col_version = st.columns([4, 1])
with col_header:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #7C3AED, #A78BFA); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 1.2rem;">🎨</span>
        </div>
        <div>
            <h1 style="margin: 0; font-size: 1.4rem; color: #1f2937;">{APP_TITLE}</h1>
            <p style="margin: 0; font-size: 0.85rem; color: #6b7280;">{APP_SUBTITLE}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_version:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 8px;">
        <span style="font-size: 0.75rem; color: #9ca3af;">Config Version: </span>
        <span style="font-size: 0.75rem; color: #7C3AED; font-weight: 500;">{SYSTEM_VERSION}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# API KEY (간단히 상단에)
# ═══════════════════════════════════════════════════════════════
api_key = ""
if "GOOGLE_API_KEY" in st.secrets:
    api_key = str(st.secrets["GOOGLE_API_KEY"]).strip()
else:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()

if not api_key:
    st.error("❌ API Key가 없습니다. `.streamlit/secrets.toml`에 `GOOGLE_API_KEY`를 설정해주세요.")
    st.stop()

model_options = load_model_options(api_key)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
if "step1_output" not in st.session_state:
    st.session_state["step1_output"] = None
if "step2_output" not in st.session_state:
    st.session_state["step2_output"] = None
if "step3_output" not in st.session_state:
    st.session_state["step3_output"] = None

# 채팅 히스토리
if "step1_messages" not in st.session_state:
    st.session_state["step1_messages"] = []
if "step2_messages" not in st.session_state:
    st.session_state["step2_messages"] = []
if "step3_messages" not in st.session_state:
    st.session_state["step3_messages"] = []

# 채팅 세션
if "step1_chat" not in st.session_state:
    st.session_state["step1_chat"] = None
if "step2_chat" not in st.session_state:
    st.session_state["step2_chat"] = None
if "step3_chat" not in st.session_state:
    st.session_state["step3_chat"] = None

# ═══════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🎭 Step 1: Character", "🏠 Step 2: Interior", "📦 Step 3: Composite"])

# ═══════════════════════════════════════════════════════════════
# STEP 1: CHARACTER
# ═══════════════════════════════════════════════════════════════
with tab1:
    col_input1, col_output1 = st.columns([1, 1.2])
    
    with col_input1:
        st.markdown("### ① Model Character Setup")
        
        col_gender, col_age = st.columns(2)
        with col_gender:
            s1_gender = st.selectbox("GENDER", GENDER_OPTIONS, format_func=lambda x: GENDER_LABELS[x], key="s1_gender")
        with col_age:
            s1_age = st.selectbox("AGE GROUP", ["20s", "30s", "40s", "50s", "60s"], key="s1_age")
        
        s1_ethnicity = st.text_input("ETHNICITY", value="Korean", key="s1_ethnicity")
        
        col_region, col_city = st.columns(2)
        with col_region:
            s1_region = st.selectbox("REGION", REGION_OPTIONS, format_func=lambda x: REGION_LABELS[x], key="s1_region")
        with col_city:
            s1_city = st.selectbox("CITY", CITY_OPTIONS[s1_region], key="s1_city")
        
        s1_occupation = st.text_input("OCCUPATION", value="Gallery Curator", key="s1_occupation")
        
        col_cast, col_diversity = st.columns(2)
        with col_cast:
            s1_cast_mode = st.selectbox("CAST MODE", CAST_MODE_OPTIONS, format_func=lambda x: CAST_MODE_LABELS[x], key="s1_cast_mode")
        with col_diversity:
            s1_diversity = st.selectbox("DIVERSITY", DIVERSITY_MODE_OPTIONS, format_func=lambda x: DIVERSITY_MODE_LABELS[x], key="s1_diversity")
        
        s1_ratio = st.selectbox("ASPECT RATIO", ASPECT_RATIO_OPTIONS, index=2, key="s1_ratio")
        s1_model = st.selectbox("MODEL", model_options, key="s1_model")
        
        if st.button("🎨 Generate Step 1", type="primary", key="s1_generate"):
            prompt = f"""[SYSTEM_OVERRIDE_DATA]
Region: {s1_region}
City: {s1_city}
Fixed_Age: {s1_age}
Fixed_Gender: {s1_gender}
Fixed_Ethnicity: {s1_ethnicity}
Fixed_Occupation: {s1_occupation}
Cast_Mode: {s1_cast_mode}
Diversity_Mode: {s1_diversity}
Aspect_Ratio: {s1_ratio}

프롬프트를 생성해주세요.
"""
            st.session_state["step1_messages"].append({"role": "user", "content": f"설정: {s1_gender}, {s1_age}, {s1_ethnicity}, {s1_city}"})
            
            with st.spinner("Generating... (최대 60초 소요)"):
                try:
                    # 새 채팅 세션 시작
                    st.session_state["step1_chat"] = get_chat_session(api_key, s1_model, STEP1_SYSTEM_PROMPT)
                    response = st.session_state["step1_chat"].send_message(prompt)
                    result = response.text
                    
                    if result:
                        st.session_state["step1_output"] = result
                        st.session_state["step1_json"] = parse_json_from_response(result)
                        st.session_state["step1_messages"].append({"role": "assistant", "content": result})
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col_output1:
        st.markdown("### Generated Output & Chat")
        if st.session_state.get("step1_json"):
            st.markdown('<span class="status-badge status-validated">Schema Validated</span>', unsafe_allow_html=True)
        
        # 채팅 메시지 표시
        chat_container = st.container(height=450)
        with chat_container:
            for msg in st.session_state["step1_messages"]:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    with st.chat_message("assistant"):
                        content = msg["content"]
                        json_data = parse_json_from_response(content)
                        clean_text = JSON_BLOCK_RE.sub("", content).strip()
                        
                        # SET 패턴으로 분리
                        sets = re.split(r'(?=SET\s*\d+)', clean_text, flags=re.IGNORECASE)
                        sets = [s.strip() for s in sets if s.strip() and re.search(r'SET\s*\d+', s, re.IGNORECASE)]
                        
                        if sets:
                            st.markdown(f"**📸 {len(sets)}개 세트 생성됨**")
                            for i, set_content in enumerate(sets[:3]):  # 처음 3개만 미리보기
                                with st.expander(f"SET {i+1}", expanded=(i==0)):
                                    st.code(set_content[:500] + "..." if len(set_content) > 500 else set_content, language=None)
                            if len(sets) > 3:
                                st.caption(f"외 {len(sets)-3}개 세트...")
                        else:
                            st.markdown(clean_text[:800] + "..." if len(clean_text) > 800 else clean_text)
                        
                        if json_data:
                            with st.expander("📦 JSON (Step 2로 전달)"):
                                st.json(json_data)
        
        # 채팅 입력
        if s1_chat_input := st.chat_input("추가 지시 또는 수정 요청...", key="s1_chat_input"):
            if st.session_state.get("step1_chat") is None:
                st.session_state["step1_chat"] = get_chat_session(api_key, s1_model, STEP1_SYSTEM_PROMPT)
            
            st.session_state["step1_messages"].append({"role": "user", "content": s1_chat_input})
            
            with st.spinner("응답 중..."):
                try:
                    response = st.session_state["step1_chat"].send_message(s1_chat_input)
                    result = response.text
                    st.session_state["step1_messages"].append({"role": "assistant", "content": result})
                    
                    # JSON 있으면 업데이트
                    new_json = parse_json_from_response(result)
                    if new_json:
                        st.session_state["step1_json"] = new_json
                        st.session_state["step1_output"] = result
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# ═══════════════════════════════════════════════════════════════
# STEP 2: INTERIOR
# ═══════════════════════════════════════════════════════════════
with tab2:
    col_input2, col_output2 = st.columns([1, 1.2])
    
    with col_input2:
        st.markdown("### ② Interior Setup")
        
        # Step 1 데이터 자동 로드
        if st.session_state.get("step1_json"):
            st.success("✅ Step 1 데이터 자동 로드됨")
            s1_json = st.session_state["step1_json"]
        else:
            st.warning("⚠️ Step 1을 먼저 완료하세요")
            s1_json = None
        
        col_housing, col_style = st.columns(2)
        with col_housing:
            s2_housing = st.selectbox("HOUSING TYPE", HOUSING_TYPE_OPTIONS, format_func=lambda x: HOUSING_TYPE_LABELS[x], key="s2_housing")
        with col_style:
            s2_style = st.selectbox("INTERIOR STYLE", INTERIOR_STYLE_OPTIONS, format_func=lambda x: INTERIOR_STYLE_LABELS[x], key="s2_style")
        
        s2_rooms = st.multiselect("ROOM TYPES (4분할)", ROOM_TYPE_OPTIONS, default=["Kitchen", "Living", "Bedroom", "Laundry"], key="s2_rooms")
        
        s2_entropy = st.slider("ENTROPY LEVEL", 1, 10, 5, key="s2_entropy")
        st.caption(f"오브젝트 밀도: {ENTROPY_LEVELS.get(s2_entropy, '')}")
        
        s2_preset = st.selectbox("OUTPUT PRESET", OUTPUT_PRESET_OPTIONS, key="s2_preset")
        s2_model = st.selectbox("MODEL", model_options, key="s2_model")
        
        if st.button("🏠 Generate Step 2", type="primary", key="s2_generate"):
            prompt_lines = [
                "[STEP2_SETTINGS]",
                f"Housing_Type: {s2_housing}",
                f"Interior_Style: {s2_style}",
                f"Room_Types: {', '.join(s2_rooms)}",
                f"Entropy_Level: {s2_entropy}",
                f"Output_Preset: {s2_preset}",
            ]
            if s1_json:
                prompt_lines.append("")
                prompt_lines.append("[STEP1_JSON_BLOCK]")
                prompt_lines.append("```json")
                prompt_lines.append(json.dumps(s1_json, indent=2, ensure_ascii=False))
                prompt_lines.append("```")
            prompt_lines.append("")
            prompt_lines.append("인테리어 프롬프트를 생성해주세요.")
            
            st.session_state["step2_messages"].append({"role": "user", "content": f"설정: {s2_housing}, {s2_style}, {', '.join(s2_rooms)}"})
            
            with st.spinner("Generating... (최대 60초 소요)"):
                try:
                    st.session_state["step2_chat"] = get_chat_session(api_key, s2_model, STEP2_SYSTEM_PROMPT)
                    response = st.session_state["step2_chat"].send_message("\n".join(prompt_lines))
                    result = response.text
                    
                    if result:
                        st.session_state["step2_output"] = result
                        st.session_state["step2_json"] = parse_json_from_response(result)
                        st.session_state["step2_messages"].append({"role": "assistant", "content": result})
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col_output2:
        st.markdown("### Generated Output & Chat")
        if st.session_state.get("step2_json"):
            st.markdown('<span class="status-badge status-validated">Schema Validated</span>', unsafe_allow_html=True)
        
        # 채팅 메시지 표시
        chat_container = st.container(height=450)
        with chat_container:
            for msg in st.session_state["step2_messages"]:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    with st.chat_message("assistant"):
                        content = msg["content"]
                        json_data = parse_json_from_response(content)
                        clean_text = JSON_BLOCK_RE.sub("", content).strip()
                        
                        st.markdown(clean_text[:1000] + "..." if len(clean_text) > 1000 else clean_text)
                        
                        if json_data:
                            with st.expander("📦 JSON (Step 3로 전달)"):
                                st.json(json_data)
        
        # 채팅 입력
        if s2_chat_input := st.chat_input("추가 지시 또는 수정 요청...", key="s2_chat_input"):
            if st.session_state.get("step2_chat") is None:
                st.session_state["step2_chat"] = get_chat_session(api_key, s2_model, STEP2_SYSTEM_PROMPT)
            
            st.session_state["step2_messages"].append({"role": "user", "content": s2_chat_input})
            
            with st.spinner("응답 중..."):
                try:
                    response = st.session_state["step2_chat"].send_message(s2_chat_input)
                    result = response.text
                    st.session_state["step2_messages"].append({"role": "assistant", "content": result})
                    
                    new_json = parse_json_from_response(result)
                    if new_json:
                        st.session_state["step2_json"] = new_json
                        st.session_state["step2_output"] = result
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# ═══════════════════════════════════════════════════════════════
# STEP 3: COMPOSITE
# ═══════════════════════════════════════════════════════════════
with tab3:
    col_input3, col_output3 = st.columns([1, 1.2])
    
    with col_input3:
        st.markdown("### ③ Product Composite Setup")
        
        # Step 1/2 데이터 자동 로드
        s1_json = st.session_state.get("step1_json")
        s2_json = st.session_state.get("step2_json")
        
        if s1_json and s2_json:
            st.success("✅ Step 1 + Step 2 데이터 로드됨")
        elif s2_json:
            st.warning("⚠️ Step 1 데이터 없음")
        else:
            st.warning("⚠️ Step 1, 2를 먼저 완료하세요")
        
        st.markdown("**제품 정보**")
        s3_product_model = st.text_input("MODEL NAME", placeholder="예: LG Styler S5MBC", key="s3_product_model")
        
        col_cat, col_line = st.columns(2)
        with col_cat:
            s3_category = st.selectbox("CATEGORY", PRODUCT_CATEGORY_OPTIONS, format_func=lambda x: PRODUCT_CATEGORY_LABELS[x], key="s3_category")
        with col_line:
            s3_line = st.selectbox("PRODUCT LINE", PRODUCT_LINE_OPTIONS, key="s3_line")
        
        col_w, col_h, col_d = st.columns(3)
        with col_w:
            s3_width = st.number_input("W (mm)", value=445, key="s3_width")
        with col_h:
            s3_height = st.number_input("H (mm)", value=1850, key="s3_height")
        with col_d:
            s3_depth = st.number_input("D (mm)", value=585, key="s3_depth")
        
        s3_color = st.text_input("COLOR", value="Mist Beige", key="s3_color")
        
        col_room, col_grid = st.columns(2)
        with col_room:
            s3_room = st.selectbox("ROOM TYPE", ROOM_TYPE_OPTIONS, key="s3_room")
        with col_grid:
            s3_grid = st.selectbox("GRID ZONE", GRID_ZONE_OPTIONS, index=4, key="s3_grid")
        
        col_hand, col_logo = st.columns(2)
        with col_hand:
            s3_hand = st.selectbox("HAND POLICY", HAND_POLICY_OPTIONS, index=1, format_func=lambda x: HAND_POLICY_LABELS[x], key="s3_hand")
        with col_logo:
            s3_logo = st.selectbox("LOGO MODE", LOGO_MODE_OPTIONS, key="s3_logo")
        
        if s3_category == "TV":
            s3_tv_state = st.selectbox("TV STATE", TV_STATE_OPTIONS, key="s3_tv_state")
        else:
            s3_tv_state = "OFF"
        
        s3_model = st.selectbox("MODEL", model_options, key="s3_model")
        
        if st.button("📦 Generate Step 3", type="primary", key="s3_generate"):
            prompt_lines = [
                "[PRODUCT_DATA]",
                f"Model_Name: {s3_product_model}",
                f"Category: {s3_category}",
                f"Dimensions: W{s3_width} x H{s3_height} x D{s3_depth} mm",
                f"Color: {s3_color}",
                f"Line: {s3_line}",
                "",
                "[ROOM_TARGET]",
                f"Room_Type: {s3_room}",
                f"Grid_Zone: {s3_grid}",
                "",
                "[STEP3_SETTINGS]",
                f"Hand_Policy: {s3_hand}",
                f"TV_State: {s3_tv_state}",
                f"Logo_Mode: {s3_logo}",
            ]
            if s1_json:
                prompt_lines.append("")
                prompt_lines.append("[STEP1_JSON_BLOCK]")
                prompt_lines.append("```json")
                prompt_lines.append(json.dumps(s1_json, indent=2, ensure_ascii=False))
                prompt_lines.append("```")
            if s2_json:
                prompt_lines.append("")
                prompt_lines.append("[STEP2_JSON_BLOCK]")
                prompt_lines.append("```json")
                prompt_lines.append(json.dumps(s2_json, indent=2, ensure_ascii=False))
                prompt_lines.append("```")
            prompt_lines.append("")
            prompt_lines.append("5-SET 합성 프롬프트를 생성해주세요.")
            
            st.session_state["step3_messages"].append({"role": "user", "content": f"제품: {s3_product_model}, {s3_category}, {s3_color}"})
            
            with st.spinner("Generating 5-SET... (최대 90초 소요)"):
                try:
                    st.session_state["step3_chat"] = get_chat_session(api_key, s3_model, STEP3_SYSTEM_PROMPT)
                    response = st.session_state["step3_chat"].send_message("\n".join(prompt_lines))
                    result = response.text
                    
                    if result:
                        st.session_state["step3_output"] = result
                        st.session_state["step3_json"] = parse_json_from_response(result)
                        st.session_state["step3_messages"].append({"role": "assistant", "content": result})
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col_output3:
        st.markdown("### Generated Output & Chat")
        if st.session_state.get("step3_json"):
            st.markdown('<span class="status-badge status-validated">Schema Validated</span>', unsafe_allow_html=True)
        
        # 채팅 메시지 표시
        chat_container = st.container(height=450)
        with chat_container:
            for msg in st.session_state["step3_messages"]:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    with st.chat_message("assistant"):
                        content = msg["content"]
                        json_data = parse_json_from_response(content)
                        clean_text = JSON_BLOCK_RE.sub("", content).strip()
                        
                        # SET 분리
                        sets = re.split(r'(?=SET\s*\d+)', clean_text, flags=re.IGNORECASE)
                        sets = [s.strip() for s in sets if s.strip() and re.search(r'SET\s*\d+', s, re.IGNORECASE)]
                        
                        if sets:
                            st.markdown(f"**📦 5-SET ({len(sets)}개)**")
                            set_labels = {
                                "01": "LIFESTYLE 1-A", "02": "HERO 2-A", "03": "LIFESTYLE 1-B",
                                "04": "HERO 2-B", "05": "HERO 2-C",
                            }
                            for i, set_content in enumerate(sets):
                                match = re.search(r'SET\s*(\d+)', set_content, re.IGNORECASE)
                                set_num = match.group(1).zfill(2) if match else str(i+1).zfill(2)
                                label = set_labels.get(set_num, f"SET {set_num}")
                                with st.expander(f"SET {set_num} - {label}", expanded=(i==0)):
                                    st.code(set_content[:800] + "..." if len(set_content) > 800 else set_content, language=None)
                        else:
                            st.markdown(clean_text[:1000] + "..." if len(clean_text) > 1000 else clean_text)
                        
                        if json_data:
                            with st.expander("📦 JSON"):
                                st.json(json_data)
        
        # 채팅 입력
        if s3_chat_input := st.chat_input("추가 지시 또는 수정 요청...", key="s3_chat_input"):
            if st.session_state.get("step3_chat") is None:
                st.session_state["step3_chat"] = get_chat_session(api_key, s3_model, STEP3_SYSTEM_PROMPT)
            
            st.session_state["step3_messages"].append({"role": "user", "content": s3_chat_input})
            
            with st.spinner("응답 중..."):
                try:
                    response = st.session_state["step3_chat"].send_message(s3_chat_input)
                    result = response.text
                    st.session_state["step3_messages"].append({"role": "assistant", "content": result})
                    
                    new_json = parse_json_from_response(result)
                    if new_json:
                        st.session_state["step3_json"] = new_json
                        st.session_state["step3_output"] = result
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
col_reset, col_info = st.columns([1, 3])
with col_reset:
    if st.button("🗑️ Reset All", type="secondary"):
        keys_to_clear = [
            "step1_output", "step1_json", "step1_messages", "step1_chat",
            "step2_output", "step2_json", "step2_messages", "step2_chat",
            "step3_output", "step3_json", "step3_messages", "step3_chat",
        ]
        for key in keys_to_clear:
            st.session_state.pop(key, None)
        st.rerun()
with col_info:
    st.caption(f"LG Composite Prompt Suite v{SYSTEM_VERSION} | Powered by Gemini")
