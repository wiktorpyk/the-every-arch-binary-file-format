import os
import subprocess
import tempfile
import sys
import platform
import shutil
import stat

# Check if no arguments were provided
if len(sys.argv) < 2:
    print("Error: No arguments provided. Please specify files to process.")
    sys.exit(1)

# Determine the current architecture and map it to the expected filename component
machine = platform.machine()
machine_mapping = {
    'x86_64': 'x64',
    'aarch64': 'AArch64',
    'riscv64': 'RISC-V',
}
current_arch = machine_mapping.get(machine)
if current_arch is None:
    print(f"Unsupported architecture: {machine}")
    sys.exit(1)

for arg in sys.argv[1:]:
    # Create a temporary directory for each file to avoid interference
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory: {temp_dir}")

    try:
        file_path = os.path.abspath(arg)
        print(f"Processing: {file_path}")

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            continue

        file_name = os.path.basename(file_path)
        new_file_name = file_name.replace(".gz", "")
        output_path = os.path.join(temp_dir, new_file_name)

        # Decompress the file using gunzip
        try:
            with open(output_path, 'wb') as out_file:
                subprocess.run(['gunzip', '-c', file_path], check=True, stdout=out_file)
            print(f"Decompressed to: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to decompress {file_path}: {e}")
            continue

        # Extract the archive using ar
        try:
            subprocess.run(['ar', 'x', output_path], cwd=temp_dir, check=True)
            print(f"Extracted archive contents in {temp_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to extract archive {output_path}: {e}")
            continue

        # Determine the original base name (removing .ar.gz)
        original_base = os.path.splitext(os.path.splitext(file_name)[0])[0]
        source_file = os.path.join(temp_dir, current_arch)
        target_file = os.path.join(os.getcwd(), original_base)

        # Copy the architecture-specific file to the working directory
        if os.path.exists(source_file):
            shutil.copy(source_file, target_file)
            # Make the file executable
            os.chmod(target_file, os.stat(target_file).st_mode | stat.S_IEXEC)
            print(f"Copied and made executable: {current_arch} to {target_file}")
        else:
            print(f"Error: {current_arch} file not found in {temp_dir}")

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

print("Extraction process completed.")