import os
import shutil
import tempfile
from elftools.elf.elffile import ELFFile

def get_binaries():
    binaries = []
    for root, dirs, files in os.walk('build'):
        for file in files:
            binaries.append(os.path.join(root, file))
    return binaries

def get_distinct_binaries():
    binaries = get_binaries()
    distinct_binaries = []
    for binary in binaries:
        name = os.path.basename(binary)
        if name not in distinct_binaries:
            distinct_binaries.append(name)
    return distinct_binaries

for binary in get_distinct_binaries():
    paths = []
    for root, dirs, files in os.walk('build'):
        for file in files:
            if file == binary:
                paths.append(os.path.join(root, file))
    files = dict()
    for path in paths:
        with open(path, 'rb') as f:
            elffile = ELFFile(f)
            arch = elffile.get_machine_arch()
            files[arch] = path

    with tempfile.TemporaryDirectory() as temp_dir:
        for arch, path in files.items():
            dest = os.path.join(temp_dir, arch)
            shutil.copy(path, dest)
        
        ar_path = os.path.join(temp_dir, f'{binary}.ar')
        os.system(f'ar rcs {ar_path} {temp_dir}/*')
        
        os.makedirs('build_combined', exist_ok=True)
        os.system(f'gzip -c {ar_path} > build_combined/{binary}.ar.gz')