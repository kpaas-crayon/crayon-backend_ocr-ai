# Docker 빌드용
# 입력: [file_id], [criteria], [access_token]
# 전체 과정 자동화 완료 ✔️
# 출력: "점수: n점", \n"이유: ~~"
# 코드에 대한 상세한 설명은 \previous\pre_main.py에 있음

from fastapi import FastAPI, Request, HTTPException
from google_auth import router as auth_router
from pydantic import BaseModel
import httpx

from drive_convert import convert_pdf_to_docs
from docs_extract import extract_text_from_docs
from gpt_assessment import grade_text

app = FastAPI()
app.include_router(auth_router)

# 요청 Body 정의
class AutoGradeRequest(BaseModel):
    file_id: str
    criteria: str

# 서버 상태 확인용
@app.get("/")
async def root():
    return {"message": "FastAPI 서버 정상 동작 중"}

# ======================================
# PDF → Docs 변환 → 텍스트 추출 → GPT 채점 자동화 테스트용
# ======================================
@app.post("/ocr-ai")
async def auto_grade(req: Request, body: AutoGradeRequest):
    """
    PDF → Google Docs 변환 → 텍스트 추출 → GPT 채점까지 자동 실행.
    """

    # ✅ Kong이 이미 인증한 상태이므로 Authorization 헤더에서 access_token 가져옴
    access_token = req.headers.get("X-Google-Access-Token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access Token 누락됨")

    # httpx AsyncClient를 한 세션으로 사용
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1️⃣ PDF → Docs 변환
        doc_id = await convert_pdf_to_docs(client, access_token, body.file_id)
        if not doc_id:
            raise HTTPException(status_code=400, detail="PDF → Docs 변환 실패")

        # 2️⃣ Docs 텍스트 추출
        text = await extract_text_from_docs(client, access_token, doc_id)
        if not text:
            raise HTTPException(status_code=400, detail="Docs 텍스트 추출 실패")

        # 3️⃣ GPT 채점
        result = await grade_text(client, text, body.criteria)
        if not result:
            raise HTTPException(status_code=400, detail="GPT 채점 실패")

    # 4️⃣ 결과 반환
    return result
