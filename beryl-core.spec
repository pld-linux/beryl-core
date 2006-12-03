#
# TODO: python
#
Summary:	OpenGL window and compositing manager
Summary(pl):	OpenGL-owy zarz±dca okien i sk³adania
Name:		beryl-core
Version:	20061201
Release:	1
License:	MIT
Group:		X11
#Source0:	http://distfiles.xgl-coffee.org/beryl-core/%{name}-%{version}.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	5c0ac3fcc25e8e3936e854dcff5d1b05
Source1:	beryl-mesa-%{version}.tar.bz2
# Source1-md5:	c9a58134b47f871daefe815d9c7b5692
Patch0:		%{name}-aiglx.patch
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	intltool
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-modules >= 1:2.2
BuildRequires:	startup-notification-devel >= 0.7
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXcomposite-devel >= 0.3
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-util-makedepend
Provides:	compiz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Beryl is an OpenGL compositing manager that use
GLX_EXT_texture_from_pixmap for binding redirected top-level windows
to texture objects. It has a flexible plug-in system and it is
designed to run well on most graphics hardware.

This is an enhanced version of compiz, developed mainly by Quinnstorm.
Some parts were optimized for speed and there were added few
additional plugins and patches, delivering even more eyecandy.

%description -l pl
Beryl jest OpenGL-owym zarz±dc± sk³adania, u¿ywaj±cym rozszerzenia
GLX_EXT_texture_from_pixmap w celu wi±zania przekierowanych okien do
tekstur. Posiada elastyczny system wtyczek i jest tak zaprojektowany,
by dobrze dzia³aæ na wiêkszo¶ci kart graficznych.

To jest udoskonalona wersja compiza, tworzona g³ównie przez
Quinnstorma. Niektóre czê¶ci zosta³y zoptymalizowane pod wzglêdem
prêdko¶ci oraz dodano kilka dodatkowych wtyczek i ³atek,
dostarczaj±cych jeszcze wiêcej ¶wiecide³ek.

%package devel
Summary:	Header files for beryl
Summary(pl):	Pliki nag³ówkowe dla beryla
Group:		Development
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-devel
Requires:	libpng-devel
Requires:	startup-notification-devel >= 0.7
Requires:	xorg-lib-libSM-devel
Requires:	xorg-lib-libXcomposite-devel >= 0.3
Requires:	xorg-lib-libXdamage-devel
Requires:	xorg-lib-libXrandr-devel
Conflicts:	compiz-devel

%description devel
Header files for beryl.

%description devel -l pl
Pliki nag³ówkowe dla beryla.

%prep
%setup -q -a1 -n %{name}
%patch0 -p1

%build
autoreconf -v --install
%{__glib_gettextize}
intltoolize --automake --copy --force

# bashizms inside
sed -i -e 's@^#! /bin/sh$@#!/bin/bash@' configure

%configure \
	--disable-static \
	--with-berylmesadir=beryl-mesa
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*.*.*
%dir %{_libdir}/beryl
%dir %{_libdir}/beryl/backends
%attr(755,root,root) %{_libdir}/beryl/backends/*.so
%{_libdir}/beryl/backends/*.la
%{_datadir}/beryl
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/beryl
%{_pkgconfigdir}/*.pc
%{_mandir}/man3/*.3*
