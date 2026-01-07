"""
LG Composite Prompt Suite v5.9.0 - Prompt Loader
각 Step별 md 파일들을 읽어서 시스템 프롬프트로 조합
"""

import os
import re

# 현재 파일 기준 prompts 폴더 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

# HTML 코멘트 제거 패턴
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)

# 각 Step별 프롬프트 파일 순서
STEP1_FILES = [
    "00_core_contract.md",
    "10_cast_variation_engine.md",
    "20_world_style_output.md",
]

STEP2_FILES = [
    "00_step2_core_rules.md",
    "10_step2_logic_physics.md",
    "20_step2_output_handoff_qa.md",
]

STEP3_FILES = [
    "00_step3_compose_rules.md",
    "10_step3_output_templates.md",
    "20_step3_userflow_qa_advanced.md",
]


def load_prompt_file(step_folder: str, filename: str) -> str:
    """단일 프롬프트 파일 로드 및 정리"""
    filepath = os.path.join(PROMPTS_DIR, step_folder, filename)
    
    if not os.path.exists(filepath):
        return ""
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # HTML 코멘트 제거
    content = HTML_COMMENT_PATTERN.sub("", content)
    
    # 앞뒤 공백 정리
    content = content.strip()
    
    return content


def load_step_prompt(step: int) -> str:
    """특정 Step의 시스템 프롬프트 로드"""
    if step == 1:
        folder = "step1"
        files = STEP1_FILES
    elif step == 2:
        folder = "step2"
        files = STEP2_FILES
    elif step == 3:
        folder = "step3"
        files = STEP3_FILES
    else:
        return f"Invalid step: {step}"
    
    parts = []
    for filename in files:
        content = load_prompt_file(folder, filename)
        if content:
            parts.append(content)
    
    if not parts:
        return f"LG Composite Prompt Suite v5.9.0 - Step {step} prompt files not found"
    
    return "\n\n---\n\n".join(parts)


def get_version() -> str:
    """시스템 버전 반환"""
    return "5.9.0"


# 메인 export
STEP1_SYSTEM_PROMPT = load_step_prompt(1)
STEP2_SYSTEM_PROMPT = load_step_prompt(2)
STEP3_SYSTEM_PROMPT = load_step_prompt(3)
SYSTEM_VERSION = get_version()


if __name__ == "__main__":
    print(f"=== LG Composite Prompt Suite v{SYSTEM_VERSION} ===")
    print(f"Step 1 prompt length: {len(STEP1_SYSTEM_PROMPT)} chars")
    print(f"Step 2 prompt length: {len(STEP2_SYSTEM_PROMPT)} chars")
    print(f"Step 3 prompt length: {len(STEP3_SYSTEM_PROMPT)} chars")
