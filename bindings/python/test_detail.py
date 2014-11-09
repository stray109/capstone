#!/usr/bin/env python

# Capstone Python bindings, by Nguyen Anh Quynnh <aquynh@gmail.com>
from __future__ import print_function
from capstone import *


X86_CODE16 = b"\x8d\x4c\x32\x08\x01\xd8\x81\xc6\x34\x12\x00\x00"
X86_CODE32 = b"\x8d\x4c\x32\x08\x01\xd8\x81\xc6\x34\x12\x00\x00"
X86_CODE64 = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
ARM_CODE = b"\xED\xFF\xFF\xEB\x04\xe0\x2d\xe5\x00\x00\x00\x00\xe0\x83\x22\xe5\xf1\x02\x03\x0e\x00\x00\xa0\xe3\x02\x30\xc1\xe7\x00\x00\x53\xe3"
ARM_CODE2 = b"\x10\xf1\x10\xe7\x11\xf2\x31\xe7\xdc\xa1\x2e\xf3\xe8\x4e\x62\xf3"
THUMB_CODE = b"\x70\x47\xeb\x46\x83\xb0\xc9\x68"
THUMB_CODE2 = b"\x4f\xf0\x00\x01\xbd\xe8\x00\x88"
MIPS_CODE = b"\x0C\x10\x00\x97\x00\x00\x00\x00\x24\x02\x00\x0c\x8f\xa2\x00\x00\x34\x21\x34\x56"
MIPS_CODE2 = b"\x56\x34\x21\x34\xc2\x17\x01\x00"
MIPS_32R6M = b"\x00\x07\x00\x07\x00\x11\x93\x7c\x01\x8c\x8b\x7c\x00\xc7\x48\xd0"
MIPS_32R6 = b"\xec\x80\x00\x19\x7c\x43\x22\xa0"
ARM64_CODE = b"\x09\x00\x38\xd5\xbf\x40\x00\xd5\x0c\x05\x13\xd5\x20\x50\x02\x0e\x20\xe4\x3d\x0f\x00\x18\xa0\x5f\xa2\x00\xae\x9e\x9f\x37\x03\xd5\xbf\x33\x03\xd5\xdf\x3f\x03\xd5\x21\x7c\x02\x9b\x21\x7c\x00\x53\x00\x40\x21\x4b\xe1\x0b\x40\xb9\x20\x04\x81\xda\x20\x08\x02\x8b\x10\x5b\xe8\x3c"
PPC_CODE = b"\x80\x20\x00\x00\x80\x3f\x00\x00\x10\x43\x23\x0e\xd0\x44\x00\x80\x4c\x43\x22\x02\x2d\x03\x00\x80\x7c\x43\x20\x14\x7c\x43\x20\x93\x4f\x20\x00\x21\x4c\xc8\x00\x21"
SPARC_CODE = b"\x80\xa0\x40\x02\x85\xc2\x60\x08\x85\xe8\x20\x01\x81\xe8\x00\x00\x90\x10\x20\x01\xd5\xf6\x10\x16\x21\x00\x00\x0a\x86\x00\x40\x02\x01\x00\x00\x00\x12\xbf\xff\xff\x10\xbf\xff\xff\xa0\x02\x00\x09\x0d\xbf\xff\xff\xd4\x20\x60\x00\xd4\x4e\x00\x16\x2a\xc2\x80\x03"
SPARCV9_CODE = b"\x81\xa8\x0a\x24\x89\xa0\x10\x20\x89\xa0\x1a\x60\x89\xa0\x00\xe0"
SYSZ_CODE = b"\xed\x00\x00\x00\x00\x1a\x5a\x0f\x1f\xff\xc2\x09\x80\x00\x00\x00\x07\xf7\xeb\x2a\xff\xff\x7f\x57\xe3\x01\xff\xff\x7f\x57\xeb\x00\xf0\x00\x00\x24\xb2\x4f\x00\x78"
XCORE_CODE = b"\xfe\x0f\xfe\x17\x13\x17\xc6\xfe\xec\x17\x97\xf8\xec\x4f\x1f\xfd\xec\x37\x07\xf2\x45\x5b\xf9\xfa\x02\x06\x1b\x10"

