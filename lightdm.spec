# Conditional build:
%bcond_with	tests		# build without tests (tests fail mostly)
%bcond_without	qt4		# build without Qt4
%bcond_without	qt5		# build without Qt5

Summary:	A lightweight display manager
Summary(hu.UTF-8):	Egy könnyűsúlyú bejelentkezéskezelő
Name:		lightdm
# Odd versions are development, use only Even versions here (1.x = x odd/even)
Version:	1.28.0
Release:	2
# library/bindings are LGPLv2 or LGPLv3, the rest GPLv3+
License:	(LGPLv2 or LGPLv3) and GPLv3+
Group:		X11/Applications
Source0:	https://github.com/CanonicalLtd/lightdm/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	3e33b2bd15d769bbcc2e73ac94a1e1ea
Source1:	%{name}.pamd
Source2:	%{name}-autologin.pamd
Source3:	%{name}-greeter.pamd
Source4:	%{name}.init
Source5:	%{name}-tmpfiles.conf
Patch0:		config.patch
Patch1:		%{name}-nodaemon_option.patch
URL:		http://www.freedesktop.org/wiki/Software/LightDM
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.30
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel >= 0.9.5
BuildRequires:	gtk-doc
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgcrypt-devel
BuildRequires:	libtool
BuildRequires:	libxcb-devel
BuildRequires:	libxklavier-devel
BuildRequires:	pam-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.690
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
%if %{with qt4}
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	qt4-build
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5DBus-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	qt5-build
%endif
Requires:	/usr/bin/X
Requires:	dbus-x11
Requires:	lightdm-greeter
Requires:	xinitrc-ng >= 1.1-2
Provides:	XDM
Provides:	group(xdm)
Provides:	user(xdm)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define bashdir %{_sysconfdir}/bash_completion.d

%description
An X display manager that:
 - Has a lightweight codebase
 - Is standards compliant (PAM, ConsoleKit, etc)
 - Has a well defined interface between the server and user interface
 - Fully themeable (easiest with the webkit interface)
 - Cross-desktop (greeters can be written in any toolkit)

%description -l hu.UTF-8
Egy X bejelentkezéskezelő, amely:
 - pehelysúlyú kóddal rendelkezik
 - követi a standardokat (PAM, ConsoleKit, stb.)
 - jól-definiált felület a szerver és a felhasználói felület között
 - teljesen témázható (a legkönnyebb a webkit felülettel)
 - desktop-független (üdvözlők bármilyen eszközkészlettel írhatók)

%package libs-gobject
Summary:	LightDM GObject client library
Group:		Libraries
Obsoletes:	lightdm-libs < 1.7.0-0.6

%description libs-gobject
This package contains a GObject based library for LightDM clients to
use to interface with LightDM.

%package libs-gobject-devel
Summary:	Development files for %{name}-gobject
Group:		Development/Libraries
Group:		Libraries
Requires:	%{name}-libs-gobject = %{version}-%{release}

%description libs-gobject-devel
This package contains development files for a GObject based library
for LightDM clients to use to interface with LightDM.

%package libs-qt4
Summary:	LightDM Qt4 client library
Group:		Libraries
Obsoletes:	lightdm-libs-qt
Conflicts:	lightdm-libs < 1.7.0-0.6

%description libs-qt4
This package contains a Qt4 based library for LightDM clients to use
to interface with LightDM.

%package libs-qt4-devel
Summary:	Development files for %{name}-qt4
Group:		Development/Libraries
Requires:	%{name}-libs-qt4 = %{version}-%{release}
Obsoletes:	lightdm-libs-qt-devel

%description libs-qt4-devel
This package contains development files for a Qt4 based library for
LightDM clients to use to interface with LightDM.

%package libs-qt5
Summary:	LightDM Qt5 client library
Group:		Libraries

%description libs-qt5
This package contains a Qt5 based library for LightDM clients to use
to interface with LightDM.

%package libs-qt5-devel
Summary:	Development files for %{name}-qt5
Group:		Development/Libraries
Requires:	%{name}-libs-qt5 = %{version}-%{release}

%description libs-qt5-devel
This package contains development files for a Qt5 based library for
LightDM clients to use to interface with LightDM.

%package apidocs
Summary:	lightdm API documentation
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
lightdm API documentation.

%package init
Summary:	Init script for Lightdm
Summary(pl.UTF-8):	Skrypt init dla Lightdm-a
Group:		X11/Applications
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Obsoletes:	lightdm-upstart < 1.7.12-6

%description init
Init script for Lightdm.

%description init -l pl.UTF-8
Skrypt init dla Lightdm-a.

%package -n bash-completion-lightdm
Summary:        Bash completion for LightDM
Summary(pl.UTF-8):      Bashowe uzupełnianie parametrów dla LightDM
Group:          Applications/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
%if "%{_rpmversion}" >= "5" 
BuildArch:      noarch
%endif

%description -n bash-completion-lightdm
Bash completion for LightDM.

