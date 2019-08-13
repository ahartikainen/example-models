import shutil
import glob
import os
os.chdir(os.path.join(os.path.expanduser("~"), "github", "example-models"))

files = glob.glob("ARM/Ch.3/*.R", recursive=True)
files


for path in files:
    if not path.endswith(".data.R"):
        root, ext = os.path.splitext(path)
        pyfile = root + ".py"
        shutil.copy2(src=path, dst=pyfile)
        print(f"src={path}, dst={pyfile}")
        
