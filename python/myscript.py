from build import save_name
f = open(save_name("myfile.txt"),'w')
f.write("XXXXX")
f.close()

f = open(save_name("dir/myfile2.txt"),'w')
f.write("XXXXX")
f.close()
