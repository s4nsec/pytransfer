# Description: The purpose of the script is to upload/download files/folders
# to/from a remote server using rsync.
import argparse
from pathlib import Path
import subprocess
from loguru import logger

def parse_args()->argparse.Namespace:
    parser = argparse.ArgumentParser(description='Transfer files/folders to/from a remote server')

    parser.add_argument('-u', '--upload', action='store_true', help='Upload a file/folder to a remote server')
    parser.add_argument('-d', '--download', action='store_true', help='Download a file/folder from a remote server')
    parser.add_argument('-r', '--remote', help='Remote server to upload/download files/folders')
    parser.add_argument('-f', '--file', type=Path, help='File to upload/download')

    return parser.parse_args()

def check_args(args: argparse.Namespace):
    if not args.upload and not args.download:
        logger.error('Please specify either --upload or --download')
        exit(1)

    if not args.remote:
        logger.error('Please specify the remote server')
        exit(1)

    if not args.file:
        logger.error('Please specify the file/folder to upload/download')
        exit(1)

    if not args.file.exists():
        logger.error(f'{args.file} does not exist')
        exit(1)

    if args.upload and args.download:
        logger.error('Please specify only either --upload or --download')
        exit(1)

def upload(file: Path, remote: str):
    if file.is_file():
        command = f"rsync {file} {remote}"
        try:
            subprocess.run(command, shell=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error uploading {file}: {e}")

    elif file.is_dir():
        command = f"rsync -av {file} {remote} --exclude={file}/.git"
        try:
            subprocess.run(command, shell=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error uploading {file}: {e}")

def download(file: Path, remote: str):
    if file.is_file():
        command = f"rsync {remote}/{file} ."
        try:
            subprocess.run(command, shell=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading {file}: {e}")

    elif file.is_dir():
        command = f"rsync -av {remote}/{file} . --exclude={file}/.git"
        try:
            subprocess.run(command, shell=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading {file}: {e}")


def main():
    args = parse_args()
    check_args(args)

    if args.upload:
        upload(args.file, args.remote)
    elif args.download:
        download(args.file, args.remote)

if __name__ == '__main__':
    main()
