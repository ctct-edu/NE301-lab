# Session 4: レビュー機能活用

## 前提

- Session 3 でタスク表示・追加機能が完成していること
- `exercise/` フォルダの中身を作業フォルダにコピーしていること

## この演習で使う AI 機能

この演習では、複数の AI 機能を使い分けます。

| 機能           | 用途                                 | 操作                                                                                                                   |
| -------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| インライン補完 | 関数の実装                           | コードを入力すると自動で提案が表示。`Tab` で受け入れ                                                                   |
| チャット       | コードレビュー、リファクタリング相談 | GitHub Copilot: `Ctrl + Shift + I`（Mac: `Cmd + Shift + I`）/ Cursor: `Ctrl + L`（Mac: `Cmd + L`）                     |
| インライン編集 | コードの部分的な修正                 | GitHub Copilot: `Ctrl + I`（Mac: `Cmd + I`）/ Cursor: `Ctrl + K`（Mac: `Cmd + K`）。修正したいコードを選択してから実行 |

---

## 演習 1: 完了切り替え・削除機能の実装（15 分）

この演習では、タスクの完了状態を切り替える機能と、タスクを削除する機能を実装します。

### ステップ 1: ファイルを確認する

作業フォルダにコピーした `todo.py` を VS Code または Cursor で開きます。Session 3 の完成形（メニュー表示、タスク一覧表示、タスク追加）が入っています。

> [!NOTE]
> **フォルダを VS Code で開くには**
>
> デスクトップにある該当フォルダを、デスクトップの VS Code のショートカットにドラッグ＆ドロップすると、そのフォルダが VS Code で開きます。

### ステップ 2: 完了切り替え関数の骨格を入力する

`todo.py` に以下のコードを追加します。

```py
def toggle_task(tasks):
    # タスク一覧を表示
    # ユーザーに ID を入力してもらう
    # 該当タスクの completed を反転させる
    pass
```

### ステップ 3: インライン補完で実装する

使用する AI 機能: **インライン補完**

`pass` を削除し、コメントの下に新しい行を作ります。AI がインライン補完でコードを提案してくるので、内容を確認して `Tab` で受け入れます。

期待される実装：

```py
def toggle_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("切り替えるタスクの ID を入力してください: "))
    except ValueError:
        print("無効な入力です。数字を入力してください。")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            status = "完了" if task["completed"] else "未完了"
            print(f"タスク「{task['title']}」を{status}にしました。")
            return

    print("指定された ID のタスクが見つかりません。")
```

ポイント：

- `try-except` で数字以外の入力に対応しています
- `not task["completed"]` で `True` / `False` を反転させています
- 該当するタスクが見つからない場合のエラーメッセージも重要です

### ステップ 4: 削除関数の骨格を入力する

続けて以下のコードを追加します。

```py
def delete_task(tasks):
    # タスク一覧を表示
    # ユーザーに ID を入力してもらう
    # 確認メッセージを表示
    # 該当タスクを削除する
    pass
```

### ステップ 5: インライン補完で実装する

使用する AI 機能: **インライン補完**

`pass` を削除し、コメントの下で AI のインライン補完を活用して実装します。

期待される実装：

```py
def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("削除するタスクの ID を入力してください: "))
    except ValueError:
        print("無効な入力です。数字を入力してください。")
        return

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            confirm = input(f"タスク「{task['title']}」を削除しますか？ (y/n): ")
            if confirm.lower() == "y":
                tasks.pop(i)
                print("タスクを削除しました。")
            else:
                print("削除をキャンセルしました。")
            return

    print("指定された ID のタスクが見つかりません。")
```

ポイント：

- `enumerate()` でインデックスと要素を同時に取得しています
- 削除前に確認メッセージを表示して、誤操作を防止しています
- `tasks.pop(i)` でリストから該当のタスクを削除しています

### ステップ 6: メインメニューに組み込む

`main()` 関数内に、選択肢 3 と 4 の処理を追加します。

```py
        elif choice == "3":
            toggle_task(tasks)
        elif choice == "4":
            delete_task(tasks)
```

### ステップ 7: 動作確認

```sh
python todo.py
```

以下を確認します。

- `3` を選択してタスクの完了状態が切り替わること
- `4` を選択してタスクが削除できること（確認メッセージが表示されること）

---

## 演習 2: AI を使ったリファクタリング（15 分）

この演習では、AI にコードレビューを依頼し、その結果を元にリファクタリング（コードの改善）とバリデーション（入力値の検証）を実装します。

### ステップ 1: AI にコードレビューを依頼する

使用する AI 機能: **チャット（Chat パネル）**

チャットパネルを開きます。

- **GitHub Copilot**: サイドバーのチャットアイコンをクリック、または `Ctrl + Shift + I`（Mac: `Cmd + Shift + I`）
- **Cursor**: `Ctrl + L`（Mac: `Cmd + L`）

チャットパネルに以下のプロンプトを入力して送信します。

**入力するプロンプト：**

```txt
@todo.py をレビューしてください。
特に以下の観点で確認してください。
- バグがないか
- コードの可読性
- 改善できる点
```

`@todo.py` と入力すると、ファイルの内容を AI に渡すことができます。GitHub Copilot でも Cursor でも `@` でファイルを参照できます。

### ステップ 2: 指摘事項を確認する

AI の回答を確認します。一般的に以下のような指摘が返ってきます。

- エラーハンドリングがない（数字以外の入力への対応）
- タスクが空のときの処理
- 変数名やコメントの改善提案
- マジックナンバー（意味の分からない数値）の使用

AI の指摘をすべて受け入れる必要はありません。「なるほど」と思う点は修正し、自分のコードのスタイルと合わない提案は無視してかまいません。

