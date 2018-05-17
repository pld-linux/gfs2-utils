# TODO: PLDify and install init script(?)
Summary:	Global File System 2 (GFS2) utilities
Summary(pl.UTF-8):	Narzędzia do systemu plików GFS2 (Global File System 2)
Name:		gfs2-utils
Version:	3.1.10
Release:	1
License:	LGPL v2.1+ (libraries), GPL v2+ (applications)
Group:		Applications/System
Source0:	http://releases.pagure.org/gfs2-utils/%{name}-%{version}.tar.xz
# Source0-md5:	31d330b1f69da8474a52bf36a824e9c1
Patch0:		%{name}-link.patch
URL:		https://pagure.io/gfs2-utils
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel >= 0.18
BuildRequires:	libblkid-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libuuid-devel
# for gfs2 headers
BuildRequires:	linux-libc-headers >= 7:3.3
BuildRequires:	ncurses-devel >= 5
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	uname(release) >= 3.3
Obsoletes:	gfs2 < 1:3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GFS2 is a cluster file system. It allows a cluster of computers to
simultaneously use a block device that is shared between them (with
FC, iSCSI, NBD, etc). GFS2 reads and writes to the block device like a
local file system, but also uses a lock module to allow the computers
coordinate their I/O so file system consistency is maintained. One of
the nifty features of GFS2 is perfect consistency - changes made to
the file system on one machine show up immediately on all other
machines in the cluster.

%description -l pl.UTF-8
GFS2 to klastrowy system plików. Pozwala klastrowi komputerów
jednocześnie używać urządzenia blokowego współdzielonego między sobą
(poprzez FC, iSCSI, NBD itp.). GFS2 wykonuje odczyty i zapisy na
urządzeniu blokowym tak, jak na lokalnym systemie plików, ale
wykorzystuje moduł blokujący, aby umożliwić komputerom koordynację
operacji wejścia-wyjścia w celu zachowania spójności systemu plików.
Jedną z bardziej istotnych cech systemu plików GFS2 jest idealna
spójność - zmiany wykonane na jednej maszynie są natychmiast widoczne
na wszystkich innych maszynach w klastrze.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's, po/Makefile.in$,,' configure.ac
%{__sed} -i -e '1s,#!/usr/bin/env python,#!/usr/bin/python,' gfs2/scripts/gfs2_{lockcapture,trace}

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-udevdir=/lib/udev

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/sbin
%{__mv} $RPM_BUILD_ROOT%{_sbindir}/{fsck.gfs2,mkfs.gfs2,gfs2_{grow,jadd,lockcapture,trace}} $RPM_BUILD_ROOT/sbin

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/gfs2-utils

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{COPYRIGHT,README.contributing,README.licence,gfs2.txt,journaling.txt}
%attr(755,root,root) /sbin/fsck.gfs2
%attr(755,root,root) /sbin/gfs2_grow
%attr(755,root,root) /sbin/gfs2_jadd
%attr(755,root,root) /sbin/gfs2_lockcapture
%attr(755,root,root) /sbin/gfs2_trace
%attr(755,root,root) /sbin/mkfs.gfs2
%attr(755,root,root) %{_sbindir}/gfs2_convert
%attr(755,root,root) %{_sbindir}/gfs2_edit
%attr(755,root,root) %{_sbindir}/gfs2_withdraw_helper
%attr(755,root,root) %{_sbindir}/glocktop
%attr(755,root,root) %{_sbindir}/tunegfs2
/lib/udev/rules.d/82-gfs2-withdraw.rules
%{_mandir}/man5/gfs2.5*
%{_mandir}/man8/fsck.gfs2.8*
%{_mandir}/man8/gfs2_convert.8*
%{_mandir}/man8/gfs2_edit.8*
%{_mandir}/man8/gfs2_grow.8*
%{_mandir}/man8/gfs2_jadd.8*
%{_mandir}/man8/gfs2_lockcapture.8*
%{_mandir}/man8/gfs2_trace.8*
%{_mandir}/man8/glocktop.8*
%{_mandir}/man8/mkfs.gfs2.8*
%{_mandir}/man8/tunegfs2.8*
