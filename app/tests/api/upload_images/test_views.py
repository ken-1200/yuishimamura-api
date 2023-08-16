import pytest
from httpx import AsyncClient


@pytest.mark.skip(reason="テスト用のを用意する必要があるためスキップする")
@pytest.mark.asyncio
async def test_upload_images(ac: AsyncClient) -> None:
    """Upload Images

    正常系テスト
    """
    # 処理の実行
    response = await ac.post(
        "/api/v1/upload_images",
        json={
            "images": ["data:image/png;base64,テスト"],
            "images_json": {
                "images": [
                    {"id": 1, "idx": 1, "src": "/images/IMG_1.webp", "alt": "IMG_1"}
                ]
            },
        },
    )

    # 結果の確認
    print(response.content)
    assert response.status_code == 200
