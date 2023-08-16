import pytest

params_test_images_path = {
    "文字列はNG": ["テスト"],
    "数字はNG": [1],
    "辞書はNG": [{"a": "b"}],
    "リストはNG": [["a", "b"]],
    "NoneはNG": [None],
    "特殊文字を含む文字列はNG": ["!@#$%^&*()"],
}


@pytest.mark.tmp
@pytest.mark.parametrize(
    "images_path",
    params_test_images_path.values(),
    ids=params_test_images_path.keys(),
)
def test_upload_image_request_valid(images_path):
    from app.api.upload_images.schema import UploadImageRequest

    param = {
        "images": images_path,
        "images_json": {},
    }
    with pytest.raises(ValueError):
        UploadImageRequest(**param)
