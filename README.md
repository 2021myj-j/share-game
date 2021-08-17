# share-game
This project is for the Hackathon Summer Camp 2021 organized by Myjlab of SSI AGU.

The team members are the following four people:

- @a8119056
- @nkry-617
- @zookam
- @KuroiCc

## 概要
share-gameはYouTube Studioのコメント欄からコメントを抽出し、抽出した結果によって動きを制御するゲームです。

###  - ゲームの内容

キャラクターを左右に動かし、敵や障害物を避けるゲーム

### - 操作方法

    ✔︎　A　＝　左に動く

    ✔︎　D　＝　右に動く


## Quick Start
### 環境配置
1. まずは
[このファイル](https://github.com/2021myj-j/share-game/blob/main/Jチーム開発環境手引き.md)
を参照してPython仮想環境を作る。

2. 仮想環境で以下のコードで必要なモジュールをダウンロードする。
```shell
$ pip install -r share-game/requirements.txt
```

3. [YouTube APIキーの取得 (2020/03/25時点)](https://qiita.com/iroiro_bot/items/1016a6a439dfb8d21eca)
にしたがってYouTube APIを取得し、YouTube StudioのURLと一緒に `key.yaml` にコピーする。

    例えはこのように：
```yaml
YOTUBER_URL: “Your YouTube Live URL”
YOTUBER_API_KEY: ”Your YouTube API Key“
```

### 実行
`main.py` を実行すると、ゲームが始まる。

main.pyの最後に一行 `App()` を `App(debug_mode=True)`に変更すると、debug modeでゲームを起動することができる。