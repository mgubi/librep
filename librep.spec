Name: librep
Version: 0.90.5
Release: 1%{?dist}
Summary: An embeddable LISP environment
License: GPL
Group: Development/Languages
Source: http://download.sourceforge.net/librep/librep-%{version}.tar.bz2
URL: http://librep.sourceforge.net/
Packager: Christopher Bratusek <zanghar@freenet.de>
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gmp-devel gdbm-devel readline-devel texinfo libffi-devel

%if %{?_emacs_sitelispdir:1}%{!?_emacs_sitelispdir:0}
%define emacs_lispdir %{_emacs_sitelispdir}
%else
%define emacs_lispdir %{_datadir}/emacs/site-lisp
%endif

%description
This is a lightweight Lisp environment for UNIX. It contains a Lisp
interpreter, byte-code compiler and virtual machine. Applications may
use the Lisp interpreter as an extension language, or it may be used
for standalone scripts.

Originally inspired by Emacs Lisp, the language dialect combines many
of the elisp features while trying to remove some of the main
deficiencies, with features from Common Lisp and Scheme.

%package devel
Summary: librep include files and link libraries
Group: Development/Languages
Requires: %{name} = 0.90.5, pkgconfig

%description devel
Link libraries and C header files for librep development.

%package -n emacs-%{name}-el
Group: System Environment/Libraries
Summary: Emacs bindings for the librep main application

%description -n emacs-%{name}-el
The librep-emacs package contains the emacs related .el files so that librep
nicely interacts and integrates into emacs.

%prep
%setup -q

%build
%configure --with-readline --enable-shared
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc NEWS README THANKS TODO BUGS TREE HACKING
%dir %{_libdir}/rep/
%{_bindir}/rep
%{_bindir}/rep-remote
%{_datadir}/rep/
%{_datadir}/man/man1/rep*.gz
%{_infodir}/librep.info*
%{_libdir}/librep.so.*
%{_libdir}/rep/%{version}/%{_host}/

%files devel
%defattr(-,root,root,-)
%{_bindir}/rep-xgettext
%{_bindir}/repdoc
%{_includedir}/rep/
%{_libdir}/rep/%{_host}/
%{_libdir}/pkgconfig/librep.pc
%{_libdir}/librep.so
%exclude %{_libdir}/librep.la
%exclude %{_libdir}/librep.a

%files -n emacs-%{name}-el
%defattr(-,root,root,-)
%{emacs_lispdir}/*.el

%changelog
* Sat Sep 05 2009 Kim B. Heino <b@bbbs.net>
- add dist-tag, update buildrequires

* Sun Jan 18 2009 Christopher Bratusek <zanghar@freenet.de>
- several updates

* Fri Jan 02 2009 Christopher Bratusek <nano-master@gmx.de>
- source archive is a .tar.bz2

* Thu Dec 18 2008 Christopher Bratusek <nano-master@gmx.de>
- rep.m4 no longer available
- install librep.pc

* Tue Jun 13 2000 John Harper <john@dcs.warwick.ac.uk>
- use better macros

* Wed Nov 10 1999 Michael K. Johnson <johnsonm@redhat.com>
- post{,un} use -p

* Mon Sep 13 1999 Aron Griffis <agriffis@bigfoot.com>
- 0.5 spec file update: added buildroot
