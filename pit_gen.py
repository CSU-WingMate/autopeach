import os
import sys
import configparser

from debug import *
from openai import OpenAI

def extract_content(string):
    start_index = string.find('```xml')
    end_index = string.find('```', start_index + 6)
    
    if start_index != -1 and end_index != -1:
        return string[start_index + 6: end_index]
    else:
        error("Automated generation of DataModel failed.")
        sys.exit(-1)

def dataModel_gen(api_key, data_path, save_pit_path):
    doing("DataModel generating")

    base_url = "https://api.132999.xyz/v1"

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    if not any(file.endswith('.txt') for file in os.listdir(data_path)):
        error(f'No .txt files found in {data_path}.')
        sys.exit(-1)
    data_files = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".txt"):
                data_files.append(os.path.join(root, file))
    
    preprompt = "Generate the PIT file DataModel section of the fuzzer Peach based on the following data information:"
    ordprompt = "No need to explain, just provide the generated PIT file DataModel section."

    for data_file in data_files:

        data_file_name = os.path.basename(data_file)
        datamodel_file_name = data_file_name[:-8] + 'DataModel.xml'
        save_pit_path = save_pit_path + datamodel_file_name

        lines = ()

        with open(data_file, 'r') as file:
            lines = tuple(file.readlines())
        
        for line in lines:

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"{preprompt} + {line} + {ordprompt}"
                    }
                ],
                model="gpt-4-1106-preview",
            )

            with open(save_pit_path, 'a' if os.path.exists(save_pit_path) else 'w') as file:
                dataModel = extract_content(chat_completion.choices[0].message.content)
                file.write(dataModel)
                file.write('\n')
    
    xml_head_content = '''<?xml version="1.0" encoding="utf-8"?>
<Peach xmlns="http://peachfuzzer.com/2012/Peach" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://peachfuzzer.com/2012/Peach ../peach.xsd">
'''
    xml_end_content = "</Peach>"

    with open(save_pit_path, 'r') as file:
        content = file.readlines()
    content.insert(0, xml_head_content)
    content.append(xml_end_content)

    with open(save_pit_path, 'w') as file:
        file.writelines(content)
    
    okf("DataModel generation completed.")
    
def stateModel_gen():
    
    pass

def agent_gen(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file, encoding='utf-8')

    executable = config.get('Agent', 'Executable')
    arguments = config.get('Agent', 'Arguments')
    restart_on_each_test = config.getboolean('Agent', 'RestartOnEachTest')
    fault_on_early_exit = config.getboolean('Agent', 'Faultonearlyexit')
    no_cpu_kill = config.getboolean('Agent', 'NoCpuKill')
    start_on_call = config.get('Agent', 'StartOnCall')
    wait_for_exit_on_call = config.get('Agent', 'WaitForExitOnCall')
    wait_for_exit_timeout = config.get('Agent', 'WaitForExitTimeout')

    if not executable:
        error("Error reading conf.conf file. Parameter 'Executable' is not initialized.")
        sys.exit(-1)

    agent_content = f'''
    <Agent name="LinAgent">
        <Monitor class="Process">
            <Param name="Executable" value="{executable}"/>'''

    if arguments is not None:
        agent_content += f'''
            <Param name="Arguments" value="{arguments}"/>'''

    if isinstance(restart_on_each_test, bool):
        if restart_on_each_test:
            agent_content += f'''
            <Param name="RestartOnEachTest" value="{restart_on_each_test}"/>'''
    else:
        error(f"Error reading conf.conf file. Parameter value {restart_on_each_test} is illegal (not of bool type)")
        sys.exit(-1)

    if isinstance(fault_on_early_exit, bool):
        if fault_on_early_exit:
            agent_content += f'''
            <Param name="Faultonearlyexit" value="{fault_on_early_exit}"/>'''
    else:
        error(f"Error reading conf.conf file. Parameter value {fault_on_early_exit} is illegal (not of bool type)")
        sys.exit(-1)

    if isinstance(no_cpu_kill, bool):
        if no_cpu_kill:
            agent_content += f'''
                <Param name="NoCpuKill" value="{no_cpu_kill}"/>'''
    else:
        error(f"Error reading conf.conf file. Parameter value {no_cpu_kill} is illegal (not of bool type)")
        sys.exit(-1)

    # 这里需要再细化一下
    if start_on_call is None:
        agent_content += f'''
            <Param name="StartOnCall" value="{start_on_call}"/>
'''

    if wait_for_exit_on_call is None:
        agent_content += f'''
            <Param name="WaitForExitOnCall" value="{wait_for_exit_on_call}"/>
'''

    if wait_for_exit_timeout != 'disabled':
        agent_content += f'''
            <Param name="WaitForExitTimeout" value="{wait_for_exit_timeout}"/>
'''

    agent_content += f'''
        </Monitor>
    </Agent>
'''
    return agent_content
    
