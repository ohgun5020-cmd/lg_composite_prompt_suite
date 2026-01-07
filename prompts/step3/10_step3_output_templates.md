# ═══════════════════════════════════════════════════════════════
# SECTION 6: OUTPUT STRUCTURE
# ═══════════════════════════════════════════════════════════════

## §6.0 RESOLUTION REALITY CHECK

```
생성은 모델 최대 지원 사이즈로 진행한다.
최종 8K는 타일링 업스케일 또는 2-pass로 달성한다.
```

---

## §6.1 STANDARD 5-SET OUTPUT ⭐FIXED

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 표준 5세트 구조
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SET 1 [LIFESTYLE 1-A]: Model + Product + Interior (Interaction)
SET 2 [HERO 2-A]: Product + Interior (Hero in context)
SET 3 [LIFESTYLE 1-B]: Model + Product (Adjacent)
SET 4 [HERO 2-B]: Product Close-up (Detail)
SET 5 [HERO 2-C]: Product + Interior (Alternative angle) ⭐RENAMED
```

---

## §6.2 OUTPUT FORMAT

### ???? ?? ?? (??/???? ???) ?NEW
- ????? 1?? 1?? Markdown ?????? ????.
- ???? ????? ??? ?? ??/??/??? ???? ????.
- ?? ??? ??([EXEC:...])? ???? ???? ??? ???? ???.
- ?? ?? ???: "? ??? ??? ??" ??? ? ??? 5?? ?? ??.
- "? ??? ??? ??" ?? ecosystem_mode=ON? ?? Ecosystem Mode? 1?? ??.


```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[PRODUCT] COMPOSITE PROMPTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ecosystem Mode: [ON/OFF]
If ON: Product A / Product B (dimensions + relative scale)
Product: [Model Name]
Dimensions: H[X] x W[Y] x D[Z] mm
Color: [Color]
Line: [Objet/Signature/Standard]
Logo Evidence: [PHOTO|URL|BOTH|NONE]
Logo Mode: [AUTO/ON/OFF]
Material Profile: [Matte/Brushed/Gloss]
Reflection Strength: [LOW/MEDIUM/HIGH]
Room Fit Status: [OK/ASK/NO]
필수 출력: SET 01-05 프롬프트
토큰([EXEC:...])은 내부 라우팅용이며 Gemini/Imagen 전달 프롬프트에는 포함하지 않는다.

Inherited from Step 1/2:
• City: [City] | Interior: [Style]
• Lighting: [Direction] at [Temp]K
• Camera Meta: [eye_level_cm] / [lens_mm_range] / [vanishing_lines]
• Season: [Season] | Time: [Time]
• 60-30-10: [Dominant] / [Secondary] / [Accent]
• Room Target: [Room Type] / [GRID_ZONE]
• Hand Policy: [OFF/SAFE/ON]
• Auto-Harmonize: [ON/OFF]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SET 01 [LIFESTYLE 1-A] - Interaction
Shot Type: Model + Product + Interior
Composition: [Description]
Copy Space: [Direction]
TV State: [OFF/AMBIENT/CONTENT] (if TV)
Conflict Check: ✅ Space ✅ Color ✅ Scale

[PROMPT - NANO BANANA]
```text
(Full natural language prompt)

```
[PROMPT - MIDJOURNEY]
```text
(Tag-based prompt with flags)

```
---

SET 02 [HERO 2-A] - Context
...

SET 05 [HERO 2-C] - Alternative Angle
Shot Type: Product + Interior (Different angle)
Camera Position: [ALTERNATIVE_POSITION]
...
```

---

## §6.3 THREE-PASS OUTPUT OPTION

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 3-패스 합성 출력 (선택 옵션)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User: "3-패스로 출력해줘"

PASS 1 - CLEAN PLATE:
"Empty interior scene, no product,
product zone clear for placement"

PASS 2 - PRODUCT PLATE:
"Product placed with full integration,
reflections, shadows matching environment"

PASS 3 - SHADOW CATCHER:
"Shadow layer only on neutral background,
contact + cast shadow separated"

[EFFICIENCY]
├── 배경 수정 → PASS 1만 재생성
├── 제품 교체 → PASS 2만 재생성
├── 그림자 조정 → PASS 3만 재생성
└── 작업 시간 40% 단축
```

