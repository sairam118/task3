import unittest 
import cli
from runner import subp
import threading

class Test_fio_rvg(unittest.TestCase):

    def setUp(self):
        print("step 1: creating pv vg lv")
        
        subp(f"sudo pvcreate {cli.disk}")
        subp(f"sudo vgcreate {cli.vg_name} {cli.disk}")
        subp(f"sudo lvcreate -n {cli.lv_name} --size {cli.lv_size}G {cli.vg_name}")
        
        self.mountpoint = "/data"
        self.lvpath = f"/dev/{cli.vg_name}/{cli.lv_name}"
        
        print("step 2 : creating file system")
        subp(f"sudo mkfs.{cli.fs} {self.lvpath}")
        subp("mkdir {self.mountpoint}")
        subp(f"mount {self.lvpath} {self.mountpoint}")
       

    def tearDown(self):
        print("\n\nstep 8 : destroying the physical volume, volume group, logical volume")
        subp(f"sudo umount /data")
        subp(f"rmdir self.mountpoint")
        subp(f"sudo lvremove -ff {cli.vg_name}")
        subp(f"sudo vgremove {cli.vg_name}")
        subp(f"sudo pvremove {cli.disk}")
 
    def testfio(self):
        t1 = threading.Thread(target=self.fio)
        t2 = threading.Thread(target=self.dremove)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print("verifying IO")
        self.assertRegex(self.f.stdout, "Run status")
        print("sucess")

        print("to check disk is removed from vg")
        self.assertRegex(self.v.stdout,cli.dr)
        print("sucess")

    def fio(self):
        print("starting fio")
        self.f = subp("sudo fio fiorandread.fio")
    
    def dremove(self):
        print("removing disk from vg")
        self.v = subp(f"sudo vgreduce {cli.vg_name} {cli.dr} ")



