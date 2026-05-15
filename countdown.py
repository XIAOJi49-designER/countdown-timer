import sys
import time
import re
import shutil


def parse_duration(arg: str) -> int:
    """解析时长字符串，返回总秒数。支持: 5m30s, 300, 10m, 90s, 1h30m"""
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
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def render_bar(remaining: int, total: int, width: int) -> str:
    filled = round(width * remaining / total) if total > 0 else 0
    return f"[{'█' * filled}{'░' * (width - filled)}]"


def get_bar_width() -> int:
    try:
        cols, _ = shutil.get_terminal_size()
        return max(20, min(cols - 20, 60))
    except (OSError, ValueError):
        return 30


def main():
    if len(sys.argv) < 2:
        print("用法: python countdown.py <时长>")
        print("示例: python countdown.py 5m    | 5 分钟")
        print("      python countdown.py 90    | 90 秒")
        print("      python countdown.py 2m30s | 2 分 30 秒")
        print("      python countdown.py 1h30m | 1 小时 30 分")
        sys.exit(1)

    total_seconds = parse_duration(sys.argv[1])
    bar_width = get_bar_width()

    print(f"\n倒数计时器启动 — 总时长: {format_time(total_seconds)}")
    print(f"预计结束: {time.strftime('%H:%M:%S', time.localtime(time.time() + total_seconds))}")
    print("按 Ctrl+C 可随时退出\n")

    start = time.monotonic()

    try:
        while True:
            elapsed = time.monotonic() - start
            remaining = max(0, total_seconds - round(elapsed))

            bar = render_bar(remaining, total_seconds, bar_width)
            t = format_time(remaining)
            sys.stdout.write(f"\r  {t}  {bar}")
            sys.stdout.flush()

            if remaining <= 0:
                break

            # 休眠到下一秒边界，避免累积漂移
            next_tick = int(elapsed) + 1
            sleep_duration = start + next_tick - time.monotonic()
            if sleep_duration > 0:
                time.sleep(sleep_duration)

        print("\n\n  === 时间到! ===")
        for _ in range(3):
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(0.15)
        print()

    except KeyboardInterrupt:
        print("\n\n已取消。\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
