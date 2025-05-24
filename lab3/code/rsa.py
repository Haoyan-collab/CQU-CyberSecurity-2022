import random

# 检查一个数是否为素数
def is_prime(num):
    """
    检查一个数字是否为素数。
    Args:
        num: 要检查的整数。
    Returns:
        如果数字是素数，则返回 True，否则返回 False。
    """
    if not isinstance(num, int): # 确保输入是整数
        return False
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# 计算两个数的最大公约数 (GCD)
def gcd(a, b):
    """
    使用欧几里得算法计算两个数的最大公约数。
    Args:
        a: 第一个整数。
        b: 第二个整数。
    Returns:
        a 和 b 的最大公约数。
    """
    while b:
        a, b = b, a % b
    return a

# 计算模逆元
def mod_inverse(e, phi):
    """
    计算 e 模 phi 的模逆元 d，使得 (d * e) % phi = 1。
    Args:
        e: 整数。
        phi: 模数。
    Returns:
        e 模 phi 的模逆元。
    """
    m0, x0, x1 = phi, 0, 1
    e = e % phi
    if e < 0:
        e += phi
    temp_phi = m0
    while e > 1:
        if phi == 0:
            return None
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# 生成 RSA 密钥对
def generate_keypair(p, q):
    """
    根据两个素数 p 和 q 生成 RSA 公钥和私钥。
    Args:
        p: 第一个大素数。
        q: 第二个大素数。
    Returns:
        一个包含公钥 (e, n) 和私钥 (d, n) 的元组。
    """
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("输入的 p 和 q 都必须是素数。")
    if p == q:
        raise ValueError("p 和 q 不能相等。")

    n = p * q
    phi = (p - 1) * (q - 1)
    print(f"计算得到 n = p * q = {p} * {q} = {n}")
    print(f"计算得到 phi(n) = (p-1) * (q-1) = ({p-1}) * ({q-1}) = {phi}")

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    print(f"选择公钥指数 e = {e} (1 < e < {phi} 且 e 与 {phi} 互质)")

    d = mod_inverse(e, phi)
    if d is None:
        raise ValueError(f"无法为 e={e} 和 phi={phi} 计算模逆元 d。")
    print(f"计算私钥指数 d = {d} (使得 d*e mod phi = 1)")

    return ((e, n), (d, n))

# 加密消息
def encrypt(public_key, plaintext_message):
    """
    使用公钥加密消息。
    Args:
        public_key: 公钥元组 (e, n)。
        plaintext_message: 要加密的明文消息（整数）。
    Returns:
        加密后的密文（整数）。
    """
    e, n = public_key
    cipher_text = pow(plaintext_message, e, n)
    return cipher_text

# 解密消息
def decrypt(private_key, ciphertext_message):
    """
    使用私钥解密消息。
    Args:
        private_key: 私钥元组 (d, n)。
        ciphertext_message: 要解密的密文（整数）。
    Returns:
        解密后的明文（整数）。
    """
    d, n = private_key
    plain_text = pow(ciphertext_message, d, n)
    return plain_text

