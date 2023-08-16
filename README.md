# yuishimamura-api

## ストラクチャー

- AWS Lambda + API Gateway + FastAPI

### ローカル開発方法

```sh
# アプリイメージのビルド
make build

# localhost:{DEV_PORT} で起動
# localhost:{DEV_PORT}/docs にアクセスしてOpenAPIドキュメントが表示されたらOK
make run
```

### テスト方法

```sh
# 以下は make run で起動中の想定。起動してない時は Makefile の exec を run に変えてください。
# 初回実行時に開発用途のライブラリが test_modules/ にインストールされます。

# 全テストの実行
make test

# 2回目以降は pytest のみを実行してもOK
make test-pytest

# @pytest.mark.tmp デコレータをつけたテストのみを実行
make test-pytest MARK=tmp
```

### 依存ライブラリの追加、最新化

```sh
rm requirements.lock
# 必要に応じて requirements.txt に追加したいライブラリを記述する
make requirements.lock

# テストが通ることを確認する
make build
make run
make test
```

### Serverless Framework

```sh
# ドメインを作成(初回のみ)
yarn sls create_domain --stage prod

# ECRにイメージをプッシュ
make push-mainimage

# リソースのデプロイ
yarn sls deploy --stage prod

# リソースの削除
yarn sls delete_domain --stage prod
yarn sls remove --stage prod
```
