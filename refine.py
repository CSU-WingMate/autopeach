import pyshark
import os

def extract_data_from_pcap(pcap_path, output_path):
    """
    从指定的pcap文件中提取data字段,并将其保存到指定的输出路径。

    参数:
    pcap_path (str): pcap文件的路径。
    output_path (str): 输出文件的保存路径。
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # 读取pcap文件
        cap = pyshark.FileCapture(pcap_path, only_summaries=False, keep_packets=False)
        
        # 打开输出文件准备写入数据
        with open(output_path, 'w') as output_file:
            for packet in cap:
                try:
                    # 尝试获取data层的数据
                    if 'DATA' in packet:
                        data_layer = packet['DATA']
                        # 将数据写入文件
                        output_file.write(str(data_layer) + '\n')
                except AttributeError:
                    # 某些包可能没有DATA层
                    continue
    except Exception as e:
        print(f"Error occurred: {e}")

# 使用示例
pcap_path = './result/002.pcap'
output_path = './result/002.txt'
extract_data_from_pcap(pcap_path, output_path)


