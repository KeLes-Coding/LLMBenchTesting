from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
import threading
import subprocess
import json
from LLMBenchingV3 import LLMPlanExecutor

messages_list = []

# 读取 message.txt 文件内容
with open("message.txt", "r") as file:
    messages_list = [line.strip().split("\n") for line in file.readlines()]

result_message = []

for i, message in enumerate(messages_list):
    combined_messages = []
    combined_messages = (
        message[0]
        + "我们从step1开始，我需要step1以及对应的result，result用模拟值代替，要求合理并贴合实际。"
    )
    # combined_messages = copy.deepcopy(messages)
    # combined_messages[-1]["content"] += (
    #     "\n "
    #     + message[0]
    #     + "我们从step1开始，我需要step1以及对应的result，result用模拟值代替，要求合理并贴合实际。"
    # )
    result_message.append(combined_messages)


# print(result_message)


def start_terminal(program_path, message):
    # 将message转换为JSON字符串
    message_json = json.dumps(message)
    # 使用subprocess.Popen来启动一个新的终端窗口并运行第二个程序，传递message作为参数
    subprocess.Popen(
        ["start", "cmd", "/k", "python", program_path, message_json], shell=True
    )


def main():
    program_path = "executor_script_APP.py"

    for message in result_message:
        start_terminal(program_path, message)


if __name__ == "__main__":
    main()
