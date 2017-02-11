# gcc-4.4 is currently too old to compile pzstd
%if 0%{?fedora} || 0%{?rhel} > 6
# aarch64 and armv7hl at least currently segfault
# in ThreadPool test for the pzstd util
%ifarch %{ix86} x86_64
%global with_pzstd 1
%endif
%endif

Name:           zstd
Version:        1.1.1
Release:        2%{?dist}
Summary:        Zstd compression library

License:        BSD and MIT
URL:            https://github.com/facebook/zstd
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# https://github.com/facebook/zstd/pull/404
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
%if 0%{?with_pzstd}
%patch1 -p1
%endif

%build
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;}
for dir in lib programs; do
  CFLAGS="%{optflags}" %make_build -C "$dir"
done
%if 0%{?with_pzstd}
CFLAGS="%{optflags}" CXXFLAGS="%{optflags} -std=c++11" %make_build -C 'contrib/pzstd'
%endif

%check
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;}
CFLAGS="%{optflags}" make -C tests test-zstd
%if 0%{?with_pzstd}
CFLAGS="%{optflags}" CXXFLAGS="%{optflags} -std=c++11" make -C contrib/pzstd test
%endif

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
rm %{buildroot}/%{_libdir}/libzstd.a
%if 0%{?with_pzstd}
install -D -m755 contrib/pzstd/pzstd %{buildroot}/usr/bin/pzstd
install -D -m644 programs/%{name}.1 %{buildroot}/%{_mandir}/man1/p%{name}.1
%endif

%files
%doc NEWS README.md
%{_bindir}/%{name}
%if 0%{?with_pzstd}
%{_bindir}/p%{name}
%{_mandir}/man1/p%{name}.1*
%endif
%{_bindir}/un%{name}
%{_bindir}/%{name}cat
%{_mandir}/man1/%{name}.1*
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
%{_includedir}/zstd_errors.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%post -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 02 2016 Pádraig Brady <pbrady@redhat.com> - 1.1.1-1
- Latest upstream

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
