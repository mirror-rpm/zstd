Name:           zstd
Version:        1.1.0
Release:        2%{?dist}
Summary:        Zstd compression library

License:        BSD and MIT
URL:            https://github.com/facebook/zstd
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Proposed upstream at https://github.com/facebook/zstd/pull/404
Patch0:         zstd-lib-no-rebuild.patch
Patch1:         pzstd.1.patch

BuildRequires:  gcc gtest-devel

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

%package -n lib%{name}
Summary:        Zstd shared library

%description -n lib%{name}
Zstandard compression shared library.

%package -n lib%{name}-devel
Summary:        Header files for Zstd library
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description -n lib%{name}-devel
Header files for Zstd library.


%prep
%setup -q
find -name .gitignore -delete
%patch0 -p1
%patch1 -p1

%build
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;}
for dir in lib programs; do
  CFLAGS="%{optflags}" %make_build -C "$dir"
done
CXXFLAGS="%{optflags}" %make_build -C 'contrib/pzstd'

%check
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;}
CFLAGS="%{optflags}" make -C tests test-zstd
CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" make -C contrib/pzstd test

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
install -D -m755 contrib/pzstd/pzstd %{buildroot}/usr/bin/pzstd
install -D -m644 programs/%{name}.1 %{buildroot}/%{_mandir}/man1/p%{name}.1
rm %{buildroot}/%{_libdir}/libzstd.a

%files
%doc NEWS README.md
%{_bindir}/%{name}
%{_bindir}/p%{name}
%{_bindir}/un%{name}
%{_bindir}/%{name}cat
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/p%{name}.1*
%{_mandir}/man1/un%{name}.1*
%{_mandir}/man1/%{name}cat.1*
%license LICENSE PATENTS

%files -n lib%{name}
%{_libdir}/libzstd.so.*
%license LICENSE PATENTS

%files -n lib%{name}-devel
%{_includedir}/zbuff.h
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%post -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig

%changelog
* Thu Oct 6  2016 Pádraig Brady <pbrady@fb.com> 1.1.0-2
- Add pzstd(1)

* Thu Sep 29 2016 Pádraig Brady <pbrady@fb.com> 1.1.0-1
- New upstream release
- Remove examples and static lib

* Mon Sep 12 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-2
- Adjust various upstream links
- Parameterize various items in spec file

* Mon Sep 5 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-1
- Initial release
