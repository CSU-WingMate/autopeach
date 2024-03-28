git clone https://github.com/google/boringssl.git
git clone https://github.com/openssl/openssl.git
git clone https://github.com/eclipse-cyclonedds/cyclonedds.git
git clone https://github.com/eclipse/mosquitto.git
git clone https://github.com/imp/dnsmasq.git
git clone https://github.com/DNSPod/dnspod-sr.git
git clone https://github.com/pymumu/smartdns.git
git clone https://github.com/obgm/libcoap.git

api key: sk-AWlop3ALe1nenKwt27E500Da2c224a2984E7D585390d8bA2


实验进行的阶段：
    一. 初始化
        1. 适配协议实现的客户端和服务端，捕获二者交互的流量；
            流量文件命名：协议名_项目名_tra_序号.pcap
            运行命令：tcpdump -w {traffic name}.pcap -i lo port {port num}

        2. 将流量解析成种子文件和配置文件；
            种子文件命名：协议名_项目名_seed_序号
            运行命令：parse.py {traffic file} {seed file} {conf file}

        3. 借助LLM生成pits；
            运行命令：pits_gen.sh 种子文件 配置文件 apikey 


    二. 测试及模板精化
        1. 运行测试，记录测试结果；
        2. 将测试信息反馈给精化模块进行模板精化；
        3. 保存测试结果；

    三. 结果整理
        1. 通过shell脚本进行结果统计；