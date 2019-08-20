"""
Inspects the map file from a target build and generates a report about RAM/ROM use.
"""
from __future__ import print_function

import os
from collections import namedtuple, OrderedDict, defaultdict
import csv
import re
import sys
import argparse

AP = argparse.ArgumentParser(description='Check map file for RAM/ROM use')
AP.add_argument('--map', default=None, help="Which map file to check")
AP.add_argument('--dasy', default='base', help="Compiled for DASY Base or Enhanced",
	choices=('base', 'enh'))
ARGS = AP.parse_args()

MAP_FILE = ARGS.map
if not MAP_FILE:
	if ARGS.dasy == 'enh':
		MAP_FILE="../../../../generatedFiles/DASY_JLR_MY20_ENH/exec/DASY_JLR_MY20_ENH.map"
	else: # assume DASY Base
		MAP_FILE="../../../../generatedFiles/DASY_JLR_MY20_BASE/exec/DASY_JLR_MY20_BASE.map"

if not os.path.exists(MAP_FILE):
	print("Map file not found:", MAP_FILE)
	exit(1)

RAM_BUDGETS = {
	'PER':  305 * 1024,
	'SIT':  225 * 1024,
	'FCT':   62 * 1024,
	'RPM':   10 * 1024,
	'INT':  175 * 1024,
	'COPY': 165 * 1024,
	'VMC':   44 * 1024,
	'BSW':  435 * 1024,
	'EDR':   50 * 1024,
}
TOTAL_RAM_BUDGET = 1.2 * 1024 * 1024

ROM_BUDGETS = {
	'PER':  900 * 1024,
	'SIT': 1000 * 1024,
	'FCT':  900 * 1024,
	'RPM':  300 * 1024,
	'INT':  900 * 1024,
	'COPY':  80 * 1024,
	'VMC':  290 * 1024,
	'BSW': 1400 * 1024,
}
TOTAL_ROM_BUDGET = 16 * 1024 * 1024

DASY_MEMORY_TYPE = {
	'pcache': 'RAM',
	'dcache': 'RAM',
	'PSPR':   'RAM',
	'DSPR':   'RAM',
	'PFlash': 'ROM',
	'DLMU':   'RAM',
	'LMU0':   'RAM',
	'LMU1':   'RAM',
	'LMU2':   'RAM',
	'DAM':    'RAM',
	'EMEM':   'RAM',
	'?':      '?', # dummy
}
	
DASY_MEMORY = { # B-Step in Bytes per Core (core -1 if it is the same mem for each core)
	# Program Cache. (If cache is disabled, can be used as RAM)
	'pcache': {0: 32768,   1: 32768,   2: 32768,   3: 32768,   4: 32768,   5: 32768 },
	# Data Cache. (If cache is disabled, can be used as RAM)
	'dcache': {0: 16384,   1: 16384,   2: 16384,   3: 16384,   4: 16384,   5: 16384 },
	# Program Scratch Pad RAM.
	'PSPR':   {0: 65536,   1: 65536,   2: 65536,   3: 65536,   4: 65536,   5: 65536 },
	# Data Scratch Pad RAM. 240KB for cores 0 and 1. 95KB for the rest.
	'DSPR':   {0: 240*1024,   1: 240*1024,   2: 95*1024,   3: 95*1024,   4: 95*1024,   5: 95*1024 },
	# Program Flash
	# Core 5 has only 1MB while the others have 3MB.
	'PFlash': {0: 3*1024*1024, 1: 3*1024*1024, 2: 3*1024*1024, 3: 3*1024*1024, 4: 3*1024*1024, 5: 1*1024*1024 },
	# Default Local Memory Unit
	'DLMU':   {0: 65536,   1: 65536,   2: 65536,   3: 65536,   4: 65536,   5: 65536 },
	# Local Memory Unit
	'LMU0':    {-1: 256*1024},
	'LMU1':    {-1: 256*1024},
	'LMU2':    {-1: 256*1024},
	# Default Application Memory. PJIF says we should not use it (Not ASIL B capable).
	'DAM0':    {-1: 0},
	'DAM1':    {-1: 0},
	# Extension Memory. Actually 4MB, but 2MB reserved for tracing.
	'EMEM':   {-1: 2 * 1024 * 1024},
	'?':      {-1:1, 0:1, 1:1, 2:1, 3:1, 4:1, 5:1}, # just dummies
}

