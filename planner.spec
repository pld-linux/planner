#
# Conditional build:
%bcond_without	eds	# without evolution-data-server support
%bcond_without	pgsql	# without PostgreSQL storage module
#
Summary:	A project management program that can help build plans, and track the progress
Summary(pl):	System zarz�dzania projektem pomocny przy planowaniu i �ledzeniu post�pu
Summary(pt_BR):	Planner � um programa para gerenciamento de projetos
Name:		planner
Version:	0.14
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/planner/0.14/%{name}-%{version}.tar.bz2
# Source0-md5:	af54ef691bfa7fc24c7ad858d55fed4a
Patch0:		%{name}-desktop.patch
URL:		http://www.imendio.com/projects/planner/
BuildRequires:	GConf2-devel
BuildRequires:	automake
BuildRequires:	gnome-vfs2-devel >= 2.0.2
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.30
BuildRequires:	libgnomeprintui-devel >= 2.6.0
BuildRequires:	libgsf-devel >= 1.4.0
BuildRequires:	libxslt-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-pygtk-devel >= 1:2.0.0
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
%if %{with eds}
BuildRequires:	evolution-data-server-devel >= 1.2
%endif
%if %{with pgsql}
BuildRequires:	libgda-devel >= 1:1.2.3
BuildRequires:	postgresql-devel
%endif
Requires(post,preun):	GConf2
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires(post,postun):	shared-mime-info
%{?with_eds:Requires:	evolution-data-server >= 1.2}
Requires:	hicolor-icon-theme
Obsoletes:	libmrproject
Obsoletes:	mrproject
Obsoletes:	python-libmrproject
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libplanner-1.so.0

%description
A project management program that can help build project plans, and
track the progress of a project.

%description -l pl
Program wspomagaj�cy zarz�dzanie projektami, tworzenie plan�w i
�ledzenie post�pu w wykonaniu projektu.

%description -l pt_BR
Planner � um gerenciador de projetos baseado no GNOME.

%package devel
Summary:	Header files for planner library
Summary(pl):	Pliki nag��wkowe biblioteki planner
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0.4
Requires:	libgsf-devel >= 1.4.0
Requires:	libxml2-devel >= 2.5.4
Obsoletes:	libmrproject-devel
Obsoletes:	libmrproject-static

%description devel
Header files for planner library.

%description devel -l pl
Pliki nag��wkowe biblioteki planner.

%package storage-pgsql
Summary:	PostgreSQL storage module for Planner
Summary(pl):	Modu� przechowywania danych w bazie PostgreSQL dla Plannera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gda-postgres
Obsoletes:	libmrproject-storage-pgsql
Obsoletes:	mrproject-storage-pgsql

%description storage-pgsql
PostgreSQL storage module for Planner application.

%description storage-pgsql -l pl
Modu� przechowywania danych w bazie PostgreSQL dla Plannera.

%package -n python-planner
Summary:	Python binding for Planner library
Summary(pl):	Wi�zanie Pythona do biblioteki Planner
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs
Requires:	python-pygtk-devel >= 1.99.14

%description -n python-planner
Python binding for Planner library.

%description -n python-planner -l pl
Wi�zanie Pythona do biblioteki Planner.

%prep
%setup -q
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub .
%configure \
	--disable-update-mimedb \
	%{?with_eds:--enable-eds} \
	%{?with_pgsql:--enable-database} \
	--enable-gtk-doc \
	--enable-python \
	--enable-python-plugin \
	--enable-timetable
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir} \
	sqldocdir=%{_docdir}/%{name}-%{version} \
	sampledir=%{_examplesdir}/%{name}-%{version} \
	omf_dest_dir=%{_omf_dest_dir}

# useless - modules loaded through gmodule
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/{,*/}*.la

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/mime/{XMLnamespaces,globs,magic}
rm -f $RPM_BUILD_ROOT%{_datadir}/mime/application/*.xml

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%scrollkeeper_update_post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall %{name}.schemas

%postun
/sbin/ldconfig
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libplanner*.so.*.*

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/file-modules
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/storage-modules

%attr(755,root,root) %{_libdir}/%{name}/file-modules/*.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%if %{with pgsql}
%exclude %{_libdir}/%{name}/storage-modules/*sql.so
%endif
%attr(755,root,root) %{_libdir}/%{name}/storage-modules/*.so

%{_datadir}/%{name}
%{_desktopdir}/*
%{_iconsdir}/hicolor/*/*/*.png
%{_pixmapsdir}/*.png
%{_datadir}/mime/packages/*.xml
%{_omf_dest_dir}/planner-C.omf
%lang(eu) %{_omf_dest_dir}/planner-eu.omf
%{_examplesdir}/%{name}-%{version}
%{_sysconfdir}/gconf/schemas/%{name}.schemas

%files devel
%defattr(644,root,root,755)
%{_libdir}/libplanner*.la
%attr(755,root,root) %{_libdir}/libplanner*.so
%{_includedir}/planner-1.0
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/libplanner

%if %{with pgsql}
%files storage-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/storage-modules/*sql.so
%endif

%files -n python-planner
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/planner*.so
