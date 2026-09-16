"""
CSV统计脚本 - 第一个可运行脚本
功能：读取CSV文件，统计行数、列名、数据样例
"""
import csv
import sys
from pathlib import Path
from loguru import logger


def analyze_csv(file_path: str) -> dict:
    """
    分析CSV文件

    Args:
        file_path: CSV文件路径

    Returns:
        包含统计信息的字典
    """
    path = Path(file_path)

    if not path.exists():
        logger.error(f"文件不存在: {file_path}")
        return {"error": f"文件不存在: {file_path}"}

    if path.suffix.lower() != ".csv":
        logger.warning(f"文件不是CSV格式: {file_path}")

    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)

        result = {
            "文件名": path.name,
            "总行数": len(rows),
            "列数": len(headers),
            "列名": headers,
            "前3行数据": rows[:3],
        }

        logger.info(f"CSV分析完成: {path.name}")
        logger.info(f"  总行数: {len(rows)}")
        logger.info(f"  列数: {len(headers)}")
        logger.info(f"  列名: {headers}")

        return result

    except Exception as e:
        logger.error(f"读取CSV失败: {e}")
        return {"error": str(e)}


def main():
    """主函数"""
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    if len(sys.argv) < 2:
        print("用法: python csv_stats.py <csv文件路径>")
        print("示例: python csv_stats.py data/sample.csv")
        sys.exit(1)

    file_path = sys.argv[1]
    result = analyze_csv(file_path)

    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print(f"文件: {result['文件名']}")
    print(f"总行数: {result['总行数']}")
    print(f"列数: {result['列数']}")
    print(f"列名: {', '.join(result['列名'])}")
    print("=" * 50)

    if result["前3行数据"]:
        print("\n前3行数据:")
        for i, row in enumerate(result["前3行数据"], 1):
            print(f"\n第{i}行:")
            for key, value in row.items():
                print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
