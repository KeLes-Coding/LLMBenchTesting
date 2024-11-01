import os
import json
from dashscope import Generation

class LLMPlanExecutor:
    def __init__(self, api_key=None, model="qwen-plus"):
        # 在此处更改API_KEY
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY") or "sk-cd4c82aa176c471d8307c4128b7aa134"
        self.model = model
        self.messages = []
        self.step_counter = 1
        self.total_steps = None
        self.result = []

    def get_response(self, messages):
        response = Generation.call(
            api_key=self.api_key,
            model=self.model,
            messages=messages,
            result_format="message",
        )
        return response

    def execute_plan(self):
        # 调用LLM生成第一步计划
        response = self.get_response(self.messages)

        if response.status_code == 200:
            self.process_step_result(response)
        else:
            self.handle_error(response)

        while self.step_counter <= self.total_steps:
            print(f"接下来执行: step{self.step_counter}\n")
            user_input = self.get_user_input()
            self.messages.append({'role': 'user', 'content': user_input})
            response = self.get_response(self.messages)

            if response.status_code == 200:
                self.process_step_result(response)
            else:
                self.handle_error(response)
                break

            if self.step_counter > self.total_steps:
                print("计划执行完毕！")
                self.print_formatted_result()
                print("计划打印完毕！")
                break

    def print_formatted_result(self):
        formatted_result = []
        for step_json in self.result:
            step_info = json.loads(step_json)
            formatted_result.append({
                "Step": step_info["Step"],
                "Description": step_info["Description"],
                "Action": step_info["Action"],
                "Result": step_info["Result"]
            })
        
        print(json.dumps(formatted_result, indent=4))


    def process_step_result(self, response):
        step_result = response.output.choices[0].message.content
        step_result = step_result.strip('```json').strip('```').strip()
        self.messages.append({'role': 'assistant', 'content': step_result})

        try:
            step_result_json = json.loads(step_result)
        except json.JSONDecodeError:
            print(f"Error parsing JSON: {step_result}")
            return

        print(f"LLM原始返回值: {json.dumps(step_result, indent=4)}")

        if self.total_steps is None:
            self.total_steps = step_result_json['OrderSteps']['TotalSteps']

        print(f"总步骤数: {self.total_steps}")

        step_info = {
            "Step": self.step_counter,
            "Description": step_result_json['OrderSteps'][f'Step{self.step_counter}']['Description'],
            "Action": step_result_json['OrderSteps'][f'Step{self.step_counter}']['Action'],
            "Result": step_result_json['OrderSteps'][f'Step{self.step_counter}']['Results']
        }
        print(json.dumps(step_info, indent=4))
        self.result.append(json.dumps(step_info, indent=4))

        self.step_counter += 1

    def handle_error(self, response):
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    def get_user_input(self):
        print(f"请输入step {self.step_counter - 1} 的返回值：")
        user_input = []
        while True:
            try:
                line = input()
                if line.strip() == "":
                    break
                user_input.append(line)
            except EOFError:
                break

        user_input_2 = f"step {self.step_counter - 1} 的返回值为：\n{user_input}，\n接下来执行step {self.step_counter}："
        print(f"用户输入: {user_input_2}")
        return user_input_2
    


# 示例使用
# if __name__ == "__main__":
#     executor = LLMPlanExecutor()
#     executor.messages = messages
#     executor.execute_plan()
