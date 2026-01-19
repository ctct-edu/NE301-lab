"""
ToDo アプリ - セッション3終了時点
機能: メニュー表示、タスク一覧表示、タスク追加
"""

from datetime import datetime


def show_tasks(tasks):
    """タスク一覧を表示する"""
    if not tasks:
        print("タスクがありません。")
        return

    print("\n----- タスク一覧 -----")
    for task in tasks:
        status = "[x]" if task["completed"] else "[ ]"
        print(f"{status} {task['id']}. {task['title']} ({task['created_at']})")
    print("----------------------")


def add_task(tasks):
    """新しいタスクを追加する"""
    title = input("タスク名を入力してください: ")

    if not title.strip():
        print("タスク名を入力してください。")
        return

    # 新しい ID を決定
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1

    # 現在日時を取得
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 新しいタスクを作成
    new_task = {"id": new_id, "title": title.strip(), "completed": False, "created_at": created_at}

    tasks.append(new_task)
    print(f"タスク「{title.strip()}」を追加しました。")


def main():
    # 初期データ（動作確認用）
    tasks = [
        {"id": 1, "title": "牛乳を買う", "completed": False, "created_at": "2024-01-15 10:30"},
        {"id": 2, "title": "メールを返信する", "completed": True, "created_at": "2024-01-14 09:00"},
    ]

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
            add_task(tasks)
        elif choice == "3":
            print("（この機能はセッション4で実装します）")
        elif choice == "4":
            print("（この機能はセッション4で実装します）")
        elif choice == "5":
            print("終了します。")
            break
        else:
            print("無効な選択です。1-5 の数字を入力してください。")


if __name__ == "__main__":
    main()