# Since BSW, JLR, and other need memory too. PL DASY is reponsible for the CSW, so PJ-PH only cares for the ASW memory.
# Source for the numbers: https://inside-ilm.bosch.com/irj/go/nui/sid/80de9ffd-fd57-3510-6fa3-a7b18413fa04
# Stack size will be subtracted further according to the map file.
ASW_BUDGETS = {
	'DSPR':   {0:107*1025, 1:  245760, 2:   98303, 3:   77313, 4:   98303, 5:   98303 },
	'PFlash': {0: 2162689, 1: 3145728, 2: 3145728, 3: 3145728, 4: 2097152, 5: 1048575 },
	'DLMU':   {0:   36000, 1:   65536, 2:   65536, 3:       0, 4:   65536, 5:   65536 },
	'LMU0':   {-1: 256*1024},
	'LMU1':   {-1: 256*1024},
	'LMU2':   {-1: 256*1024},
	'EMEM':   {-1: 2 * 1024 * 1024},
}
ASW_SUBSYS = ('PER', 'SIT', 'FCT', 'RPM', 'INT', 'COPY', 'VMC')

# Map linker sections to DASy memory types and cores
UNKNOWN_LINKER_SECTION = ('?', -1)
LINKER_SECTIONS_2_DASY = {
    ".default_data": ('DSPR', 0),
    ".default_bss": ('DSPR', 0),
    ".emem0_nc.bss": ("EMEM", -1),
    ".emem0_nc.data": ("EMEM", -1),
    ".lmu0_nc.bss": ("LMU0", -1),
    ".lmu0_nc.data": ("LMU0", -1),
    ".lmu1_nc.bss": ("LMU1", -1),
    ".lmu1_nc.data": ("LMU1", -1),
    ".lmu2_nc.bss": ("LMU2", -1),
    ".lmu2_nc.data": ("LMU2", -1),
    ".CalBoschBlock.rodata": ('PFlash', 0),
    ".CalBoschBlock.bss": ('DSPR', 0),
    ".CalBoschBlock.text": ('DSPR', 0),
}
for cpuid in range(6):
	LINKER_SECTIONS_2_DASY[".CPU%d.ustack" % cpuid] = ("?", cpuid)
	LINKER_SECTIONS_2_DASY[".CPU%d.csa" % cpuid] = ("?", cpuid)
	LINKER_SECTIONS_2_DASY[".CPU%d.istack" % cpuid] = ("?", cpuid)
	LINKER_SECTIONS_2_DASY[".CPU%d.bss" % cpuid] = ("DSPR", cpuid)
	LINKER_SECTIONS_2_DASY[".CPU%d.data" % cpuid] = ("DSPR", cpuid)
	LINKER_SECTIONS_2_DASY[".CPU%d.psram_text" % cpuid] = ("?", cpuid)
	LINKER_SECTIONS_2_DASY[".ifx_sbst%d" % cpuid] = ("DSPR", cpuid)
	for suffix in ('.bss', '.data', '_nc.bss', '_nc.data'):
		LINKER_SECTIONS_2_DASY[".dlmu%d%s" % (cpuid, suffix)] = ('DLMU', cpuid)
	for suffix in ('BlockHeader', 'BlockEpilog', 'VectorPointerTable', 'rodata', 'user_text', 'text', 'user_rodata', 'Build_Info', 'SubBlockTable', 'RBSignature', 'RBCrc'):
		LINKER_SECTIONS_2_DASY[".Applpfls%d.%s" % (cpuid, suffix)] = ('PFlash', cpuid)

# A little bit of a consistency check
for (t, _) in LINKER_SECTIONS_2_DASY.values():
	if t == '?': continue
	assert t in DASY_MEMORY, t
	assert t in DASY_MEMORY_TYPE, t

def get_memory_type(section_name):
	"""Returns tuple of the DASy memory name, CPU ID, and 'RAM'/'ROM'"""
	dasy_mem, cpuid = LINKER_SECTIONS_2_DASY.get(section_name, UNKNOWN_LINKER_SECTION)
	kind = DASY_MEMORY_TYPE[dasy_mem]
	return dasy_mem, cpuid, kind

def get_maximum_bytes(mem_type, cpuid):
	"""Returns maximum amount of bytes for a some memory"""
	if not mem_type:
		return 0.0
	return DASY_MEMORY[mem_type][cpuid]

