import severed_bindings as sb
import subprocess
import sys
import time

def get_dmesg_output():
	out = subprocess.Popen(['dmesg','-c'],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
	stdout, stderr = out.communicate()
	return stdout.decode("utf-8")

if len(sys.argv) != 2:
	print("Enter PID as an argument")
	sys.exit()

# Get PID
pid = int(sys.argv[1])

# Clean dmesg
get_dmesg_output()

# Test for setting id
print("Setting access id")
if sb.severed_set_access_id(1234):
	print("Error setting access ID")
	sys.exit()
else:
	print("Success setting access ID")

# Test for issuing NMI to VM
print("\nIssuing NMI")
if sb.severed_issue_nmi(pid):
	print("Error issuing NMI")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'Sending NMI to guest at PID' not in dmesg:
	print("Error issuing NMI")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)


# Test for finding Interrupt Handler in VM
print("\nFinding Interrupt Handler")
if sb.severed_find_int_handler(-1,pid):
	print("Error finding Interrupt Handler")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'Start to find interrupt handler' not in dmesg:
	print("Error finding Interrupt Handler NMI")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)

# Test for translating GFN to PFN
print("\nTranslating GFN to PFN")
if sb.severed_translate_gfn(0,pid):
	print("Error translating GFN to PFN")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'GFN: 0x0 = PFN: 0x' not in dmesg:
	print("Error translating GFN to PFN")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)

# Test for enabling access tracking
print("\nEnabling access tracking")
if sb.severed_enable_tracking(pid):
	print("Error enabling access tracking")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'Syscall_rip' not in dmesg:
	print("Error enabling access tracking")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)

# Test for disabling access tracking
print("\nDisabling access tracking")
if sb.severed_disable_tracking(pid):
	print("Error disabling access tracking")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'Current tlb_ctl' not in dmesg:
	print("Error disabling access tracking")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)

# Test for printing buffer
print("\nPrinting buffer")
if sb.severed_print_buffer(pid):
	print("Error printing buffer")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'severed_print' not in dmesg:
	print("Error printing buffer")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)

# Test for enabling virtio tracking
print("\nEnabling virtio tracking")
if sb.severed_set_virtio_track(1):
	print("Error enabling virtio tracking")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'set_virtio_tracking (1)' not in dmesg:
	print("Error enabling virtio tracking")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)

# Test for disabling virtio tracking
print("\nDisabling virtio tracking")
if sb.severed_set_virtio_track(0):
	print("Error disabling virtio tracking")
	sys.exit()

time.sleep(1)

dmesg = get_dmesg_output()

if 'set_virtio_tracking (0)' not in dmesg:
	print("Error disabling virtio tracking")
	print(dmesg)
	sys.exit()
else:
        print(dmesg)


'''
gfn1
gfn2
pfn2 = pfn_from(gfn)

# Change page mapping of two GFNs in SLAT
# gfn2 now also points to gfn1
sb.severed_change_mapping(gfn1,gfn2,pid)


# Change mapping of a GFN to another PFN in SLAT
# gfn2 now points to pfn2 (reverts above operation)
sb.severed_change_mapping_direct(gfn2,pfn2,pid)
'''
