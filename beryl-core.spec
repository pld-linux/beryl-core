Summary:	OpenGL window and compositing manager
Summary(pl):	OpenGL-owy zarz±dca okien i sk³adania
Name:		beryl-core
Version:	0.1.0
Release:	1
License:	GPL/MIT
Group:		X11
Source0:	http://distfiles.xgl-coffee.org/beryl-core/%{name}-%{version}.tar.bz2
# Source0-md5:	17fc446a78c557e02417b85ce7ea29e1
Patch0:		beryl-core-aiglx.patch
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	startup-notification-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-proto-glproto-devel
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
Requires:	OpenGL-devel
Requires:	libpng-devel
Requires:	startup-notification-devel >= 0.7
Requires:	xorg-lib-libSM-devel
Requires:	xorg-lib-libXcomposite-devel
Requires:	xorg-lib-libXdamage-devel
Requires:	xorg-lib-libXrandr-devel
Conflicts:	compiz-devel

%description devel
Header files for beryl.

%description devel -l pl
Pliki nag³ówkowe dla beryla.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
autoreconf -v --install
ln -s ../po config/po
#%{__intltoolize}
%{__glib_gettextize} --copy --force
rm config/po
sed -i -e 's/^mkinstalldirs.*/MKINSTALLDIRS=mkdir -p/' po/Makefile.in.in

%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	desktopfilesdir=%{_datadir}/wm-properties \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/beryl
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/beryl
%{_includedir}/beryl/beryl.h
%{_pkgconfigdir}/beryl.pc
