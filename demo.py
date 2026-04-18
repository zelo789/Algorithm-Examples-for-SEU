"""运行方式：python demo.py

这个文件不是完整单元测试，而是给你快速观察算法输入输出的示例。
"""

from algorithms.showcase import list_topics


def main() -> None:
    for topic in list_topics():
        print(f"\n=== {topic.title} ===")
        for example in topic.example_builder():
            print(f"{example.title}:", example.value)


if __name__ == "__main__":
    main()
