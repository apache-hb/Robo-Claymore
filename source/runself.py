import sys
import subprocess

def install():
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
    subprocess.call(['pip', 'install', '-e', 'git:', 'https://github.com/Apache-HB/Robo-Claymore'])

if __name__ == '__main__':
    install()
    params = [sys.executable, 'main.py']
    params.extend(sys.argv[1:])
    subprocess.call(params)