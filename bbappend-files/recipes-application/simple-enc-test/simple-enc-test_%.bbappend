### Nexell - For Yocto build with using local source, Below lines are auto generated codes

S = "${WORKDIR}/git"

do_myp() {
    rm -rf ${S}
    cp -a ${WORKDIR}${_SRC_PATH_BY_GEN_} ${S}
    rm -rf ${WORKDIR}/home
}
addtask myp before do_patch after do_unpack


SRC_URI="file://${_SRC_PATH_BY_GEN_}"

_SRC_PATH_BY_GEN_?="/home/ray/devel/drone/swallow-riscv/apps/simple-enc-test"
_MOV_PATH_BY_GEN_?="/home/ray/devel/drone/swallow-riscv/apps/simple-enc-test"
