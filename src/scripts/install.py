import os
import subprocess
import sys

def install_pip_package(package_name, version=None):
    try:
        package = f"{package_name}=={version}" if version else package_name
        print(f"Installing Python package: {package}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python package {package}: {e}")

def install_system_package(package_name, version=None):
    try:
        if version:
            package_with_version = f"{package_name}={version}"
            print(f"Installing system package: {package_with_version}")
            subprocess.check_call(['sudo', 'apt-get', 'update'], stdout=subprocess.DEVNULL)
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', package_with_version])
        else:
            print(f"Installing system package: {package_name}")
            subprocess.check_call(['sudo', 'apt-get', 'update'], stdout=subprocess.DEVNULL)
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', package_name])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install system package {package_name}: {e}")

def main():
    # List of Python packages to install with versions
    python_packages = {
        'numpy': '1.21.0',
        'pandas': '1.3.0',
        'matplotlib': '3.4.2',
        'requests': '2.25.1',
        'flask': '2.0.1'
    }

    system_packages = {
        'git': None,   
    }

    for package, version in python_packages.items():
        install_pip_package(package, version)

    for package, version in system_packages.items():
        install_system_package(package, version)

if __name__ == '__main__':
    if os.geteuid() != 0:
        print("This script requires sudo privileges to install system packages.")
        print("Please run the script using: sudo python3 script_name.py")
        sys.exit(1)

    main()
