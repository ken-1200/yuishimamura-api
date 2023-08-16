import pytest
from httpx import AsyncClient


@pytest.mark.skip(reason="テスト用のを用意する必要があるためスキップする")
@pytest.mark.asyncio
async def test_update_delete_images(ac: AsyncClient) -> None:
    """Update Delete Images

    正常系テスト
    """
    # 処理の実行
    response = await ac.post(
        "/api/v1/update_delete_images",
        json={
            "images_path": ["s3://bucket_name/2023-01-01/00000000.webp"],
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
