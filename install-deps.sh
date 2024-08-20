set -e

EXTRACT_DIR=build/sysroot/usr
mkdir -p $EXTRACT_DIR

file=fcitx5-js-dev.tar.bz2
[[ -f cache/$file ]] || wget -P cache https://github.com/fcitx-contrib/fcitx5-js/releases/download/latest/$file
tar xjvf cache/$file -C $EXTRACT_DIR
