Name:           zstd
Version:        1.1.0
Release:        1%{?dist}
Summary:        Zstd compression library

License:        BSD and MIT
URL:            https://github.com/facebook/zstd
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Proposed upstream at https://github.com/pixelb/zstd/pull/1
Patch0:         zstd-lib-no-rebuild.patch

BuildRequires:  gcc

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

%build
for dir in lib programs; do
  CFLAGS="%{optflags}" LDFLAGS="%{__global_ldflags}" %make_build -C "$dir"
done

%check
CFLAGS="%{optflags}" LDFLAGS="%{__global_ldflags}" make -C tests test-zstd

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
rm %{buildroot}/%{_libdir}/libzstd.a

%files
%doc NEWS README.md
%{_bindir}/%{name}
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
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%post -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig

%changelog
* Thu Sep 29 2016 Pádraig Brady <pbrady@fb.com> 1.1.0-1
- New upstream release
- Remove examples and static lib

* Mon Sep 12 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-2
- Adjust various upstream links
- Parameterize various items in spec file

* Mon Sep 5 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-1
- Initial release
