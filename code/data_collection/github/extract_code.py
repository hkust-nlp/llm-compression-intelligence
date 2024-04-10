"""Copies all files belonging to a given language to a new directory."""
import os
import sys
from shutil import copyfile

from language_mapping import _EXTENSION_TO_LANG,_LANG_TO_EXTENSION
MAX_FILE_SIZE = 1024 ** 2  # 1 MB
MIN_FILE_TOKENS = 100

def main():
	if len(sys.argv) <= 3:
		raise ValueError('Provide a language, source directory and target directory.')

	language = sys.argv[1]
	proj_dir = sys.argv[2]
	out_dir = sys.argv[3]

	print(f'Processing: {proj_dir}')
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	files_found = 0
	for root, _, files in os.walk(proj_dir):
		for file in files:
			if any(file.endswith(ext) for ext in _EXTENSION_TO_LANG.keys()):
				in_path = os.path.join(root, file)
				if not os.path.exists(in_path): 
					continue
				if os.path.getsize(in_path) > MAX_FILE_SIZE:  
					continue
				with open(in_path, errors='ignore') as f_in:
					text = f_in.read()
				
				rel_path = root[len(proj_dir)+1:].replace('/', '__')
				out_path = os.path.join(out_dir, rel_path + ('__' if rel_path else '') + file)
				if not os.path.exists(out_path):
					try:
						copyfile(in_path, out_path)
					except Exception as e:
						print(f'Skipping problematic file {in_path} due to: {e}')
				files_found += 1
	print(f'Done processing; copied {files_found} files.')


if __name__ == '__main__':
	main()