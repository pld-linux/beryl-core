#
# TODO: python
#
# Conditional build:
%bcond_with	beryl_mesa
#
Summary:	OpenGL window and compositing manager
Summary(pl):	OpenGL-owy zarz±dca okien i sk³adania
Name:		beryl-core
Version:	0.1.3
Release:	1
Epoch:		1
License:	MIT
Group:		X11
Source0:	http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	24caed8a8cb50fd30823a9ee182f85f4
Source1:	http://releases.beryl-project.org/%{version}/beryl-mesa-%{version}.tar.bz2
# Source1-md5:	c22765c2637846907ee6154b548151e9
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.9
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-modules >= 1:2.2
BuildRequires:	sed >= 4.0
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
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
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
%setup -q %{?with_beryl_mesa: -a1}
mv -f po/{ca_ES,ca}.po
mv -f po/{es_ES,es}.po
mv -f po/{fr_FR,fr}.po
mv -f po/{hu_HU,hu}.po
mv -f po/{it_IT,it}.po
mv -f po/{ja_JP,ja}.po
mv -f po/{ko_KR,ko}.po
mv -f po/{pt_PT,pt}.po
mv -f po/{sv_SE,sv}.po
# sv_FI is identical to sv_SE

# NOTE: check the list ofter any upgrade!
cat > po/LINGUAS <<EOF
ca
es
es_AR
fr
hu
it
ja
ko
pt_BR
pt
sv
zh_CN
zh_HK
zh_TW
EOF

sed -i 's/bin_PROGRAMS = beryl beryl-settings-dump beryl-xgl/bin_PROGRAMS = beryl beryl-settings-dump/' src/Makefile.am

%build
%{__glib_gettextize}
%{__intltoolize} --automake
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

# bashisms inside
sed -i -e 's@^#! /bin/sh$@#!/bin/bash@' configure

%configure \
	%{?with_beryl_mesa:--with-berylmesadir=beryl-mesa} \
	--disable-static
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
# XXX: check if needed (I don't see libltdl in BRs)
%{_libdir}/beryl/backends/*.la
%{_datadir}/beryl
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/beryl
%{_pkgconfigdir}/*.pc
%{_mandir}/man3/*.3*
