# Vertex AI 計算パイプライン

このプロジェクトには、次の手順を実行する単純なVertex AIパイプラインが含まれています。
1. 2つの数値を入力として受け取ります。
2. 2つの数値を乗算します。
3. 2つの数値を加算します。
4. 乗算結果と加算結果の差を計算します。
5. 最後に、その差を`scipy`ライブラリの`sigmoid`関数に入力し、最終結果を得ます。

## 前提条件

- Google Cloudプロジェクト
- `gcloud`コマンドラインツールがインストールされ、認証されていること
- Google Cloud Storage（GCS）バケット

## セットアップ

### 1. ローカル環境のセットアップ

パイプラインをコンパイルしたり実行したりするために、ローカルマシンに依存関係をインストールします。
```bash
pip install -r requirements.txt
```

### 2. Dockerコンテナイメージの準備 (コンポーネント実行環境)

このパイプラインは、各コンポーネントを実行するためにカスタムDockerイメージを使用します。これにより、依存関係が事前にインストールされ、実行が高速かつ信頼性の高いものになります。

#### a. Artifact Registry APIの有効化
```bash
gcloud services enable artifactregistry.googleapis.com
```

#### b. Dockerリポジトリの作成
Google CloudプロジェクトでDockerイメージをホストするためのリポジトリを作成します。
```bash
export REPO_NAME="pipeline-components"
export GCP_REGION="<YOUR_REGION>" # 例: us-central1
gcloud artifacts repositories create ${REPO_NAME} \
  --repository-format=docker \
  --location=${GCP_REGION} \
  --description="Repository for pipeline component images"
```

#### c. Docker認証の設定
gcloudを使用して、Artifact RegistryにDockerイメージをプッシュできるように認証を設定します。
```bash
gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev
```

#### d. Dockerイメージのビルドとプッシュ
プロジェクトのルートディレクトリ（`Dockerfile`がある場所）で、以下のコマンドを実行してイメージをビルドし、Artifact Registryにプッシュします。
```bash
export GCP_PROJECT_ID="<YOUR_PROJECT_ID>"
export IMAGE_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPO_NAME}/pipeline-base:latest"

docker build -t ${IMAGE_URI} .
docker push ${IMAGE_URI}
```
成功すると、カスタムイメージがArtifact Registryに保存されます。

### 3. パイプラインのベースイメージを設定

次に、パイプラインのすべてのコンポーネントが、先ほどプッシュしたカスタムイメージを使用するように設定します。

`config.py` ファイルをテキストエディタで開き、`BASE_IMAGE` の値を、上で作成した `IMAGE_URI`（例: `us-central1-docker.pkg.dev/my-gcp-project/pipeline-components/pipeline-base:latest`）に置き換えてください。

**変更前:**
`BASE_IMAGE = 'gcr.io/YOUR_PROJECT_ID/pipeline-components:latest'`

**変更後 (例):**
`BASE_IMAGE = 'us-central1-docker.pkg.dev/my-gcp-project/pipeline-components/pipeline-base:latest'`

このファイルを変更するだけで、パイプラインのすべてのコンポーネントが使用するDockerイメージを一元的に管理できます。


### 4. パイプライン実行スクリプトの構成

`run.py`ファイルを開き、パイプライン実行のためのプレースホルダーの値を独自のものに置き換えます。
```python
# --- ユーザー構成 ---
PROJECT_ID = "your-gcp-project-id"  # <-- 置き換えてください
REGION = "your-gcp-region"      # <-- 置き換えてください (例: "us-central1")
PIPELINE_ROOT = "gs://your-gcs-bucket/pipeline-root" # <-- 置き換えてください
# --------------------------
```

## パイプラインの実行

パイプラインをコンパイルしてVertex AIに送信するには、次のコマンドを実行します。

```bash
python run.py
```

送信後、スクリプトはパイプラインの実行を監視できるGoogle CloudコンソールへのURLを出力します。

---

## APIとしてパイプラインを呼び出す (Cloud Functions経由)

このセクションでは、HTTP POSTリクエストを送信することでパイプラインをトリガーできるAPIエンドポイントとして、Cloud Functionをデプロイする方法について説明します。

### 前提条件

-   `gcloud` CLIがインストールされ、認証済みであること。
-   APIを有効にする:
    ```bash
    gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
    ```
-   Cloud FunctionがVertex AIを呼び出すための権限を持つサービスアカウント。**Vertex AI ユーザー** (`roles/aiplatform.user`) ロールを持つサービスアカウントを使用することをお勧めします。

### デプロイ手順

1.  **パイプラインのコンパイルとコピー**:
    プロジェクトのルートディレクトリから、最新のパイプライン定義をコンパイルし、Cloud Functionのディレクトリにコピーします。これにより、APIが常に最新のパイプラインを使用するようになります。
    ```bash
    # (プロジェクトのルートディレクトリで実行)
    python pipeline.py
    cp calculation_pipeline.json cloud_function/
    ```

2.  **デプロイディレクトリへの移動**:
    `cloud_function` ディレクトリに移動します。
    ```bash
    cd cloud_function
    ```

3.  **環境変数の設定**:
    デプロイコマンドで使用する環境変数を設定します。`<YOUR_PROJECT_ID>`、`<YOUR_REGION>`、`<YOUR_PIPELINE_ROOT_GCS_PATH>`、`<YOUR_SERVICE_ACCOUNT_EMAIL>` を独自の値に置き換えてください。
    ```bash
    export GCP_PROJECT_ID="<YOUR_PROJECT_ID>"
    export GCP_REGION="<YOUR_REGION>"
    export PIPELINE_ROOT_GCS_PATH="<YOUR_PIPELINE_ROOT_GCS_PATH>"
    export SERVICE_ACCOUNT_EMAIL="<YOUR_SERVICE_ACCOUNT_EMAIL>"
    ```

4.  **Cloud Functionのデプロイ**:
    以下の`gcloud`コマンドを実行して、関数をデプロイします。
    ```bash
    gcloud functions deploy trigger-calculation-pipeline \
      --gen2 \
      --runtime=python39 \
      --region=${GCP_REGION} \
      --source=. \
      --entry-point=trigger_pipeline \
      --trigger-http \
      --allow-unauthenticated \
      --service-account=${SERVICE_ACCOUNT_EMAIL} \
      --set-env-vars=GCP_PROJECT_ID=${GCP_PROJECT_ID},GCP_REGION=${GCP_REGION},PIPELINE_ROOT_GCS_PATH=${PIPELINE_ROOT_GCS_PATH}
    ```
    デプロイが完了すると、`https://...` 形式のトリガーURLが出力されます。これがAPIエンドポイントです。

### APIの呼び出し

デプロイしたAPIは、`curl`や他のHTTPクライアントを使用して呼び出すことができます。

1.  **エンドポイントURLの設定**:
    前のステップで出力されたトリガーURLを環境変数に設定します。
    ```bash
    export API_ENDPOINT_URL="<YOUR_TRIGGER_URL>"
    ```

2.  **APIのテスト**:
    `num1`と`num2`をJSONペイロードに含めてPOSTリクエストを送信します。
    ```bash
    curl -X POST "${API_ENDPOINT_URL}" \
      -H "Content-Type: application/json" \
      -d '{
            "num1": 50,
            "num2": 12
          }'
    ```

3.  **成功の応答**:
    成功すると、以下のようなJSON応答が返ってきます。
    ```json
    {
      "dashboard_uri": "https://console.cloud.google.com/vertex-ai/locations/...",
      "job_name": "projects/...",
      "message": "Pipeline job submitted successfully."
    }
    ```
