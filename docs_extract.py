import httpx

async def extract_text_from_docs(client: httpx.AsyncClient, access_token: str, doc_id: str):
    """
    Google Docs 문서 ID로부터 모든 텍스트를 비동기로 추출
    :param client: httpx.AsyncClient 인스턴스
    :param access_token: Google OAuth 토큰
    :param doc_id: Google Docs 문서 ID
    :return: 추출된 전체 텍스트 (string)
    """

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}"

    try:
        res = await client.get(url, headers=headers)
        res.raise_for_status()
    except httpx.HTTPError as e:
        print(f"❌ Google Docs API 호출 실패: {e}")
        return None

    data = res.json()

    if "body" not in data:
        print("❌ 문서 본문을 읽을 수 없습니다.")
        print(data)
        return None

    text_chunks = []
    for content in data["body"].get("content", []):
        paragraph = content.get("paragraph")
        if not paragraph:
            continue
        for element in paragraph.get("elements", []):
            run = element.get("textRun")
            if run and "content" in run:
                text_chunks.append(run["content"])

    full_text = "".join(text_chunks).strip()
    print("✅ 텍스트 추출 완료:")
    print(full_text[:200] + "..." if len(full_text) > 200 else full_text)

    return full_text
