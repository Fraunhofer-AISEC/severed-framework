# SEVered framework

## Description

SEVered is framework for Virtual Machine Introspection (VMI) of encrypted Virtual Machines.  
The framework allows you to track memory accesses of VMs, and the modify the Second Level Adress Translation (SLAT)

This allows you for example to execute the SEVered attack, which is described here: 

<https://arxiv.org/abs/1805.09604>

## Features

The framework adds the following IOCTLs to /dev/kvm: 

* KVM_TRACKING_ENABLE <pid>
Start to track memory accesses of a VM with the given PID. Each memory access will be tracked once. 

* KVM_TRACKING_DISABLE <pid>
Stop tracking of memory accesses. List of all tracked memory accesses will be written to dmesg. 

* KVM_MAPPING_CHANGE <pid> <GPA1> <GPA2>
Remap GPA1 of a VM with the given PID to the PFN of GPA2. 

We use https://github.com/jerome-pouiller/ioctl to call IOCTLs. 

`sudo ioctl /dev/kvm <IOCTL-NAME>`

## Limitations

* We do not support situations in which multiple VMs with multiple vcpus are running, and at least one physical core is shared among VMs. 
* PIDs must match a running VM. Otherwise, the host OS might freeze. 

## Linux Kernel and Patch

* Download and extract Linux 4.18.13:

* Enter the kernel directory and apply the patch: 

`patch -p1 < severed_patch_4.18.13.patch`

* Build the kernel. We use this command: 

`make-kpkg --initrd kernel_image modules_image -j 16`

* Afterwards, install the kernel and boot it up: 

`sudo dpkg -i ../name_of_image.deb`

## Ioctl Tool Installation

In order to install the ioctl tool the following steps are taken:

* download the ioctl tool here https://github.com/jerome-pouiller/ioctl,

* before compiling and building the tool, install the dependencies: 

`sudo apt-get install libasound2-dev libdrm-dev`

* open the file ioctls_list.c and replace the line

`#include <linux/nvme.h>`

with  the line
`#include <linux/nvme_ioctl.h>`

* Type `make` and and comment all the lines ioctls_list.c about which the compiler complains,

* add the following lines into the file ioctls_list.c

`{"KVM_TRACKING_ENABLE", KVM_TRACKING_ENABLE, -1, -1}, //linux/kvm.h:782`

`{"KVM_TRACKING_DISABLE", KVM_TRACKING_DISABLE, -1, -1}, //linux/kvm.h:783`

`{"KVM_MAPPING_CHANGE", KVM_MAPPING_CHANGE, -1, -1}, //linux/kvm.h:784`

* hit "make" again,

* if a compiler complains about the variables `KMV_TRACKING_ENABLE`,
`KVM_TRACKING_DISABLE` and `KVM_MAPPING_CHANGE` then
copy the file kvm.h from your patched linux directory to the installed 
linux directory. (important: linux kernel should be built at this step):

`sudo cp your_linux_folder/usr/include/linux/kvm.h /usr/include/linux`

* hit "sudo make install".

After installation, the command ioctl will be accessable in any directory.
See below how to run the tool.

## Using the SEVered framework

* Start up the VM

* To clean kernel outputs use

`sudo dmesg -C`.

* To start tracking use the command:

`sudo ioctl /dev/kvm KVM_TRACKING_ENABLE <PID>`.

* To stop tracking use the command

`sudo ioctl /dev/kvm KVM_TRACKING_DISABLE <PID>`.

* To change mapping use the command

`sudo ioctl /dev/kvm KVM_MAPPING_CHANGE`.

Here it is required to give a PID, GPA1 and GPA2 separated by comma, for instance, 3132,00002a96,000036f1.

