import AES
def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """
    对数据进行 PKCS#7 填充。
    :param data: 输入的字节数据
    :param block_size: 块大小，默认为 16（DES 的块大小）
    :return: 填充后的字节数据
    """
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding

def pkcs7_unpad(data: bytes) -> bytes:
    """
    去除 PKCS#7 填充。
    :param data: 填充后的字节数据
    :return: 去填充后的字节数据
    """
    padding_len = data[-1]  # 获取最后一个字节的值
    if padding_len > len(data):
        raise ValueError("Invalid padding.")
    return data[:-padding_len]
def main():
        choice = int(input("请输入 1 进行加密, 2 进行解密: "))
        if choice not in [1, 2]:
            print("无效选择")
            return
        
        Text = input("请输入文本:")
        if choice == 1:
            Text_hex = ''.join(format(ord(char), '02x') for char in Text if char.isprintable())
            data_bytes = bytes.fromhex(Text_hex)
            Text_hex = pkcs7_pad(data_bytes).hex()
        else:
            Text_hex = Text

        Key = input("请输入密钥(128位,16字节):") 
        Key_hex = ''.join(format(ord(char), '02x') for char in Key if char.isprintable())

        if len(Key) != 16:
            print("密钥长度不为 128 位。")
            return
        
        result = ''
  
        for i in range(0, len(Text_hex),32):
            temp_str1 = Text_hex[i:i+32]
            result_list = AES.Encryption(temp_str1, Key_hex) if choice == 1 else AES.Decryption(temp_str1, Key_hex)
            for i in range(4):
                for j in range(4):
                    result += result_list[j][i].lstrip("0x").zfill(2)
  
        if result:
            if choice == 1:
                print("加密后的密文:"+ result)
            else:
                data_bytes = bytes.fromhex(result)
                result = pkcs7_unpad(data_bytes).hex()
                byte_data = bytes.fromhex(result)
                result = ''.join(chr(b) for b in byte_data)
                print("解密后的明文:"+ result)
        else:
            print("处理失败，请检查输入。")

if __name__ == '__main__':
    main()
    input("按任意键退出...")