# 主函数
if __name__ == '__main__':
    print("RSA 加密器/解密器")
    print("-------------------------------------------------")

    p = 101  # 示例素数 p
    q = 103  # 示例素数 q

    if not is_prime(p) or not is_prime(q) or p == q:
        print("错误：预设的 p 和 q 值无效。请检查代码。")
        exit()

    print(f"使用的素数是 p = {p}, q = {q}")
    print("-------------------------------------------------")
    print("开始生成密钥对...")
    try:
        public_key, private_key = generate_keypair(p, q)
        print(f"\n生成的公钥 (e, n): {public_key}")
        print(f"生成的私钥 (d, n): {private_key}")
        print("-------------------------------------------------")

        while True:
            print("\n请选择要执行的操作:")
            print("1. 加密 (Encrypt)")
            print("2. 解密 (Decrypt)")
            print("3. 退出程序 (Exit Program)")
            main_choice = input("请输入选项 (1, 2, 或 3): ").strip()
            print("-------------------------------------------------")

            if main_choice == '1': # 加密
                print("您选择了加密操作。")
                sub_choice = ""
                while sub_choice not in ['1', '2']:
                    print("请选择加密类型:")
                    print("  1. 加密数字")
                    print("  2. 加密字符串")
                    sub_choice = input("  请输入选项 (1 或 2): ").strip()
                    if sub_choice not in ['1', '2']:
                        print("  无效的选项，请输入 1 或 2。")
                print("-------------------------------------------------")

                if sub_choice == '1': # 加密数字
                    print("您选择了加密数字。")
                    while True:
                        try:
                            message_str = input(f"请输入要加密的整数消息 (必须小于 n={public_key[1]} 且为非负数): ")
                            message_to_encrypt = int(message_str)
                            if message_to_encrypt >= public_key[1]:
                                print(f"错误：消息 {message_to_encrypt} 太大，必须小于 n ({public_key[1]})。")
                                continue
                            if message_to_encrypt < 0:
                                print("错误：消息必须是非负整数。")
                                continue
                            break
                        except ValueError:
                            print(f"错误：'{message_str}' 不是一个有效的整数。请重新输入。")
                    
                    print(f"\n要加密的明文数字: {message_to_encrypt}")
                    encrypted_message = encrypt(public_key, message_to_encrypt)
                    print(f"加密后的密文 (数字): {encrypted_message}")

                elif sub_choice == '2': # 加密字符串
                    print("您选择了加密字符串。")
                    text_message = input(f"请输入要加密的短文本 (每个字符的ASCII值都必须小于 n={public_key[1]}): ")
                    print(f"要加密的文本消息: {text_message}")

                    int_message = []
                    can_encrypt_all = True
                    if not text_message:
                        print("未输入文本消息。")
                        can_encrypt_all = False
                    
                    if can_encrypt_all:
                        for char_val in [ord(char) for char in text_message]:
                            if char_val >= public_key[1]:
                                print(f"错误：字符 '{chr(char_val)}' (ASCII: {char_val}) 的值大于或等于 n ({public_key[1]})。无法加密。")
                                can_encrypt_all = False
                                break
                            int_message.append(char_val)

                    if can_encrypt_all and int_message:
                        print(f"文本消息的 ASCII 表示: {int_message}")
                        encrypted_int_list = []
                        print("逐个字符加密:")
                        for i, val in enumerate(int_message):
                            encrypted_val = encrypt(public_key, val)
                            encrypted_int_list.append(encrypted_val)
                            print(f"  '{text_message[i]}' (ASCII:{val}) -> 加密为: {encrypted_val}")
                        
                        print(f"加密后的 ASCII 列表: {encrypted_int_list}")
                        encrypted_string_numeric_representation = "-".join(map(str, encrypted_int_list))
                        print(f"加密后的字符串的数字表示 (用 '-' 分隔): {encrypted_string_numeric_representation}")
                        
                        encrypted_chars_display = []
                        for num in encrypted_int_list:
                            try:
                                encrypted_chars_display.append(chr(num))
                            except ValueError: # 超出 chr 范围
                                encrypted_chars_display.append('?') 
                        print(f"加密后的字符串 (由加密数字直接转为字符, 仅供观察): {''.join(encrypted_chars_display)}")


            elif main_choice == '2': # 解密
                print("您选择了解密操作。")
                ciphertext_input_str = input(f"请输入要解密的密文 (如果是多个数字代表的字符串，请用空格或连字符'-'分隔，且每个数字都应小于 n={public_key[1]}): ").strip()
                
                parts = ciphertext_input_str.replace('-', ' ').split()
                if not parts or not parts[0]: # 处理空输入或只有分隔符的输入
                    print("错误：未输入有效的密文。")
                    continue

                decrypted_values = []
                all_parts_valid_numbers = True
                for part_str in parts:
                    try:
                        num = int(part_str)
                        if num >= private_key[1]: # private_key[1] is n
                             print(f"错误：密文部分 '{num}' 大于或等于 n ({private_key[1]})。无效密文。")
                             all_parts_valid_numbers = False
                             break
                        if num < 0:
                            print(f"错误：密文部分 '{num}' 为负数。无效密文。")
                            all_parts_valid_numbers = False
                            break
                        decrypted_values.append(decrypt(private_key, num))
                    except ValueError:
                        print(f"错误：密文部分 '{part_str}' 不是一个有效的数字。")
                        all_parts_valid_numbers = False
                        break
                
                if all_parts_valid_numbers and decrypted_values:
                    print("\n解密结果:")
                    if len(decrypted_values) == 1:
                        dec_num = decrypted_values[0]
                        print(f"  解密后的数字: {dec_num}")
                        try:
                            char_representation = chr(dec_num)
                            # 对于一些控制字符或不可打印字符，repr()可能更合适
                            if char_representation.isprintable():
                                print(f"  尝试转为字符 (请根据可读性自行判断是否合理）: '{char_representation}'")
                            else:
                                print(f"  尝试转为字符 (可能不可打印): repr -> {repr(char_representation)}")
                        except ValueError:
                            print(f"  尝试转为字符: (数字 {dec_num} 超出有效字符范围)")
                    else: # 多个解密值，认为是字符串
                        print(f"  解密后的数字列表 (原始ASCII码): {decrypted_values}")
                        try:
                            decrypted_string = "".join([chr(val) for val in decrypted_values])
                            print(f"  尝试转为字符串: \"{decrypted_string}\"")
                        except ValueError:
                            print("  尝试转为字符串失败：部分解密数字无法转换为有效字符。")
                elif not decrypted_values and all_parts_valid_numbers: # 输入为空但没有解析错误
                     print("错误：未输入有效的密文进行解密。")


            elif main_choice == '3': # 退出
                print("正在退出程序...感谢使用！")
                break
            
            else:
                print("无效的选项，请输入 1, 2, 或 3。")
            
            print("-------------------------------------------------")

    except ValueError as e:
        print(f"\n在处理过程中发生错误: {e}")
    except Exception as e:
        print(f"\n发生意外错误: {e}")

    print("\n程序已结束。")
