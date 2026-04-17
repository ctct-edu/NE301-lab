"""
ToDo アプリ - セッション4終了時点
機能: 全機能（表示、追加、完了切り替え、削除、CSV 永続化、バリデーション）
"""

import csv
import os
from datetime import datetime

# 定数
DATE_FORMAT = "%Y-%m-%d %H:%M"
CSV_FILE = "tasks.csv"
MAX_TITLE_LENGTH = 100


def load_tasks():
    """CSV ファイルからタスクを読み込む"""
    tasks = []

    if not os.path.exists(CSV_FILE):
        return tasks

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = {
                "id": int(row["id"]),
                "title": row["title"],
                "completed": row["completed"] == "True",
                "created_at": row["created_at"],
            }
            tasks.append(task)

    return tasks


def save_tasks(tasks):
    """タスクを CSV ファイルに保存する"""
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "title", "completed", "created_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)


def validate_title(title):
    """タイトルのバリデーションを行う"""
    if not title:
        return False, "タスク名を入力してください。"

    stripped = title.strip()
    if not stripped:
        return False, "タスク名を入力してください。"

    if len(stripped) > MAX_TITLE_LENGTH:
        return False, f"タスク名は{MAX_TITLE_LENGTH}文字以内で入力してください。"

    return True, stripped


def find_task_by_id(tasks, task_id):
    """ID でタスクを検索する"""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def get_task_id_input(prompt):
    """タスク ID の入力を取得し、整数に変換する"""
    task_id = input(prompt)
    try:
        return int(task_id), None
    except ValueError:
        return None, "数字を入力してください。"


def get_next_id(tasks):
    """次のタスク ID を取得する"""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def show_tasks(tasks):
    """タスク一覧を表示する"""
    if not tasks:
        print("\nタスクがありません。")
        return

    print("\n----- タスク一覧 -----")
    for task in tasks:
        status = "[x]" if task["completed"] else "[ ]"
        print(f"{status} {task['id']}. {task['title']} ({task['created_at']})")
    print("----------------------")


def add_task(tasks):
    """新しいタスクを追加する"""
    title = input("タスク名を入力してください: ")

    is_valid, result = validate_title(title)
    if not is_valid:
        print(result)
        return False

    title = result

    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False,
        "created_at": datetime.now().strftime(DATE_FORMAT),
    }

    tasks.append(new_task)
    print(f"タスク「{title}」を追加しました。")
    return True


def toggle_task(tasks):
    """タスクの完了/未完了を切り替える"""
    if not tasks:
        print("\nタスクがありません。")
        return False

    show_tasks(tasks)
    task_id, error = get_task_id_input("切り替えるタスクの番号を入力してください: ")

    if error:
        print(error)
        return False

    task = find_task_by_id(tasks, task_id)
    if task is None:
        print(f"ID {task_id} のタスクが見つかりません。")
        return False

    task["completed"] = not task["completed"]
    status = "完了" if task["completed"] else "未完了"
    print(f"タスク「{task['title']}」を{status}にしました。")
    return True


def delete_task(tasks):
    """タスクを削除する"""
    if not tasks:
        print("\nタスクがありません。")
        return False

    show_tasks(tasks)
    task_id, error = get_task_id_input("削除するタスクの番号を入力してください: ")

    if error:
        print(error)
        return False

    task = find_task_by_id(tasks, task_id)
    if task is None:
        print(f"ID {task_id} のタスクが見つかりません。")
        return False

    # 削除前の確認
    confirm = input(f"タスク「{task['title']}」を削除しますか？ (y/n): ")
    if confirm.lower() != "y":
        print("削除をキャンセルしました。")
        return False

    tasks.remove(task)
    print(f"タスク「{task['title']}」を削除しました。")
    return True


def main():
    """メイン関数。アプリケーションのエントリーポイント。"""
    tasks = load_tasks()

    while True:
        print("\n===== ToDo アプリ =====")
        print("1. タスク一覧を表示")
        print("2. タスクを追加")
        print("3. タスクを完了/未完了に切り替え")
        print("4. タスクを削除")
        print("5. 終了")
        print("======================")

        choice = input("選択してください (1-5): ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            if add_task(tasks):
                save_tasks(tasks)
        elif choice == "3":
            if toggle_task(tasks):
                save_tasks(tasks)
        elif choice == "4":
            if delete_task(tasks):
                save_tasks(tasks)
        elif choice == "5":
            print("終了します。")
            break
        else:
            print("無効な選択です。1-5 の数字を入力してください。")


if __name__ == "__main__":
    main()
