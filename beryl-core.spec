#
# Conditional build:
%bcond_without	beryl_mesa	# beryl-xgl statically linked with own libGL
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
Patch0:		%{name}-link.patch
URL:		http://beryl-project.org/
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.9
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
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
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	OpenGL-GLX-devel
Requires:	glib2-devel >= 2.0
Requires:	libpng-devel
Requires:	startup-notification-devel >= 0.7
Requires:	xorg-lib-libSM-devel
Requires:	xorg-lib-libXcomposite-devel >= 0.3
Requires:	xorg-lib-libXdamage-devel
Requires:	xorg-lib-libXinerama-devel
Requires:	xorg-lib-libXrandr-devel
Requires:	xorg-proto-glproto-devel

%description devel
Header files for beryl.

%description devel -l pl
Pliki nag³ówkowe dla beryla.

%package gconf
Summary:	GConf settings plugin for beryl
Summary(pl):	Wtyczka ustawieñ GConf dla beryla
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description gconf
GConf settings plugin for beryl.

%description gconf -l pl
Wtyczka ustawieñ GConf dla beryla.

%prep
%setup -q %{?with_beryl_mesa: -a1}
%patch0 -p1

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

rm -f $RPM_BUILD_ROOT%{_libdir}/beryl/backends/*.la

# program removed
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/beryl-settings-dump.1

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/beryl
%attr(755,root,root) %{_libdir}/libberylsettings.so.*.*.*
%dir %{_libdir}/beryl
%dir %{_libdir}/beryl/backends
%attr(755,root,root) %{_libdir}/beryl/backends/libini.so
%{_datadir}/beryl
%{_mandir}/man1/beryl.1*
%if %{with beryl_mesa}
%attr(755,root,root) %{_bindir}/beryl-xgl
%{_mandir}/man1/beryl-xgl.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libberylsettings.so
%{_libdir}/libberylsettings.la
%{_includedir}/beryl
%{_pkgconfigdir}/beryl.pc
%{_pkgconfigdir}/berylsettings.pc
%{_mandir}/man3/*.3*

%files gconf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/beryl/backends/libgconf.so
