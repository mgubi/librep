# Copyright 1999-2008 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/dev-libs/librep/librep-0.90.5.ebuild,v 1.11 2006/10/20 00:24:49 kloeri Exp $

inherit eutils libtool toolchain-funcs multilib autotools

DESCRIPTION="Shared library implementing a Lisp dialect"
HOMEPAGE="http://librep.sourceforge.net/"
SRC_URI="mirror://sourceforge/${PN}/${P}.tar.bz2"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="alpha amd64 ia64 ppc sparc x86 ppc64"
IUSE="readline gmp libffi emacs"

RDEPEND=">=sys-libs/gdbm-1.8.3
	readline? ( sys-libs/readline )
	gmp? ( dev-libs/gmp )
	libffi? ( virtual/libffi )"

DEPEND="${RDEPEND}
	sys-apps/texinfo"

src_unpack() {
	unpack ${A}

	cd "${S}"

}

src_compile() {
	local myconf="$(use_with readline)"
	use ppc && myconf="${myconf} --with-stack-direction=1"

	# It seems that stack-direction=-1 for gcc-3.x and 1 for gcc-4.x on ia64
	if use ia64 && [[ $(gcc-major-version) -ge 4 ]]; then
		myconf="${myconf} --with-stack-direction=1"
	fi

	econf \
		--prefix=/usr \
		$(use_with gmp) \
		$(use_with libffi ffi) \
		$(use_with readline) \
		${myconf} || die "configure failed"

	emake || die "make failed"

}

src_install() {
	make DESTDIR="${D}" install || die "make install failed"

	dodoc AUTHORS BUGS ChangeLog COPYING HACKING INSTALL MAINTAINERS README THANKS TODO TREE
	docinto doc
	dodoc doc/*

}
