def test_default():
    from app.exceptions.exception import YuishimamuraAPIBaseException

    exc = YuishimamuraAPIBaseException()
    assert exc.status_code == 500
    assert {
        "code": "yuishimamura_api.internal_server_error",
        "message": "InternalServerError",
    } == exc.content
