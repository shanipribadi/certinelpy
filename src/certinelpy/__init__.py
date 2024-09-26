import time
from pathlib import Path
import shutil

CERT_NAME = Path("cert")
KEY_NAME = Path("key")
DATA_NAME = Path("..data")
DATA_NEW_NAME = Path("..data_new")


# TODO: move this to a test
def generate():
    import argparse

    parser = argparse.ArgumentParser(prog="certinelpy")
    parser.add_argument("--target-dir", type=Path, required=True)
    parser.add_argument("--rm", action="store_true")
    parser.add_argument("--sleep", type=int, default=0)
    args = parser.parse_args()

    target_dir = args.target_dir
    if args.rm:
        if target_dir.exists():
            shutil.rmtree(target_dir)

    setup(target_dir)
    time.sleep(args.sleep)
    write(target_dir, Path(".first"), "c1", "k1")
    swap(target_dir, Path(".first"))
    read(target_dir)

    time.sleep(args.sleep)
    write(target_dir, Path(".second"), "c2", "k2")
    swap(target_dir, Path(".second"))
    read(target_dir)

    time.sleep(args.sleep)
    write(target_dir, Path(".third"), "c3", "k3")
    swap(target_dir, Path(".third"))
    read(target_dir)


def setup(target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)
    key_symlink = target_dir / KEY_NAME
    key_symlink.symlink_to(DATA_NAME / KEY_NAME)
    cert_symlink = target_dir / CERT_NAME
    cert_symlink.symlink_to(DATA_NAME / CERT_NAME)


def write(target_dir: Path, dir_name: Path, cert_value: str, key_value: str):
    dir = target_dir / dir_name
    dir.mkdir(parents=True, exist_ok=True)
    cert = dir / CERT_NAME
    cert.write_text(cert_value)
    key = dir / KEY_NAME
    key.write_text(key_value)


def swap(target_dir: Path, dir_name: Path):
    data = target_dir / DATA_NAME
    data_new = target_dir / DATA_NEW_NAME
    data_new.symlink_to(dir_name)
    data_new.rename(data)


def read(target_dir: Path):
    key_symlink = target_dir / KEY_NAME
    cert_symlink = target_dir / CERT_NAME
    print(f"key: {key_symlink.read_text()}; cert: {cert_symlink.read_text()}")


def watch():
    import argparse
    from watchfiles import watch, Change

    parser = argparse.ArgumentParser(prog="certinelpy")
    parser.add_argument("--target-file", type=Path, required=True)
    args = parser.parse_args()

    target_dir: Path = args.target_file.parent
    data_symlink: Path = target_dir / args.target_file.readlink().parent
    for changes in watch(target_dir):
        for change, n in changes:
            if n == str(data_symlink):
                if change in [Change.modified]:
                    print(change)


def scan():
    import argparse

    parser = argparse.ArgumentParser(prog="certinelpy")
    parser.add_argument("--target-file", type=Path, required=True)
    args = parser.parse_args()

    dir: Path = args.target_file.parent
    file: Path = args.target_file
    print(dir)
    print(file)
    print(file.readlink())
    print(file.readlink().parent)
