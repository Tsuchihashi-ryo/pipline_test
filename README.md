# Vertex AI 計算パイプライン

このプロジェクトには、次の手順を実行する単純なVertex AIパイプラインが含まれています。
1. 2つの数値を入力として受け取ります。
2. 2つの数値を乗算します。
3. 2つの数値を加算します。
4. 乗算結果と加算結果の差を計算します。

## 前提条件

- Google Cloudプロジェクト
- `gcloud`コマンドラインツールがインストールされ、認証されていること
- Google Cloud Storage（GCS）バケット

## セットアップ

1.  **依存関係のインストール:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **パイプラインの構成:**
    `run.py`ファイルを開き、プレースホルダーの値を独自のものに置き換えます。
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