all_tests = (
        (CS_ARCH_X86, CS_MODE_16, X86_CODE16, "X86 16bit (Intel syntax)", 0),
        (CS_ARCH_X86, CS_MODE_32, X86_CODE32, "X86 32bit (ATT syntax)", CS_OPT_SYNTAX_ATT),
        (CS_ARCH_X86, CS_MODE_32, X86_CODE32, "X86 32 (Intel syntax)", 0),
        (CS_ARCH_X86, CS_MODE_64, X86_CODE64, "X86 64 (Intel syntax)", 0),
        (CS_ARCH_ARM, CS_MODE_ARM, ARM_CODE, "ARM", 0),
        (CS_ARCH_ARM, CS_MODE_ARM, ARM_CODE2, "ARM: Cortex-A15 + NEON", 0),
        (CS_ARCH_ARM, CS_MODE_THUMB, THUMB_CODE, "THUMB", 0),
        (CS_ARCH_ARM, CS_MODE_THUMB, THUMB_CODE2, "THUMB-2", 0),
        (CS_ARCH_ARM64, CS_MODE_ARM, ARM64_CODE, "ARM-64", 0),
        (CS_ARCH_MIPS, CS_MODE_32 + CS_MODE_BIG_ENDIAN, MIPS_CODE, "MIPS-32 (Big-endian)", 0),
        (CS_ARCH_MIPS, CS_MODE_64 + CS_MODE_LITTLE_ENDIAN, MIPS_CODE2, "MIPS-64-EL (Little-endian)", 0),
        (CS_ARCH_MIPS, CS_MODE_32 + CS_MODE_MIPS32R6 + CS_MODE_MICRO + CS_MODE_BIG_ENDIAN, MIPS_32R6M, "MIPS-32R6 | Micro (Big-endian)", 0),
        (CS_ARCH_MIPS, CS_MODE_32 + CS_MODE_MIPS32R6 + CS_MODE_BIG_ENDIAN, MIPS_32R6, "MIPS-32R6 (Big-endian)", 0),
        (CS_ARCH_PPC, CS_MODE_BIG_ENDIAN, PPC_CODE, "PPC-64", 0),
        (CS_ARCH_SPARC, CS_MODE_BIG_ENDIAN, SPARC_CODE, "Sparc", 0),
        (CS_ARCH_SPARC, CS_MODE_BIG_ENDIAN + CS_MODE_V9, SPARCV9_CODE, "SparcV9", 0),
        (CS_ARCH_SYSZ, 0, SYSZ_CODE, "SystemZ", 0),
        (CS_ARCH_XCORE, 0, XCORE_CODE, "XCore", 0),
)


def print_detail(insn):
    print("0x%x:\t%s\t%s  // insn-ID: %u, insn-mnem: %s" \
        % (insn.address, insn.mnemonic, insn.op_str, insn.id, \
        insn.insn_name()))

    # "data" instruction generated by SKIPDATA option has no detail
    if insn.id == 0:
        return

    if len(insn.regs_read) > 0:
        print("\tImplicit registers read: ", end=''),
        for m in insn.regs_read:
            print("%s " % insn.reg_name(m), end=''),
        print()

    if len(insn.regs_write) > 0:
        print("\tImplicit registers modified: ", end=''),
        for m in insn.regs_write:
            print("%s " % insn.reg_name(m), end=''),
        print()

    if len(insn.groups) > 0:
        print("\tThis instruction belongs to groups: ", end=''),
        for m in insn.groups:
            print("%s " % insn.group_name(m), end=''),
        print()


# ## Test class Cs
def test_class():
    for (arch, mode, code, comment, syntax) in all_tests:
        print('*' * 40)
        print("Platform: %s" % comment)
        print("Disasm:")

        try:
            md = Cs(arch, mode)
            md.detail = True

            if syntax != 0:
                md.syntax = syntax

            for insn in md.disasm(code, 0x1000):
                print_detail(insn)

            print()
        except CsError as e:
            print("ERROR: %s" % e)

if __name__ == '__main__':
    test_class()
