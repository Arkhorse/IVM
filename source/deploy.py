from compileall import compile_dir
from shutil import copyfile as c
from shutil import make_archive as m

compile_dir('E:\Python\IVM\IVM\source\ivm')
# a -tzip -mx0 IVM.Main.wotmod "res"

#m('com.ivm', format='zip', root_dir='E:\Python\IVM\IVM\source\ivm', base_dir='E:\Python\IVM\IVM\source\ivm')