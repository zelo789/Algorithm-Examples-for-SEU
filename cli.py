"""算法样例命令行入口。

运行方式：
python cli.py --list
python cli.py sorting
python cli.py backtracking
python cli.py all
"""

from __future__ import annotations

import argparse
from algorithms.showcase import TOPICS, build_topic_examples, list_topics


def _show(title: str, result: object) -> None:
    print(f"\n[{title}]")
    print(result)


def run_topic(topic: str) -> None:
    for example in build_topic_examples(topic):
        _show(example.title, example.value)


def run_all() -> None:
    for topic in TOPICS:
        print(f"\n=== {TOPICS[topic].title} ===")
        run_topic(topic)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Python 算法样例命令行入口")
    parser.add_argument(
        "topic",
        nargs="?",
        default="all",
        help="可选：all, sorting, dp, graph, divide, theory, backtracking",
    )
    parser.add_argument("--list", action="store_true", help="列出可运行主题")
    args = parser.parse_args(argv)

    if args.list:
        for topic in list_topics():
            print(f"{topic.slug:12s} {topic.description}")
        print("all      运行全部示例")
        print("visualize 使用 python visualize.py 打开本地动画演示")
        return

    if args.topic == "all":
        run_all()
        return

    if args.topic not in TOPICS:
        parser.error(f"未知主题：{args.topic}")
    run_topic(args.topic)


if __name__ == "__main__":
    main()
