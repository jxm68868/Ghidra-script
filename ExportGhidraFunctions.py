# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import re
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

reload(sys)
sys.setdefaultencoding('utf-8')

INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1F]'
REPLACE_CHAR = '_'


def sanitize_part(part):
    """清理单个路径部分"""
    return re.sub(INVALID_CHARS, REPLACE_CHAR, part)


def get_full_namespace_prefix(namespace):
    """获取完整的命名空间前缀"""
    parts = []
    current = namespace
    while current and not current.isGlobal():
        parts.append(sanitize_part(current.getName()))
        current = current.getParentNamespace()
    return '_'.join(reversed(parts)) + '_' if parts else ''


def export_all_functions():
    """修复后的导出函数"""
    base_dir = r"output_PATH"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    decompiler = DecompInterface()
    decompiler.openProgram(currentProgram)

    func_manager = currentProgram.getFunctionManager()
    total = 0
    success = 0
    errors = []

    for func in func_manager.getFunctions(True):
        try:
            total += 1
            ns_prefix = get_full_namespace_prefix(func.getParentNamespace())
            func_name = sanitize_part(func.getName())

            # 构建基础文件名并限制长度
            base_name = ns_prefix + func_name
            if len(base_name) > 200:
                base_name = base_name[:197] + "..."
            output_path = os.path.join(base_dir, base_name + ".c")

            # 处理重名文件
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(base_dir, base_name + "_" + str(counter) + ".c")
                counter += 1

            # 反编译并写入文件
            result = decompiler.decompileFunction(func, 30, ConsoleTaskMonitor())
            if result.getDecompiledFunction() is not None:
                try:
                    with open(output_path, "w") as f:
                        f.write(result.getDecompiledFunction().getC())
                    success += 1
                    print("[SUCCESS] " + ns_prefix + func_name + " -> " + output_path)
                except IOError as e:
                    errors.append((base_name, str(e)))
                    print("[FAILED] " + base_name + ": " + str(e))
            else:
                error = "Decompilation failed"
                if hasattr(result, 'getErrorMessage'):
                    error = result.getErrorMessage()
                errors.append((base_name, error))
                print("[FAILED] " + base_name + ": " + error)

        except Exception as e:
            errors.append((func.getName(), str(e)))
            print("[ERROR] " + func.getName() + ": " + str(e))

    # 生成报告
    report_path = os.path.join(base_dir, "export_report.txt")
    with open(report_path, "w") as f:
        f.write("Export Summary:\nTotal: " + str(total) + "\nSuccess: " + str(success) + "\nFailed: " + str(
            len(errors)) + "\n")
        if errors:
            f.write("\nError Details:\n")
            for name, err in errors:
                f.write(name + ": " + err + "\n")

    print("\n导出完成！成功：" + str(success) + "/" + str(total) + "，错误日志：" + report_path)


if __name__ == "__main__":
    export_all_functions()