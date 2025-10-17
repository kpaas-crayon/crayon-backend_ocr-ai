import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 환경 감지
# APP_ENV 환경변수가 undefined인 경우, 기본값은 dev
APP_ENV = os.getenv("APP_ENV", "dev").lower()

# 운영(prod)일 때는 logger 설정
# 모드 변환 예시) docker run -e APP_ENV=prod ocr-assessment-ai
if APP_ENV == "prod":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("/var/log/fastapi/app.log"),
            logging.StreamHandler()
        ]
    )
    log = logging.getLogger(__name__)
else:
    log = None  # 개발 모드에선 print() 사용

def grade_text(student_text: str, criteria: str):
    """
    수행평가 자동 채점 — 문맥 분석 중심, 수정 금지
    """
    instruction = """
# 역할
당신은 대한민국의 논술 교사이자 수행평가 채점 전문가입니다.
당신의 임무는 학생의 답안을 문법적으로 수정하거나 다시 쓰는 것이 아니라,
문맥이 다소 뒤섞여 있더라도 스스로 논리적으로 내용을 이해하고,
교사의 채점 기준에 따라 공정하게 점수와 이유를 제시하는 것입니다.

# 반드시 지켜야 할 사항
- 학생의 글을 수정, 요약, 재작성하지 않습니다.
- 문장이 뒤죽박죽이더라도 스스로 문맥을 해석하여 의미를 파악합니다.
- 점수는 10점 만점 기준으로 채점합니다.
- 출력은 오직 아래 형식으로만 합니다.

출력 형식 예시:
점수: 8/10
이유: 학생은 ~~ 내용을 충실히 제시했으나 ~~ 부분이 부족함.

# 업무 처리 순서
1. 학생의 답안에서 주요 키워드 및 논리적으로 주제 파악
2. 내용을 한 번 더 검토하고 수행평가 채점 기준과 비교
3. 수행평가 채점 기준에 의거하여 점수 도출
4. 도출된 점수에 대한 이유 작성
5. 출력 형태: 점수는 줄바꿈으로 구분하며 이후 이유를 작성합니다.
"""

    grading_prompt = f"""
[채점 기준]
{criteria}

[학생 답안]
{student_text}

요청사항:
- 학생 글의 논리 흐름이 다소 뒤섞여 있더라도 의미를 파악해 채점
- 학생의 글을 직접 수정하거나 재작성하지 말 것
- 점수와 이유만 출력할 것
"""

    full_prompt = instruction.strip() + "\n\n" + grading_prompt.strip()
    token_estimate = len(full_prompt) / 4

    # 환경에 따른 로그 출력 방식 전환
    if APP_ENV == "prod":
        log.info(f"🔍 예상 토큰 수: 약 {int(token_estimate)}개")
    else:
        print(f"🔍 예상 토큰 수: 약 {int(token_estimate)}개")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=200,
    )

    result = response.choices[0].message.content.strip()

    if APP_ENV == "prod":
        log.info("✅ GPT 채점 완료")
    else:
        print("✅ GPT 채점 완료")

    return result
