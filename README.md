# LLMBenchTesting

```
用于LLM批量测试
```
## 使用

1. 克隆本项目到本地
```
git clone https://github.com/KeLes-Coding/LLMBenchTesting.git
```

2. 安装依赖
```
pip install -r requirements.txt
```

3. 运行
   
windows*终端*运行：
```
python .\BenchingRequestV4.py
```
4. 在[LLMBenchingV3.py](LLMBenchingV3.py)处添加API_KEY

5. 更改query：

直接将query复制在[message.txt](message.txt)中即可

6. 更改API tools:
   > 1. 更改system_prompt：
   > 在[executor_script.py](executor_script.py)中更改：
   > ![](resources\system_prompt.png)
   > 2. 更改user_tools：
   > 在[executor_script.py](executor_script.py)中更改：
   > ![](resources\user_tools.png)
   > 3. 更改user_tools_response：
   > 在[executor_script.py](executor_script.py)中更改：
   > ![](resources\user_responses.png)
