# Jチーム開発環境手引き
2021.8.13更新<br><br>

Pythonの `venv` モジュールを使用して仮想環境を作って環境を揃えます。

githubのリポジトリのURLは以下です。

<https://github.com/2021myj-j/share-game.git>


## Pythonのバージョンは3.9.6

最初にPythonのバージョンが3.9.6であることを確認します。

違う場合はVS codeのPythonプラグインを入れ直すか、Python自体を入れ直してください。

## 仮想環境を作成

今回のプロジェクトのフォルダーを作成し、`cd` で入ります。

### 仮想環境を作ります。
以下のコマンドで仮想環境を作ります。

``` shell
python -m venv env
```

### 仮想環境を有効化
以下のコマンドで仮想環境を有効化します

Mac:
```shell
source ./env/bin/activate
```

Windows:

　　PowerShell, cmd.exe:
```shell
.\env\Scripts\Activate.ps1
```

　　Git Bashなど:
```shell
source ./env/Scripts/activate
```

動作の確認には、下記を実行します:

macOS, Windows Git Bash:
```
which pip
```

Windows PowerShell
```
Get-Command pip
```
こればpipコマンドのpathを調べるコマンドです。そのpathが最初に作成したフォルダーの中に確認ができた場合は、正常に機能しています。🎉

### 仮想環境を閉じる

以下のコマンドで仮想環境を閉じます
```shell
deactivate
```

## githubからプロジェクトをclone

前述の手順で、プロジェクトのフォルダーが仮想環境となりました。

次のコマンドを入れて、プロジェクトをgithubから仮想環境にcloneしましょ。
```shell
git clone https://github.com/2021myj-j/share-game.git
```