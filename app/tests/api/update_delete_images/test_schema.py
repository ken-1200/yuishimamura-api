import pytest

params_test_images_path = {
    "数字はNG": [1],
    "辞書はNG": [{"a": "b"}],
    "s3://始まり以外はNG": ["test/test1.webp", "test/test2.webp"],
    "拡張子がwebp以外はNG": ["s3://test/test1.jpg", "s3://test/test2.jpg"],
}


@pytest.mark.tmp
@pytest.mark.parametrize(
    "images_path",
    params_test_images_path.values(),
    ids=params_test_images_path.keys(),
)
def test_update_delete_image_request_valid(images_path):
    from app.api.update_delete_images.schema import UpdateDeleteImageRequest

    param = {
        "images_path": images_path,
        "images_json": {},
    }
    with pytest.raises(ValueError):
        UpdateDeleteImageRequest(**param)