def get_maximum_ASW_bytes(mem_type, cpuid):
	"""Returns maximum amount of bytes ASW can use for some memory"""
	if not mem_type:
		return 0.0
	if not mem_type in ASW_BUDGETS:
		return 0
	return ASW_BUDGETS[mem_type][cpuid]

def get_quota(byte_count, section_name):
	"""Returns the quota of memory the byte_count is of the corresponding section_name memory"""
	dasy_mem, cpuid = LINKER_SECTIONS_2_DASY.get(section_name, UNKNOWN_LINKER_SECTION)
	max_bytes = get_maximum_bytes(dasy_mem, cpuid)
	#print("Quota", section_name, byte_count,"/", maximum)
	return float(byte_count) / max_bytes	
	
# Read MAP file
class Section:
    def __init__(self, name, size):
        self.name = name
        self.size = size
    def __repr__(self):
        return "<sec:%s>" % self.name

class Symbol:
    def __init__(self, name, section, size, afile=None, ofile=None):
        self.name = name
        self.section = section
        self.size = size
        self.afile = afile
        self.ofile = ofile
    def __repr__(self):
        return "<sym:%s>" % (self.name)

def skip_until_line_contains(f, string):
    for line in f:
        if (string in line):
            return

def split_lib(libline):
	"""Returns lib (.a) and object files (.o)"""
	if not "(" in libline:
		assert libline.endswith(".o")
		assert not " " in libline
		return (), libline
	i = libline.index('(')
	afile = libline[:i]
	ofiles = libline[i+1:-1]
	return afile, ofiles

def read_map_file(path):
	# The output of this cell:
	sections = dict()
	symbols = list()
	global_cross_references = dict()

	def split_symbol_line(line):
		parts = line.split()
		if line.startswith("  "):
			section = None
			pos, size = parts[0].split('+')
			pos = int(pos, 16)
			size = int(size, 16)
		else:
			section = parts[0]
			pos, size = parts[1].split('+')
			pos = int(pos, 16)
			size = int(size, 16)
		name = parts[-1]
		if len(parts) == 4: # global symbols
			lib = parts[-2]
		else: # local symbols
			lib = None
		return section, pos, name, size, lib

	with open(path) as f:
		# Read section info
		skip_until_line_contains(f, "Image Summary")
		for line in f:
			if line == "\x0c\n": break
			if not line.startswith("  ."): continue
			name,base,size_hex,size_dec,secoffs = line.split()
			if name in sections:
				sections[name].size += int(size_dec)
			else:
				sections[name] = Section(name, int(size_dec))
		# Read Module
		skip_until_line_contains(f, "Module Summary")
		#    ignore...
		# Read Global Symbols
		skip_until_line_contains(f, "Global Symbols")
		for line in f: break # skip one line
		for line in f: # skip non-section entries
			if not line.startswith("   "): break
		for line in f:
			if line == "\x0c\n": break
			sec_name, start, name, size, lib = split_symbol_line(line)
			if ".." in name: # Not a real symbol
				continue
			assert not lib # not for global symbols
			section = sections.get(sec_name, None)
			sym = Symbol(name, section, size)
			if sym.size > 0:
				if sym.size > 300000:
					print("Oversized?", sym.name, sym.size)
				symbols.append(sym)
				
		# Read Local Symbols
		### TODO contains global references as well
		skip_until_line_contains(f, "Local Symbols")
		for line in f: break # skip one line
		for line in f: # skip non-section entries
			if not line.startswith("   "): break
		prev_line = None # trailing one behind for size computation
		prev_section = None # Necessary for jump targets like ".L1243"
		for line in f:
			if line == "\x0c\n": break
			sec_name, start, name, size, lib = split_symbol_line(line)
			if ".." in name: # Not a real symbol
				continue
			section = sections.get(sec_name, None)
			afile, ofile = split_lib(lib)
			sym = Symbol(name, section, size, afile, ofile)
			if sym.size > 0 and sym.section:
				if sym.size > 300000:
					print("Oversized local?", sym.name, sym.size)
				symbols.append(sym)
				if name in global_cross_references:
					global_cross_references[name].append(lib)
				else:
					global_cross_references[name] = [lib]
			prev_line = line
			prev_section = section
			

		# Read Global Cross Reference
		skip_until_line_contains(f, "Cross")
		symbol_collection = list()
		ofile_collection = list()
		for line in f:
			if line == "\n": continue
			if line.startswith(" "): # add ofile
				ofile_collection.append(line.split()[0])
			else: # add symbol
				if ofile_collection: # store the previous package
					for s in symbol_collection:
						for o in ofile_collection:
							if not s in global_cross_references:
								global_cross_references[s] = list()
							global_cross_references[s].append(o)
					ofile_collection = list()
					symbol_collection = list()
				parts = line.split()
				symbol_collection.append(parts[0])
				if len(parts) > 1:
					ofile_collection.append(parts[1])
	# Some symbols have no o/a file assigned, because the global cross references are necessary.
	# Update them now.
	for s in symbols:
		if s.ofile: continue
		assert not s.afile, "symbol has ofile but not afile??"
		if s.name in global_cross_references:
			cunits = global_cross_references[s.name]
			# TODO: There is more than one entry, but we just use the first one for now
			cunits = cunits[0]
			if cunits in BUILDINFO_FILES:
				s.ofile = cunits
				continue
			ofile, afile = split_lib(cunits)
			s.afile = afile
			s.ofile = ofile
	return sections, symbols, global_cross_references

