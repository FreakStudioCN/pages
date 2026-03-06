from translate import Translator
import functools


# ==================== 1. 基础翻译（指定源语言+目标语言）====================
def basic_translate():
    """英文转中文（指定源/目标语言）"""
    # 创建翻译器：from_lang=源语言代码，to_lang=目标语言代码
    translator = Translator(from_lang="en", to_lang="zh")
    text = "Hello, world! Python is a powerful programming language."
    try:
        result = translator.translate(text)
        print("【基础翻译】")
        print(f"原文：{text}")
        print(f"译文：{result}\n")
    except Exception as e:
        print(f"基础翻译失败：{e}\n")


# ==================== 2. 自动检测源语言 ====================
def auto_detect_translate():
    """自动检测源语言（法语→中文）"""
    # 只指定目标语言，源语言自动检测
    translator = Translator(to_lang="zh")
    text = "Bonjour le monde! Python est un langage de programmation puissant."
    try:
        result = translator.translate(text)
        print("【自动检测源语言】")
        print(f"原文：{text}")
        print(f"译文：{result}\n")
    except Exception as e:
        print(f"自动检测翻译失败：{e}\n")


# ==================== 3. 批量翻译 ====================
def batch_translate():
    """批量翻译英文单词→中文"""
    translator = Translator(from_lang="en", to_lang="zh")
    text_list = ["Apple", "Banana", "Orange", "Grape", "Watermelon"]
    results = []
    print("【批量翻译】")
    for text in text_list:
        try:
            res = translator.translate(text)
            results.append(res)
            print(f"{text} → {res}")
        except Exception as e:
            results.append(f"翻译失败：{e}")
            print(f"{text} → 翻译失败：{e}")
    print()


# ==================== 4. 从文件读取/写入翻译结果 ====================
def file_translate(input_file="input.txt", output_file="output.txt"):
    """从文件读取文本翻译，结果写入新文件"""
    translator = Translator(from_lang="en", to_lang="zh")
    try:
        # 读取源文件（确保input.txt存在，编码用utf-8）
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        # 翻译
        result = translator.translate(text)

        # 写入结果文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

        print("【文件翻译】")
        print(f"已从 {input_file} 读取文本并翻译，结果写入 {output_file}\n")
    except FileNotFoundError:
        print(f"文件翻译失败：未找到 {input_file} 文件\n")
    except Exception as e:
        print(f"文件翻译失败：{e}\n")


# ==================== 5. 指定翻译引擎（MyMemory）====================
def specify_engine_translate():
    """使用 MyMemory 引擎翻译（替代默认的 Google）"""
    # provider 指定引擎：mymemory（免费）、google（默认，需网络通畅）
    translator = Translator(provider="mymemory", from_lang="en", to_lang="zh")
    text = "Welcome to Python translation world."
    try:
        result = translator.translate(text)
        print("【指定 MyMemory 引擎】")
        print(f"原文：{text}")
        print(f"译文：{result}\n")
    except Exception as e:
        print(f"MyMemory 引擎翻译失败：{e}\n")


# ==================== 6. 缓存翻译结果（提升重复翻译效率）====================
def cached_translate_demo():
    """带缓存的翻译（避免重复翻译相同文本）"""
    # 初始化翻译器
    translator = Translator(from_lang="en", to_lang="zh")

    # 装饰器实现缓存：maxsize=缓存最大条数
    @functools.lru_cache(maxsize=128)
    def cached_translate(text):
        return translator.translate(text)

    # 第一次翻译（真实请求）
    text = "Hello, Python!"
    print("【缓存翻译】")
    res1 = cached_translate(text)
    print(f"第一次翻译：{res1}")

    # 第二次翻译（使用缓存，无网络请求）
    res2 = cached_translate(text)
    print(f"第二次翻译（缓存）：{res2}\n")


# ==================== 执行所有示例 ====================
if __name__ == "__main__":
    basic_translate()  # 基础翻译
    auto_detect_translate()  # 自动检测源语言
    batch_translate()  # 批量翻译
    # file_translate()         # 文件翻译（需先创建input.txt）
    specify_engine_translate()  # 指定 MyMemory 引擎
    cached_translate_demo()  # 缓存翻译