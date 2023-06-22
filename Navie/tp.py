import subprocess
import os

def send_reset_command():
    terminal_name = os.ttyname(0)
    while True:
        command = input("Enter 'reset' to reset total_processed: ")
        if command == "reset":
            subprocess.Popen(['echo', 'reset'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable=terminal_name)

def main():
    send_reset_command()

if __name__ == "__main__":
    main()
