# SEVered framework

## Description

SEVered is framework for Virtual Machine Introspection (VMI) of Virtual Machines protected by technologies such as AMD SEV.  
The framework allows to track memory accesses of VMs, and to modify the Second Level Adress Translation (SLAT).

This enables you to execute attacks such as SEVered and SEVerity:  

<https://arxiv.org/abs/1805.09604>
<https://arxiv.org/abs/2105.13824>

## Features

The framework provides the following functions:
- severed_set_access_id(id=int): Set the access identifier used in prints
- severed_disable_tracking(pid=int): Disable page tracking
- severed_enable_tracking(pid=int): Enable page tracking
- severed_print_buf(): Print the tracked pages in the buffer
- severed_translate_gfn(gfn=unsigned_long,pid=int): Translate a given GFN to a PFN
- severed_change_mapping(gfn1=unsigned_long,gfn2=unsigned_long,pid=int): Swap page mapping of two GFNs in SLAT
- severed_change_mapping_direct(gfn=unsigned_long,pfn=unsigned_long,pid=int): Change mapping of a GFN to a specific PFN in SLAT
- severed_find_int_handler(interrupt=int,pid=int): Identify interrupt handler in guest
        - ```interrupt=-1``` for NMI interrupt
- severed_issue_nmi(pid=int): Send an NMI to the guest
- severed_set_virtio_track(): Enable/Disable virtio tracking

## Linux Kernel and Patch

1. Clone AMD's linux kernel from [https://github.com/AMDESE/linux](https://github.com/AMDESE/linux)  
2. Change into the sev-es-5.6-v3 branch with ```git checkout sev-es-5.6-v3``` and apply the patch: ```patch -p1 < ../severed_framework.patch```
3. Configure the kernel: ```cp /boot/config-$(uname -r) .config```
4. Build the kernel with ```make -j <number of threads>``` 
5. Build the kernel modules with ```make -j <number of threads> modules_install```
6. Install the newly compiled kernel with ```make install```
7. Boot the new kernel

## Installing Python Module

We provide a python package for version 3.9. You can install it using pip:

```
python3 -m pip severed_bindings-1.0-cp39-cp39-linux_x86_64.whl
```

For other python versions, you can create your own package using ```severed_bindings-1.0.tar.gz``` and ```distutils```.

1. Extract the contents of the tar with ```tar -xvf severed_bindings-1.0.tar.gz```
2. Go into the newly extracted folder ```cd severed_bindings-1.0/```
3. Use the setup.py script to install the severed_bindings in your current python3 version with ```sudo python3 setup.py install```
4. The severed_bindings should be installed now.

Once you installed the package, the functions of the SEVered framework can be called by importing the package ```severed_bindings``` in any python file.

## Using the SEVered framework

1. Start up the VM
2. Import the ```severed_bindings``` package in a python file
3. All the functions can be called using the imported package

Our [Test](./test.py) file shows examples for all functions. 

## Limitations

- The size of the target VM is statically configued with 2GB. If the target VM has a different amount of memory, this has to be modified accordingly.
        - There is an attempt to dynamically adjust the VM memory size in arch/x86/kvm/svm.c @ 5464-5468. However, although the correct size is calculated, when used with the framework it will end up in a soft lockup.
- severed_set_virtio_track(int) does not provide a PID parameter, and therefore will only work effectively when only one VM is running.
- Only 4 PIDs are tracked, thus only the first 4 VMs will be tracked. If a 5th VM is booted, it can't be address with the framework.
