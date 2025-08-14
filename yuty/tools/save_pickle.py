import pickle


def save_variable_to_pkl(var, filename):
    """将变量保存为pkl文件"""
    try:
        with open(filename, 'wb') as f:
            pickle.dump(var, f)
        print(f"变量已成功保存到 {filename}")
    except Exception as e:
        print(f"保存失败: {e}")


def load_variable_from_pkl(filename):
    """从pkl文件加载变量"""
    try:
        with open(filename, 'rb') as f:
            var = pickle.load(f)
        print(f"已从 {filename} 加载变量")
        return var
    except FileNotFoundError:
        print(f"错误: 文件 {filename} 未找到")
    except Exception as e:
        print(f"加载失败: {e}")
    return None


# 示例用法
if __name__ == "__main__":
    # 创建一个示例变量（可以是任何Python对象）
    example_data = {
        "name": "测试数据",
        "numbers": [1, 2, 3, 4, 5],
        "values": (10.5, 20.3, 30.7),
        "active": True
    }

    # 保存变量
    save_variable_to_pkl(example_data, "example_data.pkl")

    # 加载变量
    loaded_data = load_variable_from_pkl("example_data.pkl")

    # 验证加载的数据
    if loaded_data:
        print("\n加载的数据内容:")
        print(loaded_data)
