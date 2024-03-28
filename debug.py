import datetime
import traceback

# from openai import OpenAI

# def debug_chat(prompt):
#     base_url = "https://api.132999.xyz/v1"

#     api_key = "sk-AWlop3ALe1nenKwt27E500Da2c224a2984E7D585390d8bA2"

#     client = OpenAI(
#         api_key=api_key,
#         base_url=base_url
#     )

#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         model="gpt-4-1106-preview",
#     )

#     print(chat_completion.choices[0].message.content)

# debug_chat("hello")


def warning(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    traceback_info = traceback.extract_stack()[-2]
    file_name, line_number, _, _ = traceback_info
    print("\033[97m" + f"{current_time}" + "\033[0m" + "\033[93m" f" - Warning in {file_name} at line {line_number}: {msg}" + "\033[0m")

def okf(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\033[97m" + f"{current_time}" + "\033[0m" + " - " + "\033[92m" + f"{msg}" + "\033[0m")

def error(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    traceback_info = traceback.extract_stack()[-2]
    file_name, line_number, _, _ = traceback_info
    print("\033[97m" + f"{current_time}" + "\033[0m" + "\033[91m" f" - Error in {file_name} at line {line_number}: {msg}" + "\033[0m")

def doing(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\033[97m" + f"{current_time}" + "\033[0m" + " - " + "\033[94m" + f"{msg}....." + "\033[0m")



