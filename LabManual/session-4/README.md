# Session 4: レビュー機能活用

## 前提

- Session 3 でタスク表示・追加機能が完成していること
- `starter/` フォルダを作業フォルダにコピーしていること

---

## 演習 1: AI にコードレビューを依頼する（10 分）

この演習では、AI にコードレビューを依頼する方法を学びます。

### ステップ 1: チャットパネルを開く

Session 3 で作成した `todo.py` を開いた状態で、チャットパネルを開きます。

### ステップ 2: レビューを依頼する

以下のプロンプトを入力します。

**入力するプロンプト：**

```txt
@todo.py をレビューしてください。
特に以下の観点で確認してください。
- バグがないか
- コードの可読性
- 改善できる点
```

GitHub Copilot の場合は `@todo.py` でファイルを指定します。Cursor の場合も同様に `@` でファイルを参照できます。

### ステップ 3: 指摘事項を確認する

AI の回答を確認します。一般的に以下のような指摘が返ってきます：

- エラーハンドリングがない（数字以外の入力への対応）
- タスクが空のときの処理
- 変数名やコメントの改善提案

AI の指摘をすべて受け入れる必要はありません。「なるほど」と思う点は修正し、自分のコードのスタイルと合わない提案は無視してよいです。

---

## 演習 2: 完了切り替え・削除機能の実装（20 分）

この演習では、タスクの完了状態を切り替える機能と、タスクを削除する機能を実装します。

### ステップ 1: 完了切り替え関数を実装する

以下のコードを追加します。

```py
def toggle_task(tasks):
    # タスク一覧を表示
    # ユーザーに ID を入力してもらう
    # 該当タスクの completed を反転させる
    pass
```

AI の補完を活用して実装します。

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

- `try-except` で数字以外の入力に対応
- `not task["completed"]` で True/False を反転
- 該当するタスクが見つからない場合のエラーメッセージも重要

### ステップ 2: 削除関数を実装する

以下のコードを追加します。

```py
def delete_task(tasks):
    # タスク一覧を表示
    # ユーザーに ID を入力してもらう
    # 確認メッセージを表示
    # 該当タスクを削除する
    pass
```

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

- `enumerate()` でインデックスと要素を同時に取得
- 削除前に確認メッセージを表示（誤操作防止）
- `tasks.pop(i)` でリストから削除

### ステップ 3: メインメニューに組み込む

```py
elif choice == "3":
    toggle_task(tasks)
elif choice == "4":
    delete_task(tasks)
```

### ステップ 4: 動作確認

- タスクの完了状態が切り替わること
- タスクが削除できること（確認メッセージが表示されること）

---

## 演習 3: CSV ファイルへの永続化（20 分）

この演習では、タスクを CSV ファイルに保存・読み込みする機能を実装します。これにより、アプリを終了してもデータが保持されます。

### ステップ 1: 必要なモジュールをインポートする

ファイルの先頭に以下を追加します。

```py
import csv
import os
```

- `csv` は CSV ファイルを読み書きするための標準ライブラリ
- `os` はファイルの存在確認などに使う

### ステップ 2: 読み込み関数を実装する

以下のコードを追加します。

```py
CSV_FILE = "tasks.csv"

def load_tasks():
    # CSV ファイルが存在しなければ空のリストを返す
    # 存在すれば読み込んでリストで返す
    pass
```

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

- CSV から読み込んだデータはすべて文字列になる
- `id` は `int()` で数値に変換
- `completed` は文字列 `"True"` との比較で真偽値に変換
- `encoding="utf-8"` で日本語も正しく読み込める

### ステップ 3: 保存関数を実装する

```py
def save_tasks(tasks):
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "title", "completed", "created_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)
```

### ステップ 4: メインループを修正する

`main()` 関数を以下のように修正します。

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

- 起動時に `load_tasks()` で読み込み
- データが変更されるたびに `save_tasks()` で保存
- グローバル変数 `tasks` は削除して、`main()` 内で管理

### ステップ 5: 動作確認

1. アプリを起動してタスクを追加
2. アプリを終了
3. 再度起動して、タスクが保持されていることを確認
4. `tasks.csv` ファイルが作成されていることを確認

---

## 演習 4: バリデーション関数を追加（10 分）

この演習では、ユーザー入力の検証（バリデーション）を行う関数を追加します。

### ステップ 1: バリデーション関数を実装する

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

- バリデーション関数は `(成功/失敗, メッセージまたは値)` のタプルを返す
- `strip()` で前後の空白を除去
- 定数 `MAX_TITLE_LENGTH` で長さの上限を設定

### ステップ 2: add_task に組み込む

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

### ステップ 3: 動作確認

- 空のタスク名を入力してエラーメッセージが表示されること
- 空白のみのタスク名でもエラーになること
