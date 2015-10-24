#!/bin/sh
# Build the photran source tarball.
#
# Get some variables from the specfile
eval `awk '$1 == "%global" { print $2 "=" $3 }' eclipse-photran.spec`

# Checkout and create photran tarball
[ ! -d org.eclipse.photran ] && git clone git://git.eclipse.org/gitroot/ptp/org.eclipse.photran.git
pushd org.eclipse.photran
git pull
git archive --prefix org.eclipse.photran-$photran_git_tag/ $photran_git_tag | xz -c > ../org.eclipse.photran-${photran_git_tag}.tar.xz
popd
