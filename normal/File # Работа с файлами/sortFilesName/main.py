import os
import shutil

#src_dir = "F:\\[.Email_dBase]\\[Email_Pass] [.]\\ПОД РАЗЛИЧНЫЕ СЕРВЕРЫ\\321"
#target_dir = "F:\\[.Email_dBase]\\[Email_Pass] [.]\\ПОД РАЗЛИЧНЫЕ СЕРВЕРЫ\\111"
src_dir = "F:\\[.Email_dBase]\\[Email_Pass] [Combo]]"
target_dir = "F:\\[.Email_dBase]\\123"
searchstring = "HULU"

for f in os.listdir(src_dir):
    if searchstring in f and os.path.isfile(os.path.join(src_dir, f)):
        #shutil.copy2(os.path.join(src_dir, f), target_dir)
        shutil.move(os.path.join(src_dir, f), target_dir)
        print("COPY", f)
