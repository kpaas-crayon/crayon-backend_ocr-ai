# 1. python 베이스 이미지
FROM python:3.10-slim AS base

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 출력 버퍼링 비활성화 (로그 실시간 출력)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 코드 복사
COPY . .

# 6. 환경 변수 기본값 (prod로 덮어쓰기 가능)
ENV APP_ENV=dev

# 7. FastAPI 실행
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]