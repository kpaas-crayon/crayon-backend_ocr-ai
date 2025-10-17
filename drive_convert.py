# 직접 파일 이름 링크에 넣어서 검색하여 ID 찾아서 변환하는 방식

import requests

def get_file_id_by_name(access_token: str, filename: str):

    """
    Google Drive에서 파일 이름으로 ID 검색
    """

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.googleapis.com/drive/v3/files"
    params = {
        "q": f"name='{filename}' and mimeType='application/pdf'",
        "fields": "files(id, name)"
    }

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    if "files" in data and len(data["files"]) > 0:
        file_id = data["files"][0]["id"]
        print(f"✅ {filename} 찾음 (ID: {file_id})")
        return file_id
    else:
        print("❌ 해당 이름의 PDF를 찾을 수 없습니다.")
        return None


def convert_pdf_to_docs(access_token: str, file_id: str):

    """
    Google Drive의 PDF를 Google Docs 문서로 복제(변환)
    """

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}/copy"
    body = {"mimeType": "application/vnd.google-apps.document"}

    res = requests.post(url, headers=headers, json=body)
    if res.ok:
        doc_id = res.json().get("id")
        print(f"✅ 변환 완료! 새 문서 ID: {doc_id}")
        return doc_id
    print("❌ 변환 실패:", res.text)
    return None