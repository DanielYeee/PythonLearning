import tarfile
import gzip
import shutil
import os

# Paths
txz_gz_path = 'path/to/your/archive.txz.gz'
intermediate_txz_path = 'path/to/intermediate/archive.txz'
output_file_path = 'path/to/save/extracted_file.txt'
file_inside_tar = 'file/you/want/to/read.txt'

# Step 1: Decompress the .gz layer
with gzip.open(txz_gz_path, 'rb') as f_in:
    with open(intermediate_txz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Step 2: Decompress the .txz layer
with tarfile.open(intermediate_txz_path, 'r:xz') as tar:
    member = tar.getmember(file_inside_tar)
    with tar.extractfile(member) as file:
        content = file.read()

        # Step 3: Save the extracted content
        with open(output_file_path, 'wb') as output_file:
            output_file.write(content)

# Clean up the intermediate file
os.remove(intermediate_txz_path)

print(f"File has been extracted and saved to {output_file_path}")