%description -n bash-completion-lightdm -l pl.UTF-8
Bashowe uzupełnianie parametrów dla LightDM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	%{__enable tests} \
	--enable-liblightdm-gobject \
	%{?with_qt4:--enable-liblightdm-qt} \
	%{?with_qt5:--enable-liblightdm-qt5} \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc \
	--with-greeter-session=lightdm-gtk-greeter \
	--with-greeter-user=xdm
%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL='install -p' \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{pam.d,security,rc.d/init.d,dbus-1/system.d} \
	$RPM_BUILD_ROOT%{bashdir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf.d \
	$RPM_BUILD_ROOT/home/services/xdm \
	$RPM_BUILD_ROOT%{_datadir}/xgreeters \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{remote-sessions,%{name}.conf.d} \
	$RPM_BUILD_ROOT%{systemdunitdir} \
	$RPM_BUILD_ROOT/var/lib/%{name}-data \
	$RPM_BUILD_ROOT/var/{log,cache}/%{name}

install -d $RPM_BUILD_ROOT{/var/run/lightdm,%{systemdtmpfilesdir}}
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/lightdm.conf

# initscripts
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/lightdm-autologin
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/lightdm-greeter
touch $RPM_BUILD_ROOT/etc/security/blacklist.%{name}

# We don't ship AppAmor
rm -rv $RPM_BUILD_ROOT/etc/apparmor.d

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{lb,wae}

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/bash-completion
cp -p data/bash-completion/{dm-tool,lightdm} $RPM_BUILD_ROOT%{bashdir}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 55 -r -f xdm
%useradd -u 55 -r -d /home/services/xdm -s /bin/false -c "X Display Manager" -g xdm xdm

%postun
if [ "$1" = "0" ]; then
	%userremove xdm
	%groupremove xdm
fi

%post	libs-gobject -p /sbin/ldconfig
%postun	libs-gobject -p /sbin/ldconfig

%post	libs-qt4 -p /sbin/ldconfig
%postun	libs-qt4 -p /sbin/ldconfig

%post	libs-qt5 -p /sbin/ldconfig
%postun	libs-qt5 -p /sbin/ldconfig

%post init
/sbin/chkconfig --add %{name}
%service -n %{name} restart
%systemd_reload

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	%service %{name} stop
fi

%postun init
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/%{name}.conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/keys.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/users.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm-autologin
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm-greeter
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.%{name}
/etc/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%attr(755,root,root) %{_bindir}/dm-tool
%attr(755,root,root) %{_sbindir}/lightdm
%attr(755,root,root) %{_libexecdir}/lightdm-guest-session
%{_libdir}/girepository-1.0/LightDM-1.typelib
%{systemdtmpfilesdir}/lightdm.conf
%{_datadir}/accountsservice/interfaces/org.freedesktop.DisplayManager.AccountsService.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.DisplayManager.AccountsService.xml
%{_datadir}/polkit-1/actions/org.freedesktop.DisplayManager.AccountsService.policy
%dir %{_datadir}/xgreeters
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/remote-sessions
%dir %{_datadir}/%{name}/%{name}.conf.d
%{_mandir}/man1/dm-tool.1*
%{_mandir}/man1/%{name}.1*
%dir %attr(710,root,root) /var/cache/%{name}
%dir %attr(710,root,root) /var/log/%{name}
%dir %attr(770,root,root) /var/run/%{name}
%dir %attr(700,root,root) /var/lib/%{name}-data
%dir %attr(750,xdm,xdm) /home/services/xdm

%files libs-gobject
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-gobject-1.so.0

%if %{with qt4}
%files libs-qt4
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblightdm-qt-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-qt-3.so.0

%files libs-qt4-devel
%defattr(644,root,root,755)
%{_libdir}/liblightdm-qt-3.la
%attr(755,root,root) %{_libdir}/liblightdm-qt-3.so
%{_includedir}/lightdm-qt-3
%{_pkgconfigdir}/liblightdm-qt-3.pc
%endif

%if %{with qt5}
%files libs-qt5
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblightdm-qt5-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-qt5-3.so.0

%files libs-qt5-devel
%defattr(644,root,root,755)
%{_libdir}/liblightdm-qt5-3.la
%attr(755,root,root) %{_libdir}/liblightdm-qt5-3.so
%{_includedir}/lightdm-qt5-3
%{_pkgconfigdir}/liblightdm-qt5-3.pc
%endif

%files libs-gobject-devel
%defattr(644,root,root,755)
%{_datadir}/gir-1.0/LightDM-1.gir
%{_includedir}/lightdm-gobject-1
%{_pkgconfigdir}/liblightdm-gobject-1.pc
%{_libdir}/liblightdm-gobject-1.la
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so
# -vala
%{_datadir}/vala/vapi/liblightdm-gobject-1.vapi
%{_datadir}/vala/vapi/liblightdm-gobject-1.deps

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/lightdm-gobject-1

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{systemdunitdir}/%{name}.service

%files -n bash-completion-lightdm
%defattr(644,root,root,755)
%{bashdir}/dm-tool
%{bashdir}/lightdm