_LFILES = {
    'libgen.a': 'BSW',
    'librba.a': 'BSW',
    'libper.a': 'PER',
    'libtia.a': 'SIT',
    'libsit_x.a': 'SIT',
    'libvmc.a': 'VMC',
    'libfco_x.a': 'FCT',
    'librpm.a': 'RPM',
    'libdaddy.a': 'INT',
    'libnet.a': 'BSW',
    'libscheduling.a': 'BSW',
    'RTAOS.a': 'BSW',
    'libsys.a': 'BSW',
    'libcom.a': 'BSW',
    'libvx1000.a': 'BSW',
    'libecush.a': 'BSW',
    'libecuid.a': 'BSW',
    'libecu_shutdown.a': 'BSW',
    'librtaos.a': 'BSW',
    'libmath_sd.a': 'BSW',
    'libansi.a': 'BSW',
    'libsyslog.a': 'BSW',
    'libfmalloc.a': 'BSW',
    'libdomainlib.a': 'BSW',
    'libsedgnoe_xvtbl.a': 'BSW',
    'libicu.a': 'BSW',
    'libalgos.a': 'BSW',
    'libsystem.a': 'BSW',
    'libdcom.a': 'BSW',
    'libmcal.a': 'BSW',
    'libmt.a': 'BSW',
    'libind_sd.a': 'BSW',
    'libtraphandler.a': 'BSW',
    'libar4.a': 'BSW',
    'XcpSeedKey.a': 'BSW',
    'libfw_dsm.a': 'BSW',
    'libdsm_1r1v.a': 'BSW',
	'ebrobinos_ehr_010400.a': 'PER',
	'ebrobinos_ehr_010501.a': 'PER',
	'librte.a': 'BSW',
	'libccf_data.a': 'BSW',
	'libnet_ipma_deser.a': 'BSW',
	'libevm.a': 'BSW',
	'libpdm.a': 'BSW',
	'libmem.a': 'BSW',
	'libcubas.a': 'BSW',
	'lib1r1v_int.a': 'INT',
	'libapl_cubas.a': 'BSW',
	'libip_if.a': 'BSW',
	'libapl_main.a': 'INT',
	'libdc_fw_vmc_lib.a': 'VMC',
	'libapl_net.a': 'BSW',
	'libapl_fct.a': 'FCT',
	'libapl_sit.a': 'SIT',
	'libapl_per.a': 'PER',
	'libapl_rte.a': 'BSW',
	'libapl_vmc.a': 'VMC',
	'libapl_int.a': 'INT',
	'libapl_dsm.a': 'BSW',
	'libapl_dem.a': 'BSW',
	'libapl_rpm.a': 'RPM',
	'libapl_dcm.a': 'BSW',
	'libapl_edr.a': 'EDR',
	'libapl_memstack.a': 'BSW',
	'libapl_variant_handler.a': 'CCD',
	'libapl_pdmcus.a': 'BSW',
	'libapl_preintegration.a': 'BSW',
	'libapl_rbaCDD_CCF_x.a': 'BSW',
	'libIoExt.a': 'BSW',
	'libdc_fw_sit_lib.a': 'SIT',
	'libdc_fw_per_lib.a': 'PER',
	'libdc_fw_rpm_lib.a': 'RPM',
	'libdc_fw_dsm_lib.a': 'DSM',
	'libapl_ccf_data.a': 'BSW',
	'libvmc_core_lib.a': 'VMC',
	'librba_cubas.a': 'BSW',
	'JLR_L663_MY20_DDM.a': 'BSW',
	'libapl_cubas_gen_base.a': 'BSW',
	'DADCMaster.a': 'BSW',
	'libsedgnoe.a': 'INT',
	'librbHwCfgCheck_cfg.a': 'BSW',
	'libbist.a': 'BSW',
	'libstartup_cfg.a': 'BSW',
	'librbMemProt.a': 'BSW',
	'DADCAutoTrMaster.a': 'BSW',
	'librbSysLog.a': 'BSW',
	'libapl__Hacked_driver_.a': 'BSW',
	'librbSysEvM.a': 'BSW',
	'librbPda.a': 'BSW',
	'librbSftMon.a': 'BSW',
	'librbTrapHandler.a': 'BSW',
	'librbHwCfgCheck.a': 'BSW',
	'libvx1100.a': 'BSW',
	'libIoExt_cfg.a': 'BSW',
	'libapl_net_NI5.a': 'BSW',
	'libapl_cubas_gen_base_NI5.a': 'BSW',
	'libapl_dem_NI5.a': 'BSW',
	'libapl_rte_NI5.a': 'BSW',
	'libapl_rbaSigGrp_Ada_NI5.a': 'BSW',
	'libapl_ccf_data_NI5.a': 'BSW',
	'libapl_variant_handler_NI5.a': 'CCD',
	'libapl_smu.a': 'BSW',
	'libapl_rbaCDD_CCF_x_NI5.a': 'BSW',
	'libapl_ccd.a': 'CCD',
	'libapl_npp.a': 'FCT',
	'libRA5_apl_guam.a': 'BSW',
	'libapl_dcm_NI5.a': 'FCT',
	'libapl_ecuid.a': 'BSW',
	'libapl_ecu_shutdown.a': 'BSW',
	'librbMonReact.a': 'BSW',
	'librbNetScheduler.a': 'BSW',
}
_OFILES = {
    'copy_c0_to_c1.o': 'COPY',
    'copy_c1_to_c0.o': 'COPY',
    'copy_c1_to_c0_user.o': 'COPY',
    'copy_c0_to_c1_user.o': 'COPY',
    'scom_env_copy_tasks.o': 'COPY',
    'rba_EthDHCP_Client.c.o': 'BSW',
    'DoIP_SoAdTpCopyRxData.c.o': 'BSW',
    'per_sppVObjPolarRunnable.cpp.o': 'PER',
}

