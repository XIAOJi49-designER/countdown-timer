import sys
import time
import re


def parse_duration(arg: str) -> int:
    """解析时长字符串，返回总秒数。支持: 5m30s, 300, 10m, 90s"""
    arg = arg.strip().lower()
    if arg.isdigit():
        return int(arg)

    total = 0
    h_match = re.search(r"(\d+)\s*h", arg)
    m_match = re.search(r"(\d+)\s*m", arg)
    s_match = re.search(r"(\d+)\s*s", arg)

    if h_match:
        total += int(h_match.group(1)) * 3600
    if m_match:
        total += int(m_match.group(1)) * 60
    if s_match:
        total += int(s_match.group(1))

    if total == 0:
        print(f"错误: 无法解析时长 '{arg}'。用法: python countdown.py 5m30s | 300 | 10m | 90s")
        sys.exit(1)

    return total


def format_time(seconds: int) -> str:
    if seconds >= 3600:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    else:
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"


def render_bar(remaining: int, total: int, width: int = 30) -> str:
    filled = int(width * remaining / total)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"


def main():
    if len(sys.argv) < 2:
        print("用法: python countdown.py <时长>")
        print("示例: python countdown.py 5m    | 5 分钟")
        print("      python countdown.py 90    | 90 秒")
        print("      python countdown.py 2m30s | 2 分 30 秒")
        print("      python countdown.py 1h30m | 1 小时 30 分")
        sys.exit(1)

    total_seconds = parse_duration(sys.argv[1])

    print(f"\n倒数计时器启动 — 总时长: {format_time(total_seconds)}\n")
    print("按 Ctrl+C 可随时退出\n")

    try:
        for remaining in range(total_seconds, -1, -1):
            bar = render_bar(remaining, total_seconds)
            t = format_time(remaining)
            sys.stdout.write(f"\r  {t}  {bar}")
            sys.stdout.flush()
            if remaining > 0:
                time.sleep(1)

        print("\n\n  === 时间到! ===\n")
        sys.stdout.write("\a")
        sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\n已取消。\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
