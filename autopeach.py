import os
import sys
# import logging
import argparse

import parse
import pit_gen
import debug

""" 
    -i          Path to save traffic files      (存放流量文件的路径)
    -o          Path to save fuzzing results    (保存测试结果的路径)
    -api        Open api key                    (open api key)
    -pit        Path to save the Pit files      (保存pit文件的路径)
    -conf       Path to conf.conf file          (指定配置文件的路径)
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    """
        type: 表示输入参数的类型,可以是int, str, float
        required:指定该参数是否是必需的。默认为 False,即可选参数。如果将其设置为 True,则在命令行中必须提供该参数，否则将引发错误。
        action:指定参数的动作。常见的动作包括 'store'(默认动作，将参数值存储为属性)、'store_true'(将参数解析为 True)、
                                            'store_false'(将参数解析为 False)、'append'(将多个参数值存储为列表)等。
        choices:指定参数的可选值列表。如果设置了该参数,那么命令行中提供的值必须是列表中的一个,否则将引发错误。                                    
    """
    parser.add_argument('-i',    type=str, required=True, help='Path to save traffic files')
    parser.add_argument('-o',    type=str, required=True, help='Path to save fuzzing results')
    parser.add_argument('-api',  type=str, required=True, help='Open api key')
    parser.add_argument('-pit',  type=str, required=True, help='Path to save the Pit files')
    parser.add_argument('-conf', type=str, required=True, help='Path to conf.conf file')

    args = parser.parse_args()

    open_api_key = args.api

    if not os.path.exists(args.i):
        debug.error(f"Path '{args.i}' does not exist.")
        sys.exit(-1)
    else:
        traffic_path = args.i
    
    if not os.path.exists(args.o):
        os.makedirs(args.o)
        test_result_path = args.o
    else:
        test_result_path = args.o

    if not os.path.exists(args.pit):
        os.makedirs(args.pit)
        save_pit_path = args.pit
    else:
        save_pit_path = args.pit

    if os.path.exists(os.path.join(args.conf, 'conf.conf')):
        conf_path = args.conf
    else:
        debug.error(f'No conf.conf file in {args.conf}')
        sys.exit(-1)

    print("\n\033[94m---------- autopeach ----------\033[0m")
    print(f'保存流量的文件夹:     {traffic_path}')
    print(f'保存测试结果的文件夹: {test_result_path}')
    print(f'给定的api的值:        {open_api_key}')
    print(f'保存pit文件的文件夹:  {save_pit_path}')
    print(f'指定配置文件的路径:   {conf_path}')
    print("\033[94m-------------------------------\033[0m")

    pcap_files = parse.read_pcap_files(traffic_path)
    parse.extract_pcap_data(pcap_files)
