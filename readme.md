# リアルタイム位置情報共有アプリWhere am I in Sapporo

![スクリーンショット 2023-07-19 15.52.32.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2365400/dfd865bf-ba4b-c43f-0e3d-bb8165b428ea.png)
- ローカルホストを起動
```shell
uvicorn main:app --reload
```

- ngrokで配信する
```shell
ngrok http 8000
```
