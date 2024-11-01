import json
import sys
from LLMBenchingV3 import LLMPlanExecutor
import copy

# 初始化消息列表
messages = [
    {
        "role": "system",
        "content": """As a competent planner, you are able to skillfully call the APIs and app tools I provide to create a reasonable plan based on the queries I submit.
      Your response template should be as follows:
     {
  "OrderSteps": {
    "TotalSteps": totalsteps(int), // Total number of steps, integer type
    "Step1": {
      "Description": "Open Ele.me",
      "Action": "Tap on the Ele.me app icon to open it."
      "Results": {
        "Status": "Success",
        "Response":  {
        "DeliveryTab": "Tapped on the 'Delivery' tab at the top of the screen.",
        "AddAddress": "Selected 'Add New Address' and entered the delivery address:",
        "AddressDetails": {
          "Room": "Room 506",
          "Building": "Building A",
          "Location": "Sanlitun SOHO",
          "District": "Chaoyang District",
          "City": "Beijing"
        }
      }
    },
}""",
    },
    {
        "role": "user",
        "content": """任务是:""",
    },
]


def main():
    # 从命令行参数中获取message
    message_json = sys.argv[1]
    query_message = json.loads(message_json)

    # 打印message
    print("Received message:")
    # for msg in message:
    #     print(msg)
    print(query_message)

    combined_messages = copy.deepcopy(messages)
    combined_messages[-1]["content"] += query_message

    print(combined_messages)

    executor = LLMPlanExecutor()
    executor.messages = combined_messages
    executor.execute_plan()


if __name__ == "__main__":
    main()