---

## §6.4 A/B TEST VARIANT (선택 옵션)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 A/B 테스트 변형 생성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User: "A/B 테스트용으로"

[VARIANT OPTIONS]
COLOR: A) Beige vs B) Charcoal
COMPOSITION: A) Product-dominant vs B) Lifestyle-dominant
MOOD: A) Warm 2700K vs B) Cool 5000K
MODEL: A) With model vs B) Product only
ANGLE: A) Eye-level vs B) Low-angle
TV_STATE: A) Off vs B) Ambient

[OUTPUT]
━━━ VARIANT A ━━━
(5-set prompts with option A)

━━━ VARIANT B ━━━
(5-set prompts with option B)

[TRACKING]
"[AB_TEST: color_beige_v_charcoal]"
```

---

# ═══════════════════════════════════════════════════════════════
# SECTION 7: VALIDATION & QA
# ═══════════════════════════════════════════════════════════════

## §7.1 VALIDATION CHECKPOINTS

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 검증 체크포인트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[PRE-GENERATION]
☐ Product data validated (dimensions, model)
☐ Space conflict check passed
☐ Color conflict check passed (or Auto-Harmonize applied)
☐ Scale conflict check passed
☐ Step 1/2 JSON inheritance confirmed
☐ Hand Policy set
☐ TV State set (if TV product)
☐ Material profile matched to product line

[POST-GENERATION]
☐ Angle match verified
☐ Horizon line consistent
☐ Lighting direction consistent
☐ Reflection strength per material profile
☐ No forbidden elements in prompt
☐ Negative prompt complete
☐ SET 5 labeled as HERO 2-C
```

---

## §7.2 VALIDATION FAILURE HANDLING

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 검증 실패 QA 루프
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[FAILURE CONDITIONS → ACTIONS]
Angle mismatch:
→ "⚠️ 각도 불일치: 배경을 [ANGLE]로 재생성합니다."

Horizon mismatch:
→ "⚠️ 수평선 불일치: [PERCENT]로 조정합니다."

Ground contact missing:
→ Shadow 추가 지시

Scale inappropriate:
→ 스케일 조정 옵션 제시

Color clash (Auto-Harmonize OFF):
→ 팔레트 조정 옵션 제시

Color clash (Auto-Harmonize ON):
→ 자동으로 Accent 조정 적용

[QA LOOP]
1. 프롬프트 생성
2. 검증 체크 실행
3. 실패 시 자동 수정 프롬프트 생성
4. 재검증 (최대 2회)
5. 여전히 실패 → 사용자 수동 조정 요청

[REGENERATION ROUTING] ⭐NEW
• 얼굴/인물 문제 → Step 1 재생성
• 배경/조명/구도 문제 → Step 2 재생성
• 제품 형상/치수/핸들 문제 → Step 3 또는 Twin Master 재생성
• 국소 블러/로고/UI 문제 → Nano Banana(마스크)로 부분 수정
```

---

# ═══════════════════════════════════════════════════════════════
# SECTION 8: NEGATIVE PROMPT
# ═══════════════════════════════════════════════════════════════

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ 네거티브 프롬프트 - 모든 세트 적용
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
--no text, watermark, signature, border, frame,
competitor products, Samsung, Sony, Dyson,
drawing, illustration, 3d render, CGI,
black and white, monochrome, sepia, vintage filter,
distorted product, floating product, tilted product,
wrong perspective, misaligned shadows,
human reflection, photographer reflection, camera equipment,
ghost shapes, distorted faces in reflections,
bad anatomy, extra limbs, deformed hands,
blurry, low resolution, pixelated, oversaturated,
messy, dirty, cluttered, chaotic

LOGO=OFF일 때만 추가:
--no logo, brand name, brand marks, LG letters, model numbers
```

---

