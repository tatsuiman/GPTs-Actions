# 関数

Function Calling から呼び出される関数です。

## サンプル
`src/function/`に以下のようなpythonファイル`my_youtube_transcript.py`を作成してください
```python
import os
import sys
import logging
from youtube_transcript_api import YouTubeTranscriptApi

def run(url, language=["ja"]):
    video_id = url.split("=")[-1] if "=" in url else url.split("/")[-1]
    # 字幕リストを取得
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    # 英語字幕は"en"に変更
    transcript = transcript_list.find_generated_transcript(language)
    text = ""
    transcript_text = ""
    for d in transcript.fetch():
        text = d["text"]
        transcript_text += f"{text}\n"
    return transcript_text
```

serverless.yamlに以下を追記
```yaml
  my_youtube_transcript:
    maximumEventAge: 21600
    maximumRetryAttempts: 0
    image:
      name: gpts-functions
      command: app.handler
    events:
      - http:
          path: my_youtube_transcript
          method: post
          cors: true
          integration: lambda-proxy
          private: true
```

再度デプロイを行うと関数が追加されます
```bash
sls deploy
```