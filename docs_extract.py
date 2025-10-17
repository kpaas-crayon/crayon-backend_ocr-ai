import requests

def extract_text_from_docs(access_token: str, doc_id: str):

    """
    Google Docs 문서 ID로부터 모든 텍스트를 추출
    """

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}"

    res = requests.get(url, headers=headers)
    data = res.json()

    if "body" not in data:
        print("❌ 문서 본문을 읽을 수 없습니다.")
        print(data)
        return None

    text = ""
    for content in data["body"]["content"]:
        paragraph = content.get("paragraph")
        if not paragraph:
            continue
        for element in paragraph.get("elements", []):
            run = element.get("textRun")
            if run:
                text += run["content"]

    print("✅ 텍스트 추출 완료:")
    print(text[:200] + "..." if len(text) > 200 else text)
    return text.strip()