def test_gen(conf_file, stateModel_name):
    
    config = configparser.ConfigParser()
    config.read(conf_file, encoding='utf-8')

    test_content = f'''    <Test name="Default">
        <Agent ref="LinAgent" platform="linux"/>
        <StateModel ref="{stateModel_name}"/>'''

    publisher_class = config.get('Publisher', 'class')
    publisher_para_host = config.get('Publisher', 'Host')
    publisher_para_port = config.getint('Publisher', 'Port')
    publisher_para_timeout = config.getint('Publisher', 'Timeout')

    test_content += f'''
        <Publisher class="{publisher_class}" name="multicast">
            <Param name="Host" value="{publisher_para_host}" />
            <Param name="Port" value="{publisher_para_port}" />'''

    if publisher_para_timeout != 3000:
        test_content += f'''
            <Param name="Timeout" value="{publisher_para_timeout}" />'''

    if publisher_class == 'TcpClient':

        publisher_para_connecttimeout = config.getint('Publisher', 'Connecttimeout')
        if publisher_para_connecttimeout != 10000:
            test_content += f'''
            <Param name="Connecttimeout" value="{publisher_para_connecttimeout}" />'''

    elif publisher_class == 'Udp':
        publisher_para_srcport = config.get('Publisher', 'Srcport')
        if not publisher_para_srcport:
            pass
        else:
            try:
                srcport = int(publisher_para_srcport)
                test_content += f'''
            <Param name="Srcport" value="{srcport}" />'''
            except ValueError:
                error(f"Srcport {publisher_para_srcport} illegal")
        
        publisher_para_interface = config.get('Publisher', 'Interface')
        if publisher_para_interface:
            test_content += f'''
            <Param name="Interface" value="{publisher_para_interface}" />'''

        publisher_para_maxMTU = config.getint('Publisher', 'maxMTU')
        if publisher_para_maxMTU != 131070:
            test_content += f'''
            <Param name="maxMTU" value="{publisher_para_maxMTU}" />'''

        publisher_para_minMTU = config.getint('Publisher', 'minMTU')
        if publisher_para_minMTU != 1280:
            test_content += f'''
            <Param name="minMTU" value="{publisher_para_minMTU}" />'''

    else:
        error(f"Error reading conf.conf file. publisher_class = {publisher_class} not supported.")
        sys.exit(-1)

    test_content += f'''
        </Publisher>'''


    strategy_class = config.get('Strategy', 'class')
    
    if strategy_class not in ('Random', 'Sequential', 'RandomDeterministic'):
        error(f"Error reading conf.conf file. strategy_class = {strategy_class} not supported.")
    
    if strategy_class == 'Random':
        test_content += f'''
        <Strategy class="{strategy_class}">'''

        strategy_para_MaxFieldsToMutate = config.getint('Strategy', 'MaxFieldsToMutate')
        strategy_para_Switchcout = config.getint('Strategy', 'Switchcout')

        if strategy_para_MaxFieldsToMutate != 6:
            test_content += f'''
            <Param name="MaxFieldsToMutate" value="{strategy_para_MaxFieldsToMutate}"/>'''

        if strategy_para_Switchcout != 200:
            test_content += f'''
            <Param name="Switchcout" value="{strategy_para_Switchcout}"/>'''

        test_content += f'''
        </Strategy>'''
    else:
        test_content += f'''
        <Strategy class="{strategy_class}"/>'''


    logger_class = config.get('Logger', 'class')

    if logger_class != 'File':
        error(f"Error reading conf.conf file. logger_class = {logger_class} not supported.")
        sys.exit(-1)

    logger_para_Path = config.get('Logger', 'Path')
    test_content += f'''
        <Logger class="{logger_class}">
		<Param name="Path" value="{logger_para_Path}" />
	</Logger>'''

    test_content += f'''
    </Test>'''
    
    return test_content

# print(agent_gen('conf.conf'))
# print(test_gen('conf.conf', 'mqtt'))
dataModel_gen('sk-AWlop3ALe1nenKwt27E500Da2c224a2984E7D585390d8bA2', './result/', './result/')
