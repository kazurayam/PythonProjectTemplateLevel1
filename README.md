# Pythonプロジェクトのテンプレート　レベル1

- @author kazurayam
- @date Feb 2021

## これは何か

Python言語でプログラムを自作したい。そのために環境を作り道具を揃えて使えるようにする必要がある。アプリケーションが何であれ環境と道具は概ね同じであり、繰り返し利用しつつ磨き上げていくものだ。Python初心者のわたしがやってきた環境と道具の準備作業を細かく記録しよう。結果としてさまざまなPythonプロジェクトの雛形を作ろう。

Gitレポジトリを4つ作る。

1. [PythonProjectTemplateLevel1](https://github.com/kazurayam/PythonProjectTemplateLevel1) --- つまりこのレポジトリ。Python処理系をインストールする。pipenvで仮想環境を構築する。わたし流のディレクトリ構造を決める。IntelliJ IDEAを設定する。pytestでユニットテストする。
1. [PythonProjectTemplateLevel2](https://github.com/kazurayam/PythonProjectTemplateLevel2) --- わたしのPythonコードをpipでライブラリにしてPyPIにアップロードして共有可能にする。そのライブラリを仕込んだDockerイメージを作りDocker Hubにアップロードして共有可能にする。
1. [PythonProjectTemplateLevel3](https://github.com/kazurayam/PythonProjectTemplateLevel3) --- 単純なWebサーバアプリケーションを作る。Laravelフレームワークで。Dockerイメージを作る。
1. [PythonProjectTemplateLevel4](https://github.com/kazurayam/PythonProjectTemplateLevel4) --- Laravelで作ったWebサーバアプリのユーザインタフェースをSeleniumでテストする。Page Objectモデルで。

## 前提条件

1. マシンはMac Book Air、OSは macOS 11.1 Big Sur。
1. MacにHomebrewをインストール済み、説明は省略する
1. MacにGitをインストール済み、Git Hubに自分のアカウントを持っていて、Gitの操作に熟達していると前提するので説明は省略する。
1. MacでIntelliJ IDEAを開発環境として使う。IDEAのライセンスを持っていてPythonプラグインをインストール済みと前提する。

## 達成目標

Level1では下記のことを達成することを目標とする。

1. Python処理系をマシンにインストールする。Python 3.8をメインとし、Python 3.9も使えるようにする。各プロジェクトがPythonインタープレタのバージョンを切り替えられるようにしたい。[pyenv]() を経由して複数バージョンの[Anaconda](https://www.anaconda.com/) をインストールする。そして特定のバージョンのAnacondaを選択する。
1. Python仮想環境を作る。つまりプロジェクトそれぞれのためにPython処理系のバージョンを選択し、外部ライブラリとそのバージョンを選択できるようにし、他のプロジェクトに影響を及ぼさないよう分離する。このために [pipenv](https://pypi.org/project/pipenv/) を利用する。
1. プロジェクトのディレクトリ構造をどうするか、自分はこうするという形を決める。
1. 上記で作ったプロジェクト専用のPython仮想環境をIntelliJ IDEAにPython SDKの一つとして追加する。そして本プロジェクトのためのSDKとしてそれを登録する。これにより本プロジェクト専用の仮想環境がIntelliJ IDEAから使えるようになる。
1. [pytest](https://docs.pytest.org/en/stable/) を導入しユニットテストを書き、実行する。

## 手順

### pyenv経由でAnacondaをインストールする

この記事を参考にした。

- [【2021年最新版】MacOSで複数のPython/Anacondaバージョンを使い分ける方法【データ分析】](https://www.simpletraveler.jp/2021/01/02/macos-pyenv-python-anaconda-versionmanagement/#pyenvMac)

[pyenv](https://github.com/pyenv/pyenv)は複数のバージョンのPython処理系を管理するためのツール。

pyenvをインストールする。

```
$ brew install pyenv
```

pyenvのパスをMacの.bash_profileに記述する。

```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

なおmacOS11ではデフォルトではzshを使うことになっているが、個人的好みのせいでわたしはいまだにbashです。

pyenvを使って特定バージョンのAnacondaをインストールする

```
$ pyenv install --list | grep anaconda
  ...
  anaconda3-4.4.0
  ...
  anaconda3-5.3.1
  ...
```
たくさんリストアップされた候補の中からanaconda3-4.4.0とanaconda3-5.3.1の二つをインストールすることにした。

```
$ pyenv install anaconda3-4.4.0
```

そして

```
$ pyenv install anaconda3-5.3.1
```

わたしの環境ではそれぞれ10分ぐらいかかった。

コマンドラインで`python`コマンドを投入した時にどのバージョンが使われるかを確認しよう。

```
$ pyenv versions
* system (set by /Users/kazuakiurayama/.pyenv/version)
  anaconda3-4.4.0
  anaconda3-5.3.1
```

`system`に*がついています。macOSにプレインストールされたものが選択がされてい流。追加したanacondaが選択されていません。これではつまらない。

`pyenv global バージョン`コマンドで設定を切り替えます。今からはanaconda3-4.4.0を使うことにしましょう。

```
$ pyenv global anaconda3-4.4.0
:~
$ pyenv versions
  system
* anaconda3-4.4.0 (set by /Users/kazuakiurayama/.pyenv/version)
  anaconda3-5.3.1
```

anaconda3-4.4.0に切り替わりました。

なお特定のディレクトリにcdしてから `pyenv local anaconda3-5.3.1` とやればそのディレクトリのしたではglobalに指定したのと別のPython環境を使うことができます。

### プロジェクトのためにディレクトリを作る

本プロジェクトのためにディレクトリを作ります。場所は適宜。mkdirで。

```
$ cd
$ cd github
$ mkdir PythonProjectTemplateLevel1
$ cd PythonProjectTemplateLevel1
$ pwd
~/github/PythonProjectTemplateLevel1
```

以下の記述では `~/github/PythonProjectTemplateLevel1` を手短に `$repo` と書くことにします。

### pipenvで仮想環境を作る

[pipenv](https://pypi.org/project/pipenv/) はPython仮想環境を作るツールです。下記の記事を参考にした。

- [Qiita Pipenvを使ったPython開発まとめ](https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a)

pyenvで選択したanacondaにpipenvをインストールします。

```
$ pip install pipenv
```