_SERVICE_TO_SUBSY = {
	'EnvModel': 'PER',
	'HV': 'PER',
	'Bs': 'SIT',
	'Bc': 'SIT',
	'Rpm': 'RPM',
	'rbDasyEvM': 'BSW',
	'DraReadRteRunnable': 'BSW',
}

def classify_mempool(symbol):
	"""Returns subsystem name of a mempool symbol or None if its not a mempool"""
	if not symbol.startswith("g_"):
		return None
	if not symbol.endswith("__4scom"):
		# Not a mempool (or not following ScomGen naming scheme)
		return None
	PREFIXES = ("g_JLR_L663_", "g_PL_AD_fw_PL_AD_", "g_PL_AD_fw_DACoreBT_", "g_PL_AD_fw_DACoreCyclic_", "g_PL_AD_fw_PL_DASy_")
	for p in PREFIXES:
		if symbol.startswith(p):
			symbol = symbol[len(p):]
			i = symbol.index("_")
			symbol = symbol[:i]
			if symbol in ("Dra", "evmApplRunnable", "PDM", "DSM", "NET"):
				return "BSW"
			symbol = _SERVICE_TO_SUBSY.get(symbol, symbol)
			return symbol

BUILDINFO_FILES = ("buildinfo.o", "buildinfo.c.o", "build_version_info.c.o")

def classify_by_lib(symbol):
    """Returns subsystem name of a symbol"""
    libs = global_cross_references.get(symbol, [])
    if not libs:
        return None
    for lib in libs:
        if not "(" in lib:
            if lib in BUILDINFO_FILES:
                return "INT"
            else:
                continue
        i = lib.index("(")
        lfile = lib[:i]
        ofile = lib[i+1:-1]
        if ofile in _OFILES:
            return _OFILES[ofile]
        if lfile in _LFILES:
            return _LFILES[lfile]
    #print("Not via lib:", symbol, libs)

