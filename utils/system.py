import sys
import os

class SystemController:
    def __init__(self):
        return
    
    def clear_screen():
        os.system('cls' if os.name == "nt" else "clear")
    
    def wait_for_keypress():
        print("Press any key to continue . . .", end="", flush=True)
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)

            try:
                tty.setraw(fd)
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print()
        

    def print_loading_bar(self, task_name, current, total, bar_length=50, max_name_length=20):
        progress = (current / total)
        arrow = '=' * int(round(progress*bar_length) - 1)
        spaces = ' ' * (bar_length - len(arrow))
        percent = round(progress * 100, 1)

        truncated_task_name = task_name[:max_name_length]
        truncated_task_name = truncated_task_name.ljust(max_name_length)
        
        truncated_task_name = f"{truncated_task_name}"

        sys.stdout.write(f'\r[{arrow}{spaces}] {percent}% - {truncated_task_name}')
        sys.stdout.flush()
        