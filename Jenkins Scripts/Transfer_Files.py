import os
import shutil 

print('Inside the script')
SRC_DIR = "C:\Program Files (x86)\Jenkins\workspace\Build Job - Generic Approval Process"
print('SRC_DIR has been declared')
SRC_FILES = os.listdir(SRC_DIR)
print('SRC_FILES list has been declared')
TGT_DIR = "K:/TGT_DIR"

for file in SRC_FILES:
	file_name = SRC_DIR + "\ "
	file_name = file_name.strip() + file + " "
	if file_name.strip().endswith(".bpmn"):
		print(file_name)
		shutil.copy(file_name.strip(),TGT_DIR)