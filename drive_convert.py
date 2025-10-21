import httpx

# ======================================
# Google Drive 파일 검색 및 PDF → Docs 변환 (비동기 버전)
# ======================================

async def get_file_id_by_name(client: httpx.AsyncClient, access_token: str, filename: str):
    """
    Google Drive에서 파일 이름으로 ID 검색 (비동기)
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.googleapis.com/drive/v3/files"
    params = {
        "q": f"name='{filename}' and mimeType='application/pdf'",
        "fields": "files(id, name)"
    }

    try:
        res = await client.get(url, headers=headers, params=params)
        res.raise_for_status()
    except httpx.HTTPError as e:
        print(f"❌ 파일 검색 실패: {e}")
        return None

    data = res.json()
    if "files" in data and len(data["files"]) > 0:
        file_id = data["files"][0]["id"]
        print(f"✅ {filename} 찾음 (ID: {file_id})")
        return file_id
    else:
        print("❌ 해당 이름의 PDF를 찾을 수 없습니다.")
        return None


async def convert_pdf_to_docs(client: httpx.AsyncClient, access_token: str, file_id: str):
    """
    Google Drive의 PDF를 Google Docs 문서로 복제(변환) (비동기)
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}/copy"
    body = {"mimeType": "application/vnd.google-apps.document"}

    try:
        res = await client.post(url, headers=headers, json=body)
        res.raise_for_status()
    except httpx.HTTPError as e:
        print(f"❌ 변환 요청 실패: {e}")
        return None

    if res.status_code == 200:
        doc_id = res.json().get("id")
        print(f"✅ 변환 완료! 새 문서 ID: {doc_id}")
        return doc_id
    else:
        print(f"❌ 변환 실패: {res.text}")
        return None
