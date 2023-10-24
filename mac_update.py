import paramiko
import re

def update_mac_address():
    # 创建SSH客户端实例
    ssh = paramiko.SSHClient()
    
    # 自动添加未知主机的主机密钥（这是不安全的，仅用于测试！）
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # 连接到路由器
    ssh.connect('192.168.0.1', username='', password='')
    
    # 运行一个命令来查看网络配置
    stdin, stdout, stderr = ssh.exec_command('cat /etc/config/network')
    
    # 获取输出并解码
    network_config = stdout.read().decode()
    
    # 使用正则表达式找到所有的MAC地址
    mac_addresses = re.findall(r"option macaddr '([0-9A-Fa-f:]+)'", network_config)
    
    # 更新wan和wan6的MAC地址
    for mac in mac_addresses:
        # 递增MAC地址
        new_mac = increment_mac_address(mac)
        
        # 使用sed命令更新MAC地址
        sed_command = f"sed -i 's/{mac}/{new_mac}/g' /etc/config/network"
        ssh.exec_command(sed_command)
    
    ssh.exec_command('ifdown wan')
    ssh.exec_command('ifup wan')
    ssh.exec_command('ifdown wan6')
    ssh.exec_command('ifup wan6')
    print("Ah ♂ yes sir")
    # 最后，关闭SSH连接
    ssh.close()

# 定义用于递增MAC地址的函数（这里简单复制上面的函数代码）
def increment_mac_address(mac_address):
    components = mac_address.split(":")
    last_byte = int(components[-1], 16)
    last_byte = (last_byte + 1) % 256
    last_byte_hex = format(last_byte, '02X')
    components[-1] = last_byte_hex
    new_mac_address = ":".join(components)
    return new_mac_address

# 运行函数
update_mac_address()
