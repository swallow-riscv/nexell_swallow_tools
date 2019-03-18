#!/usr/bin/env python
#

import sys
import os

PREBUILT_BBAPPEND_PATH = "/tools/bbappend-files"
INDEX_BBAPPEND=0
INDEX_GEN_PATH=1
INDEX_PATCH=2

R_NX_LIBS='/recipes-nexell-libs/nx-libs'
R_TESTSUITE='/recipes-application/testsuite'
R_SIMPLE_ENC_TEST='/recipes-application/simple-enc-test'

TEMPLATE1=[
    "### Nexell - For Yocto build with using local source, Below lines are auto generated codes",
    "",
    "S = \"${WORKDIR}/git\"",
    "",
    "do_myp() {",
    "    rm -rf ${S}",
    "    cp -a ${WORKDIR}${_SRC_PATH_BY_GEN_} ${S}",
    "    rm -rf ${WORKDIR}/home",
    "}",
    "addtask myp before do_patch after do_unpack",
    "",
]

TEMPLATE_SRC_URI="SRC_URI=\"file://${_SRC_PATH_BY_GEN_}\""

###  ---------------------------------------------------------------------------------------------------------------------------------------------------
###  ------------------------------------------------------------------ Usage --------------------------------------------------------------------------
###  ---------------------------------------------------------------------------------------------------------------------------------------------------
###  {bbappend file name : [[real src path, recipes location, /tmp/work/.../buildpath location], [patch file name]]}
###  ex)) 's5p6818-avn-ref-bl1.bbappend': ['OFF',['/bl1/bl1-s5p6818',R_BL1,'/bl1-s5p6818'], ['0001-s5p6818-avn-bl1.patch']],
###                    |                     |              |           |     |                      '--->> .patch file of bl1 recipe
###                    |                     |              |           |     '--->> /tmp/work/.../s5p6818-avn-ref-bl1/.../ src dir after copy .bbappend
###                    |                     |              |           '--->> meta-nexell/recipes-bsp/  path
###                    |                     |              '--->> local source path in Your Host PC
###                    |                     '----->> Use local source Yes or No
###                    '----->> This .bbappend file name have to same name .bb file in meta-nexell/recipes-xxx/
###  ---------------------------------------------------------------------------------------------------------------------------------------------------

HASH_RECIPENAME_PATH = {
    'nx-allocator_%.bbappend':          ['ON',['/library/nx-allocator',R_NX_LIBS,'/nx-allocator'],[]],
    'nx-scaler_%.bbappend':             ['ON',['/library/nx-scaler',R_NX_LIBS,'/nx-scaler'],[]],
    'nx-v4l2_%.bbappend':               ['ON',['/library/nx-v4l2',R_NX_LIBS,'/nx-v4l2'],[]],
    'nx-video-api_%.bbappend':          ['ON',['/library/nx-video-api',R_NX_LIBS,'/nx-video-api'],[]],

    'testsuite_%.bbappend' :            ['ON',['/apps/testsuite',R_TESTSUITE,'/testsuite'],[]],
    'simple-enc-test_%.bbappend' :      ['ON',['/apps/simple-enc-test',R_SIMPLE_ENC_TEST,'/simple-enc-test'],[]],
}

def gen_bbappend_paths(curWorkingPath) :
    bbfilesL = HASH_RECIPENAME_PATH.keys()
    bbfilesL.sort()
    for bbafile in bbfilesL :
        if HASH_RECIPENAME_PATH[bbafile][0]=='ON' :
	    gen_bbappend_files(bbafile, curWorkingPath, HASH_RECIPENAME_PATH[bbafile])

def gen_bbappend_files(bbappendfile,curWorkingPath,hashData) :
    L_PATHS = hashData[INDEX_GEN_PATH]
    L_PATCH_FILES = hashData[INDEX_PATCH]

    BBAPPEND_FILE_PATH = curWorkingPath + PREBUILT_BBAPPEND_PATH + L_PATHS[1] + '/' + bbappendfile

    INTO_BBAPPEND_SRC_PATH = curWorkingPath + L_PATHS[0]  #host PC's local source path
    INTO_BBAPPEND_MOV_PATH = curWorkingPath + L_PATHS[2]  #move to yocto tmp/work path
    INTO_BBAPPEND_PATCH_FILE=""
    print BBAPPEND_FILE_PATH + "  ---> OK "
    f = open(BBAPPEND_FILE_PATH,'w')

    #others
    for i in TEMPLATE1 :
        f.write(i+"\n")

    f.write("\n"+TEMPLATE_SRC_URI)
    f.write("\n")

    f.write("\n_SRC_PATH_BY_GEN_?=\""   + INTO_BBAPPEND_SRC_PATH + "\"")
    f.write("\n_MOV_PATH_BY_GEN_?=\""   + INTO_BBAPPEND_MOV_PATH + "\"")

    f.close()

def main(arg1):
    gen_bbappend_paths(arg1)

if __name__ == "__main__":
    try :
        main(sys.argv[1])
    finally :
        pass