def SuSy_of(symbol):
    """Returns a string like 'PER' which classifies the symbol name"""
    subsy = classify_mempool(symbol)
    if subsy:
        return subsy
    subsy = classify_by_lib(symbol)
    if subsy:
        return subsy
    return "?"

def compute_section_size(symbols):	
	# Sum up symbols for each section
	section_size = dict()
	unaccounted = list()

	for s in symbols:
		key = (s.section, SuSy_of(s.name))
		if not key in section_size:
			section_size[key] = 0
		section_size[key] += s.size
		if s.section and key[1] == "?" and s.size > 0:
			unaccounted.append(s)
		
	# FIXME We should classify these
	unaccounted.sort(key=lambda s: -s.size)
	total = 0
	for s in unaccounted[:10]:
		total += s.size
		#if s.section.name != ".Applpfls0.user_text": continue
		print("Unaccounted:", s.size, s.name, s.section.name, global_cross_references.get(s.name, "---"))
	print("Total Unaccounted Bytes:", total)
	return section_size
	
def store_csv_report(path, section_size):
	"""Store result csv file"""
	with open(path, 'wb') as f:
		w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, escapechar='\\')
		w.writerow(['Section', 'MemType', 'broadly', 'SuSy', 'Size (bytes)', 'Quota'])
		for sec, size in section_size.items():
			if size == 0: continue
			quota = "%.5f" % (get_quota(size, sec[0].name))
			memtype, cpuid, broad = get_memory_type(sec[0].name)
			w.writerow([sec[0].name, memtype, broad, sec[1], size, quota])
			#print(sec, size)
	
def store_all_symbols(path, symbols):
	"""Store a list of all symbols as csv file"""
	with open(path, 'wb') as f:
		w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, escapechar='\\')
		w.writerow(['Size (bytes)', 'Symbol', 'SuSy', 'Section', 'MemType', 'broadly', '.a', '.o'])
		for symbol in symbols:
			if symbol.size == 0: continue
			m, cpuid, b = get_memory_type(symbol.section.name)
			w.writerow((symbol.size, symbol.name, SuSy_of(symbol.name), symbol.section.name, m, b, symbol.ofile, symbol.afile))
			
MAX_SECTION_QUOTA = 10.0
def print_section_details(section_size, memtype, cpuid, max_bytes):
	smallers = False
	for (sec, susy), size in section_size.items():
		memtype_s, cpuid_s, broad = get_memory_type(sec.name)
		if memtype_s != memtype or cpuid_s != cpuid: continue
		quota = 100.0 * size / max_bytes
		if quota < MAX_SECTION_QUOTA:
			smallers = True
			continue
		print("  %-6s %4d KiB  %3.0f%%   %s " % (susy, size / 1024, quota, sec.name))
	if smallers:
		print("  ... and other sections with less then %d%%" % (MAX_SECTION_QUOTA))

def print_quota_warnings(section_size):
	full_section_size = dict()
	full_section_size_ASW = dict()
	unknown_sections = set()
	for k, size in section_size.items():
		sec, susy = k
		memtype, cpuid, broad = get_memory_type(sec.name)
		if memtype == "?":
			unknown_sections.add(sec.name)
		if not (memtype, cpuid) in full_section_size:
			full_section_size[(memtype, cpuid)] = 0
			full_section_size_ASW[(memtype, cpuid)] = 0
		full_section_size[(memtype, cpuid)] += size
		if susy in ASW_SUBSYS:
			full_section_size_ASW[(memtype, cpuid)] += size
	for mc, size in full_section_size.items():
		memtype, cpuid = mc
		max_bytes = get_maximum_bytes(memtype, cpuid)
		max_ASW_bytes = get_maximum_ASW_bytes(memtype, cpuid)
		assert max_ASW_bytes >= 0, (memtype, cpuid, max_ASW_bytes)
		quota = float(size) / max_bytes
		ASW_size = full_section_size_ASW[mc]
		if max_ASW_bytes == 0:
			continue
		ASW_quota = float(ASW_size) / max_ASW_bytes
		if cpuid == -1:
			name = memtype
		else:
			name = "%s_%d" % (memtype, cpuid)
		print("%-8s: %4d KiB  %.0f%% of %d KiB" % (name, size/1024, quota*100, max_bytes/1024))
		print("          %4d KiB  %.0f%% of %d KiB for ASW only" % (ASW_size/1024, ASW_quota*100, max_ASW_bytes/1024))
		rest = min(max_bytes - size, max_ASW_bytes - ASW_size)
		print("          %4d KiB available for ASW" % (rest/1024))
		print_section_details(section_size, memtype, cpuid, max_bytes)
	if unknown_sections:
		s = ", ".join(unknown_sections)
		print()
		print("Unknown sections:", s)
		print("Please extend this script!")

