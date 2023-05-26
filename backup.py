import os
import zipfile
import subprocess

def main():
    # Backup zsh configuration files
    backup_zsh()

    # Backup Python and Conda environments
    backup_python_conda()

def backup_zsh():
    zsh_files = ['.zshrc', '.zsh_history']
    with zipfile.ZipFile('zsh.zip', 'w') as zsh_zip:
        for zsh_file in zsh_files:
            zsh_file_path = os.path.expanduser(f"~/{zsh_file}")
            if os.path.isfile(zsh_file_path):
                zsh_zip.write(zsh_file_path, arcname=zsh_file)

def backup_python_conda():
    # Backup Python environments
    try:
        pip2_output = os.popen('pip2 freeze --all').read()
        with open('pip2_requirements.txt', 'w') as f:
            f.write(pip2_output)
    except FileNotFoundError:
        print("pip2 not found, skipping pip2 backup")

    pip3_output = os.popen('pip3 freeze --all').read()
    with open('pip3_requirements.txt', 'w') as f:
        f.write(pip3_output)

    # Backup Conda environments
    conda_envs_output = subprocess.getoutput('conda info --envs')
    conda_envs = conda_envs_output.split('\n')[2:]

    for conda_env in conda_envs:
        env_info = conda_env.strip().split()
        if len(env_info) < 2 or '*' in env_info:
            continue

        env_name, env_path = env_info[:2]
        if not os.path.isdir(env_path):
            print(f"Could not find the conda environment directory: {env_path}")
            continue

        env_files = [os.path.join(env_path, file) for file in os.listdir(env_path)]

        with zipfile.ZipFile(f'conda_{env_name}.zip', 'w') as conda_zip:
            for env_file in env_files:
                conda_zip.write(env_file, arcname=os.path.basename(env_file))

        conda_env_output = subprocess.getoutput(f'conda list -n {env_name}')
        with open(f'conda_{env_name}_requirements.txt', 'w') as f:
            f.write(conda_env_output)

if __name__ == "__main__":
    main()