### ステップ 3: バリデーション関数を実装する

レビューの指摘を踏まえて、ユーザー入力の検証（バリデーション）を行う関数を追加します。AI のチャット機能でリファクタリングの相談をしてみましょう。

**入力するプロンプト：**

```txt
@todo.py の add_task 関数にバリデーション機能を追加したいです。
- 空文字や空白のみの入力を拒否する
- タスク名の長さ制限（100 文字以内）を設ける
- バリデーション処理は別の関数に切り出す
どのように実装すればよいですか？
```

AI の提案を参考に、以下のバリデーション関数を実装します。インライン補完を活用してもよいですし、AI の提案をそのまま貼り付けてもかまいません。

```py
MAX_TITLE_LENGTH = 100

def validate_title(title):
    # 空文字チェック
    if not title:
        return False, "タスク名を入力してください。"

    # 空白のみチェック
    if title.strip() == "":
        return False, "タスク名を入力してください。"

    # 長さチェック
    if len(title) > MAX_TITLE_LENGTH:
        return False, f"タスク名は{MAX_TITLE_LENGTH}文字以内で入力してください。"

    return True, title.strip()
```

- バリデーション関数は `(成功/失敗, メッセージまたは値)` のタプルを返します
- `strip()` で前後の空白を除去しています
- 定数 `MAX_TITLE_LENGTH` で長さの上限を設定しています

### ステップ 4: add_task に組み込む

使用する AI 機能: **インライン編集**

`add_task` 関数の入力チェック部分を修正します。`add_task` 関数全体を選択した状態で、インライン編集を起動します。

- **GitHub Copilot**: `Ctrl + I`（Mac: `Cmd + I`）
- **Cursor**: `Ctrl + K`（Mac: `Cmd + K`）

**入力するプロンプト：**

```txt
validate_title 関数を使ってバリデーションを行うように修正してください
```

AI が提案した変更内容を確認し、問題なければ「Accept」で受け入れます。

修正後の `add_task` 関数は以下のようになります。

```py
def add_task(tasks):
    title = input("タスク名を入力してください: ")

    is_valid, result = validate_title(title)
    if not is_valid:
        print(result)
        return

    title = result  # 空白除去済みのタイトル
    # ... 以下は同じ ...
```

### ステップ 5: 動作確認

```sh
python todo.py
```

以下を確認します。

- 空のタスク名を入力してエラーメッセージが表示されること
- 空白のみのタスク名でもエラーになること

---

## 演習 3: CSV ファイルへのデータの永続化（15 分）

この演習では、タスクを CSV ファイルに保存・読み込みする機能を実装します。これにより、アプリを終了してもデータが保持されるようになります。

### ステップ 1: 必要なモジュールをインポートする

ファイルの先頭に以下を追加します。

```py
import csv
import os
```

- `csv` は CSV ファイルを読み書きするための標準ライブラリです
- `os` はファイルの存在確認などに使います

### ステップ 2: 読み込み関数の骨格を入力する

ファイルの先頭付近（`import` 文の後）に以下を追加します。

```py
CSV_FILE = "tasks.csv"

def load_tasks():
    # CSV ファイルが存在しなければ空のリストを返す
    # 存在すれば読み込んでリストで返す
    pass
```

### ステップ 3: インライン補完で読み込み関数を実装する

使用する AI 機能: **インライン補完**

`pass` を削除し、コメントの下で AI のインライン補完を活用して実装します。

期待される実装：

```py
CSV_FILE = "tasks.csv"

def load_tasks():
    if not os.path.exists(CSV_FILE):
        return []

    tasks = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = {
                "id": int(row["id"]),
                "title": row["title"],
                "completed": row["completed"] == "True",
                "created_at": row["created_at"]
            }
            tasks.append(task)
    return tasks
```

ポイント：

- CSV から読み込んだデータはすべて文字列になるため、型の変換が必要です
- `id` は `int()` で数値に変換しています
- `completed` は文字列 `"True"` との比較で真偽値（`True` / `False`）に変換しています
- `encoding="utf-8"` を指定すると日本語も正しく読み込めます

### ステップ 4: 保存関数を実装する

使用する AI 機能: **インライン補完**

続けて保存関数を追加します。以下のコメントを入力して、インライン補完を活用してください。

```py
def save_tasks(tasks):
    # タスクを CSV ファイルに保存する
```

期待される実装：

```py
def save_tasks(tasks):
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "title", "completed", "created_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)
```

### ステップ 5: メインループを修正する

`main()` 関数を以下のように修正します。変更点は 3 つです。

1. 起動時に `load_tasks()` でデータを読み込むようにする
2. データが変更されるたびに `save_tasks()` で保存する
3. テスト用のグローバル変数 `tasks` を削除する

```py
def main():
    tasks = load_tasks()  # 起動時に読み込み

    while True:
        # ... メニュー表示 ...

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
            save_tasks(tasks)  # 追加後に保存
        elif choice == "3":
            toggle_task(tasks)
            save_tasks(tasks)  # 変更後に保存
        elif choice == "4":
            delete_task(tasks)
            save_tasks(tasks)  # 削除後に保存
        elif choice == "5":
            print("終了します。")
            break
```

ファイルの先頭にあるテスト用の `tasks = [...]`（グローバル変数）は不要になったので削除してください。

### ステップ 6: 動作確認

```sh
python todo.py
```

以下を確認します。

1. アプリを起動してタスクを追加する
2. `5` を選択してアプリを終了する
3. 再度 `python todo.py` で起動して、タスクが保持されていることを確認する
4. 作業フォルダに `tasks.csv` ファイルが作成されていることを確認する

完成したら、`Ans/` フォルダの `todo.py` と見比べて確認してください。