def emem_used(section_size):
	sum = 0
	for ((sec, susy), size) in section_size.items():
		memtype, cpuid, broad = get_memory_type(sec.name)
		if memtype != 'EMEM': continue
		sum += size
	return sum
	
def print_per_subsy_memory(section_size):
	"""Returns if any quota is over 100%"""
	data = dict()
	for k, size in section_size.items():
		sec, subsy = k
		memtype, cpuid, broad = get_memory_type(sec.name)
		if not subsy in data:
			data[subsy] = dict()
		if broad in data[subsy]:
			data[subsy][broad] += size
		else:
			data[subsy][broad] = size
	over_quota = False
	total_ram = total_rom = 0
	print("SubSy        RAM              ROM")
	for subsy, d in data.items():
		marker = ""
		ram = d.get('RAM', 0)
		total_ram += ram
		ram_max = RAM_BUDGETS.get(subsy, 0)
		if ram_max > 0:
			q = float(ram) / ram_max
			if q > 1.0:
				over_quota = True
				marker = " (OVERFLOW!)"
			ram_quota = "%.0f%%" % (100.0 * q)
		else:
			ram_quota = ''
		rom = d.get('ROM', 0)
		total_rom += rom
		rom_max = ROM_BUDGETS.get(subsy, 0)
		if rom_max > 0:
			q = float(rom) / rom_max
			if q > 1.0:
				over_quota = True
				marker = " (OVERFLOW!)"
			rom_quota = "%.0f%%" % (100.0 * q)
		else:
			rom_quota = ''
		print("%5s: %4d KiB  %3s   %4d KiB  %3s%s" % (subsy, ram / 1024, ram_quota, rom / 1024, rom_quota, marker))
	print()
	
	q = 100.0 * total_ram / TOTAL_RAM_BUDGET
	print("Total RAM: %5d KiB   %.0f%% of %d KiB budget" %\
		(total_ram / 1024, q, TOTAL_RAM_BUDGET / 1024))
	if q > 100.0:
		over_quota = True
		
	q = 100.0 * total_rom / TOTAL_ROM_BUDGET
	print("Total ROM: %5d KiB   %.0f%% of %d KiB budget" %\
		(total_rom / 1024, q, TOTAL_ROM_BUDGET / 1024))
	if q > 100.0:
		over_quota = True
	return over_quota

def subtract_stack_from_RAM(sections):
	for i in range(0,5):
		ustack = sections[".CPU%d.ustack" % i]
		DASY_MEMORY['DSPR'][i] -= ustack.size
		ASW_BUDGETS['DSPR'][i] -= ustack.size
		istack = sections[".CPU%d.istack" % i]
		DASY_MEMORY['DSPR'][i] -= istack.size
		ASW_BUDGETS['DSPR'][i] -= istack.size
		csa = sections[".CPU%d.csa" % i]
		DASY_MEMORY['DSPR'][i] -= csa.size
		ASW_BUDGETS['DSPR'][i] -= csa.size

if __name__ == "__main__":
	assert(MAP_FILE.endswith(".map"))
	sections, symbols, global_cross_references = read_map_file(MAP_FILE)
	subtract_stack_from_RAM(sections)
	section_size = compute_section_size(symbols)
	store_csv_report("ram_rom_report_%s.csv" % ARGS.dasy, section_size)
	store_all_symbols("all_symbols_%s.csv" % ARGS.dasy, symbols)
	print()
	print_quota_warnings(section_size)
	print()
	over_quota = print_per_subsy_memory(section_size)
	
	# EMEM is special!
	emem_max = DASY_MEMORY['EMEM'][-1]
	emem = emem_used(section_size)
	quota = 100 * emem / emem_max
	print("\nEMEM used: %d%% KiB   %d of %d KiB" % (quota, emem / 1024, emem_max / 1024))
	
	if over_quota:
		print("Error: Memory quota overflow. Contact your software architect.")
		sys.exit(1)
	
	#dummy = input("Press enter")
