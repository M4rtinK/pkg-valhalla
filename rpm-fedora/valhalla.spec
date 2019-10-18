%global debug_package %{nil}

Summary: Open Source Routing Engine for OpenStreetMap
Name: valhalla
Version: 3.0.8
Release: 1%{?dist}
License: MIT
Group: Libraries/Location
URL: https://github.com/valhalla/valhalla

#Source: https://github.com/rinigus/valhalla
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++ libtool vim-enhanced
BuildRequires: zeromq-devel >= 4.1.4, czmq-devel >= 3.0, libcurl-devel >= 7.22.0
BuildRequires: cmake, lua, lua-devel, prime_server-devel == 0.6.3
BuildRequires: jq, protobuf-devel, libcurl-devel >= 7.22.0
BuildRequires: boost-devel >= 1.51, boost-chrono >= 1.51, boost-date-time >= 1.51, boost-filesystem >= 1.51
BuildRequires: boost-iostreams >= 1.51, boost-program-options >= 1.51, boost-regex >= 1.51
BuildRequires: boost-system >= 1.51, boost-thread >= 1.51
BuildRequires: lz4-devel >= 1.7.3, zlib-devel >= 1.2.8
BuildRequires: python3-devel
BuildRequires: python3
BuildRequires: boost-python3-devel
BuildRequires: sqlite-devel >= 3.0.0
BuildRequires: geos-devel
BuildRequires: libspatialite-devel
BuildRequires: glibc-common
BuildRequires: glibc-langpack-en

Requires: zeromq >= 4.1.4, czmq >= 3.0, libcurl >= 7.22.0, protobuf, prime_server == 0.6.3
Requires: boost-chrono >= 1.51, boost-date-time >= 1.51, boost-filesystem >= 1.51
Requires: boost-iostreams >= 1.51, boost-program-options >= 1.51, boost-regex >= 1.51
Requires: boost-system >= 1.51, boost-thread >= 1.51
Requires: lz4 >= 1.7.3, zlib >= 1.2.8

%description
Open Source Routing Engine for OpenStreetMap

%package devel
Summary: valhalla development headers
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package provides headers for development


%package tools
Summary: valhalla tools
Group: Libraries/Location
Requires: %{name} = %{version}

%description tools
Tools for valhalla

%prep
%setup -q -n %{name}-%{version}

%build
#PYTHON_DISALLOW_AMBIGUOUS_VERSION=0

mkdir build-rpm || true
cd build-rpm

CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"
%cmake ..  -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=OFF -DENABLE_DATA_TOOLS=ON -DENABLE_PYTHON_BINDINGS=ON -DENABLE_SERVICES=ON -DENABLE_NODE_BINDINGS=OFF
%{__make} %{?_smp_mflags}
cd ..

%install
cd build-rpm
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
cd ..

%clean
%{__rm} -rf %{buildroot}

%pre

%post -n valhalla -p /sbin/ldconfig

%postun -n valhalla -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_libdir}/libvalhalla.so*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/valhalla
%{_libdir}/libvalhalla.la
%{_libdir}/pkgconfig/libvalhalla.pc

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/valhalla_*

%changelog
* Fri Oct 18 2019 Martin Kolman <martin.kolman@gmail.com> - 3.0.8-1
- initial packaging release for Fedora

* Sat May 20 2017 rinigus <rinigus.git@gmail.com> - 2.2.4-1
- initial packaging release for SFOS
