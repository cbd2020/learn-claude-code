#!/usr/bin/env python3
"""
CLI 计算器 - 支持基本数学运算
"""

import sys
import re


def calculate(expression):
    """
    计算数学表达式
    支持运算符: +, -, *, /, **, //, %
    支持括号和数学函数
    """
    try:
        # 移除空格
        expression = expression.replace(" ", "")
        
        # 验证表达式只包含合法字符
        if not re.match(r'^[\d+\-*/.() %**//]+$', expression):
            return "错误: 表达式包含非法字符"
        
        # 计算表达式
        result = eval(expression)
        return result
    except ZeroDivisionError:
        return "错误: 除数不能为零"
    except SyntaxError:
        return "错误: 表达式语法错误"
    except Exception as e:
        return f"错误: {str(e)}"


def interactive_mode():
    """
    交互模式 - 持续接收用户输入
    """
    print("=" * 50)
    print("CLI 计算器 - 交互模式")
    print("=" * 50)
    print("支持的运算符: +, -, *, /, **(幂), //(整除), %(取模)")
    print("支持括号: ()")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'help' 查看帮助")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            
            # 检查帮助命令
            if user_input.lower() == 'help':
                print("\n使用示例:")
                print("  2 + 3         => 5")
                print("  10 * 5        => 50")
                print("  15 / 3        => 5.0")
                print("  2 ** 8        => 256")
                print("  17 // 3       => 5")
                print("  17 % 3        => 2")
                print("  (2 + 3) * 4   => 20")
                print("  3.14 * 2      => 6.28")
                continue
            
            # 空输入跳过
            if not user_input:
                continue
            
            # 计算并显示结果
            result = calculate(user_input)
            print(f"= {result}")
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except EOFError:
            print("\n再见！")
            break


def main():
    """
    主函数 - 支持命令行参数和交互模式
    """
    # 如果提供了命令行参数，直接计算
    if len(sys.argv) > 1:
        # 将所有参数连接成一个表达式
        expression = " ".join(sys.argv[1:])
        result = calculate(expression)
        print(result)
    else:
        # 否则进入交互模式
        interactive_mode()


if __name__ == "__main__":
    main()
