import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.skip(reason="テストでは例外ハンドラで捕捉できないためスキップ")
@pytest.mark.asyncio
async def test_default_error(ac: AsyncClient) -> None:
    @app.post("/_test/raise_not_http_exception")
    async def error():
        raise ValueError("Not HTTPException")

    # 処理の実行
    response = await ac.post("/_test/raise_not_http_exception")

    # 結果の確認
    print(response.content)
    assert response.status_code == 500
    expected = {
        "message": "InternalServerError",
        "code": "yuishimamura_api.internal_server_error",
    }
    assert expected == response.json()


@pytest.mark.asyncio
async def test_not_found_error(ac: AsyncClient) -> None:
    # 処理の実行
    response = await ac.get("/_test/not_found")

    # 結果の確認
    print(response.content)
    assert response.status_code == 404
    expected = {"message": "NotFound", "code": "yuishimamura_api.not_found"}
    assert expected == response.json()
