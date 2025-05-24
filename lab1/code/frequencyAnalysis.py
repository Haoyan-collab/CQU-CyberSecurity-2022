from collections import Counter

# 目标频率顺序
TARGET_ORDER = [
    'E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H',
    'L', 'D', 'U', 'C', 'F', 'M', 'W', 'Y', 'G',
    'P', 'B', 'V', 'K', 'X', 'J', 'Q', 'Z'
]

def frequency_decrypt(ciphertext, custom_mapping=None):
    """
    改进版频率分析解密（支持手动修正映射）
    :param ciphertext: 密文字符串
    :param custom_mapping: 手动修正的映射字典（例如 {'K':'T'}）
    :return: 解密后的明文字符串
    """
    # 预处理文本
    filtered = [c.upper() for c in ciphertext if c.isalpha()]
    if not filtered:
        return "无法解密：输入文本中未包含字母字符。"
    
    # 统计频率并排序
    counter = Counter(filtered)
    sorted_letters = sorted(counter.keys(), key=lambda x: (-counter[x], x))
    
    # 生成自动映射表
    auto_mapping = {}
    for cipher_char, target_char in zip(sorted_letters, TARGET_ORDER):
        auto_mapping[cipher_char] = target_char
    
    # 合并手动修正映射（覆盖自动映射）
    final_mapping = {**auto_mapping, **(custom_mapping or {})}
    
    # 解密文本
    decrypted = []
    for c in ciphertext:
        if c.isalpha():## 如果是字母则开始解密
            original_upper = c.isupper()
            cipher_char = c.upper()
            decrypted_char = final_mapping.get(cipher_char, c)
            decrypted.append(decrypted_char.upper() if original_upper else decrypted_char.lower())
        else:
            decrypted.append(c)## 非字母字符保留
    return ''.join(decrypted)

def show_frequency_table(ciphertext):
    """显示频率对照表"""
    filtered = [c.upper() for c in ciphertext if c.isalpha()]
    counter = Counter(filtered)
    sorted_freq = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    
    print("密文字母频率排序（从高到低）：")
    print("-" * 30)
    for char, count in sorted_freq:
        print(f"{char}: {count}次")
    print("\n目标字母顺序（从高到低）：")
    print(" ".join(TARGET_ORDER))

if __name__ == "__main__":
    ciphertext = "WTWHEQTOKEBPELHTPUKOKEKCKCWIQTKCTPTOKREKQTTQHFEKJQWMWMRUKBPEKLHTOQTBEPJTOKHKOPMPEKCCKQCZKTQFKWMIEKQHKCCKAPTWPMTPTOQTIQLHKBPEZOWIOTOKDRQAKTOKXQHTBLXXJKQHLEKPBCKAPTWPMTOQTZKOKEKOWROXDEKHPXAKTOQTTOKHKCKQCHOQXXMPTOQAKCWKCWMAQWMTOQTTOWHMQTWPMLMCKERPCHOQXXOQAKQMKZUWE TOPBBEKKCPJQMCTOQTRPAKEMJKMTPBTOKSKPSXKUDTOKSKPSXKBPETOKSKPSXKHOQXXMPTSK EWHOBEPJ TOKKQETO".replace(" ", "")
  
    # 步骤1：显示频率对照表
    show_frequency_table(ciphertext)
    
    # 步骤2：根据观察结果添加手动修正
    custom_mapping = {
        'W': 'I',
        'T': 'T',
        'H': 'S',
        'E': 'R',
        'Q': 'A',
        'O': 'H',
        'K': 'E',
        'B': 'F',
        'P': 'O',
        'L': 'U',
        'U': 'B',
        'C': 'D',
        'I': 'C',
        'R': 'G',
        'F': 'K',
        'J': 'M',
        'M': 'N',
        'Z': 'W',
        'A': 'V',
        'D': 'Y',
        'X': 'L',
        'S': 'P'
    }
    
    # 步骤3：解密并输出结果
    decrypted = frequency_decrypt(ciphertext, custom_mapping)
    print("\n解密结果：\n" + decrypted)