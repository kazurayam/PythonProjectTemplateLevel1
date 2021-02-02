# Pythonプロジェクトのテンプレート　レベル1

- @author kazurayam
- @date Feb 2021

<!-- START doctoc -->
<!-- END doctoc -->

## これは何か

Python言語でプログラムを自作したい。そのために環境を作り道具を揃えて使えるようにする必要がある。アプリケーションが何であれ環境と道具は概ね同じであり、繰り返し利用しつつ磨き上げていくものだ。Python初心者のわたしがやってきた準備作業を細かく記録しつつレポジトリとして保存しよう。さまざまなPythonプロジェクトの雛形として使えるだろう。

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
1. プロジェクトのディレクトリ構造をどうするか、自分はこうするという形を決める。
1. Python仮想環境を作る。つまりプロジェクトそれぞれのためにPython処理系のバージョンを選択し、外部ライブラリとそのバージョンを選択できるようにし、他のプロジェクトに影響を及ぼさないよう分離する。このために [pipenv](https://pypi.org/project/pipenv/) を利用する。
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

これでanaconda3-4.4.0に切り替わりました。

なお特定のディレクトリにcdしてから `pyenv local anaconda3-5.3.1` とやればそのディレクトリのしたではglobalに指定したのと別のPython環境を使うことができます。

pyenvでインストールしたバージョンをアンインストールするにはこうします。

```
$ pyenv uninstall バージョン名
```

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

`$repo`の下に下記のようなディレクトリ構造を作ります。
```
$ pwd
/Users/kazuakiurayama/github/PythonProjectTemplateLevel1
:~/github/PythonProjectTemplateLevel1 (master *)
$ tree .
.
├── README.md
└── pyproject
    ├── src
    └── test
```

サブフォルダ `pyproject` を作りました。このフォルダの下にPythonによるアプリケーションを開発する環境を作ることにします。なぜ`$repo`の下にサブフォルダを作ったかというと、Pythonではない別のテクノロジーを用いるコードやライブラリ類（たとえばExcelファイルやchromedriverのバイナリやシェルスクリプトとか）のために別のサブフォルダを作れるようにという考えです。別種のテクノロジーを用いる複数のサブフォルダをまとめて一つのGitレポジトリにまとめて管理できるようにしました。

### pipenvで仮想環境を作る

[pipenv](https://pypi.org/project/pipenv/) はPython仮想環境を作るツールです。下記の記事を参考にした。

- [Qiita Pipenvを使ったPython開発まとめ](https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a)

#### pipenvをインストールする

pyenvで選択したanacondaにpipenvをインストールします。

```
$ pip install pipenv
```

#### プロジェクト固有のPython開発環境を作る

`$repo/pyproject` ディレクトリにcdします。そして次のコマンドを投入する。すると自動的に仮想環境が作られます。

```
$ cd $repo/pyproject
$ pipenv --python 3
Creating a virtualenv for this project...
Pipfile: /Users/kazuakiurayama/github/PythonProjectTemplateLevel1/pyproject/Pipfile
Using /usr/local/bin/python3.8 (3.8.5) to create virtualenv...
⠸ Creating virtual environment...created virtual environment CPython3.8.5.final.0-64 in 1637ms
  creator CPython3Posix(dest=/Users/kazuakiurayama/.local/share/virtualenvs/pyproject-brTiVaad, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/Users/kazuakiurayama/Library/Application Support/virtualenv)
    added seed packages: pip==21.0.1, setuptools==52.0.0, wheel==0.36.2
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

✔ Successfully created virtual environment! 
Virtualenv location: /Users/kazuakiurayama/.local/share/virtualenvs/pyproject-brTiVaad
Creating a Pipfile for this project...
$ ls
Pipfile	src	test
```

前述した手順でインストールしたanaconda3-4.4.0にインストール済みのバージョンのPython3.xが選ばれてそれを使うように仮想環境が初期化されます。

Python仮想環境がどこのディレクトリに作られたのか？下記のコマンドで調べることができます。

```
$repos/pyproject $ pipenv --venv
$ pipenv --venv
/Users/myname/.local/share/virtualenvs/pyproject-brTiVaad
```

$repos/projectディレクトリの下ではなくて、別の場所にできていることに注目しましょう。後でIntelliJ IDEAにPlatform SDKを追加するときにこのパスを指定することになります。
仮想環境はGitによるバージョン管理に含めるべきではありません。だから$reposの下ではなく別の場所に仮想環境が作られるのは好都合です。



#### 外部パッケージを追加する

`requests`パッケージを仮想環境にインストールしてみましょう。

```
:$repos/pyproject (master *+)
$ pipenv install requests
Installing requests...
Adding requests to Pipfile's [packages]...
✔ Installation Succeeded 
Pipfile.lock not found, creating...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success! 
Updated Pipfile.lock (fbd99e)!
Installing dependencies from Pipfile.lock (fbd99e)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 0/0 — 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

pipenvからパッケージをインストールするとPipfileに`[packages]`の記述が自動的に追加されます。

```
$ cat Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[dev-packages]

[requires]
python_version = "3.8"
```

またこの時 `Pipfile.lock` ファイルが自動的に追加されます。

```
$ ls
Pipfile		Pipfile.lock	src		test
```

`Pipfile`と`Pipfile.lock`にはこのプロジェクトのために仮想環境に追加インストールされたパッケージに関する詳細な情報が記録されます。

#### プロジェクト固有のPython仮想環境を別マシンで再現する
 
PipfileとPipfile.lockの二つのファイルをGitレポジトリに追加して共有しよう。これにより、ほかの開発者が別のマシンで同じPython仮想環境を再現することが簡単にできる。これがpipenvを使うことのメリットの第一。

別マシンにGitレポジトリをcloneした後でPython仮想環境を再現するにはこうします。

Pipfileを入力としてパッケージを再インストールするにはこうする。
```
$ cd $anotherrepos/pyproject
$ pipenv install
$ pipenv install --dev
```

PipfileではなくPipfile.lockから詳細バージョンもきっちり合わせて環境を再現するにはこうする。
```
$ cd $anotherrepos/pyproject
$ pipenv sync
$ pipenv sync --dev
```


#### 開発環境だけで使うパッケージを別枠で管理する

通常のパッケージの他に開発環境でだけ使うパッケージを別枠で管理しながらインストールすることもできる。たとえば[`autopep8`](https://githubja.com/hhatto/autopep8)をインストールしてみよう。

```
$ cd $repo/pyproject
$ pipenv install --dev autopep8
```
するとPipfileがこうなる。`[dev-packages]`にautopep8が記入されていることに注目。
```
$ cat Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[dev-packages]
autopep8 = "*"

[requires]
python_version = "3.8"
```

#### Pipfileにスクリプトを登録する

Pipefileの `[scripts]` に短いシェルスクリプトを記述し名前をつけて登録することができます。プロダクトのmainスクリプトを起動する、ユニットテストを実行する、Pythonコードを生成する、Lintツールを実行する、など頻繁に実行するコマンドを登録しておけば便利です。

```
[scripts]
test = "python -m pytest"
format = "autopep8 -ivr ."
```

testスクリプトを実行するにはこうします。

```
$repos/pyproject $ pipenv run test
```

#### 仮想環境に入ってシェルを実行する

```
$repos/pyproject $ pipenv shell
$ pipenv shell
Launching subshell in virtual environment...
 . /Users/kazuakiurayama/.local/share/virtualenvs/pyproject-brTiVaad/bin/activate
:~/github/PythonProjectTemplateLevel1/pyproject (master *+)
$  . /Users/kazuakiurayama/.local/share/virtualenvs/pyproject-brTiVaad/bin/activate
(pyproject) :~/github/PythonProjectTemplateLevel1/pyproject (master *+)

```

```
$ exit
exit
```

#### .envの自動読み込み

プロジェクトに `.env` ファイルを用意しておくと `pepenv run` や `pipenv shell` を実行するときに自動で読み込んでくれる。認証情報などハードコードするにはまずい情報を登録しておくのに便利。ただし `.gitignore` に書いて `.env` を除外するのを忘れずに。

```.env
username=John Doe
password=ThisIsNotAPassword
DEBUG=1
```

シェルの環境変数にDEBUGその他が追加されます。確認してみましょう。
```
$repos/pyproject $ 
pipenv run python
Loading .env environment variables...
Python 3.8.5 (v3.8.5:580fbb018f, Jul 20 2020, 12:11:27) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.environ['DEBUG']
'1'
>>> os.environ['username']
'John Doe'
>>> os.environ['password']
'ThisIsNotAPassword'
```

#### Pipfileからrequirements.txtを生成する

ちなみに[PythonProjectTemplateLevel2](https://github.com/kazurayam/PythonProjectTemplateLevel2) で自作のPythonコードをライブラリにするとき `requirements.txt` ファイルが必要になります。Pipenvでインストールした外部依存ライブラリの詳細を `requirements.txt` に書き出すことができます。下記のコマンドを使う。
```
$ cd $repo/pyproject
$ pipenv run pip freeze > requirements.txt
```
このテクニックを使えば外部依存ライブラリの管理をPipenvに一元化しつつ、pipコマンドでライブラリ化する作業をすることができます。

