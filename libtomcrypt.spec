Name:           libtomcrypt
Version:        1.18.2
#Release:        3%%{?dist}
Release:        0%{?dist}
Summary:        A comprehensive, portable cryptographic toolkit
License:        Public Domain or WTFPL
URL:            http://www.libtom.net/

Source0:        https://github.com/libtom/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

%if (0%{?rhel} > 0 && 0%{?rhel} <= 7)
# Addresses python36- versus python3- dependencies
BuildRequires: epel-rpm-macros
%endif

BuildRequires:  ghostscript
BuildRequires:  libtommath-devel >= 1.0
BuildRequires:  libtool
BuildRequires:  texlive-latex-bin-bin
BuildRequires:  texlive-makeindex-bin
%if 0%{?rhel} == 8
BuildRequires:  texlive-metafont
%endif
BuildRequires:  texlive-mfware-bin
BuildRequires:  tex(cmr10.tfm)
BuildRequires:  tex(fancyhdr.sty)
BuildRequires:  tex(hyphen.tex)
%if 0%{?fedora} >= 28
BuildRequires:  tex(mf.mf)
%endif

%description
A comprehensive, modular and portable cryptographic toolkit that provides
developers with a vast array of well known published block ciphers, one-way hash
functions, chaining modes, pseudo-random number generators, public key
cryptography and a plethora of other routines.

Designed from the ground up to be very simple to use. It has a modular and
standard API that allows new ciphers, hashes and PRNGs to be added or removed
without change to the overall end application. It features easy to use functions
and a complete user manual which has many source snippet examples. 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Provides:       %{name}-doc = %{version}-%{release}
Obsoletes:      %{name}-doc < 1.17-19


%description    doc
The %{name}-doc package contains documentation for use with %{name}.

%prep
%setup -q

%build
%set_build_flags
export PREFIX="%{_prefix}"
export INCPATH="%{_includedir}"
export LIBPATH="%{_libdir}"
export EXTRALIBS="-ltommath"
export CFLAGS="%{build_cflags} -DLTM_DESC -DUSE_LTM"
%make_build V=1 -f makefile.shared library
%make_build V=1 -f makefile docs
%make_build V=1 -f makefile.shared test

%check
./test

%install
%make_install INSTALL_OPTS="-m 755" INCPATH="%{_includedir}" LIBPATH="%{_libdir}" -f makefile.shared

# Remove unneeded files
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

# Fix pkgconfig path
sed -i \
    -e 's|^prefix=.*|prefix=%{_prefix}|g' \
    -e 's|^libdir=.*|libdir=${prefix}/%{_lib}|g' \
    %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%doc doc/crypt.pdf

%changelog
* Mon May 13 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-0
- Add texlive-metafont for RHEL 8 to get /usr/bin/mf

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Simone Caronni <negativo17@gmail.com> - 1.18.2-1
- Udpate to 1.18.2.

* Wed Apr 18 2018 Simone Caronni <negativo17@gmail.com> - 1.18.1-5
- Update build requirement for texlive rebase.

* Mon Apr 09 2018 Rafael Santos <rdossant@redhat.com> - 1.18.1-4
- Fix missing Fedora linker flags (bug #1548709)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.18.1-2
- Switch to %%ldconfig_scriptlets

* Fri Dec 08 2017 Simone Caronni <negativo17@gmail.com> - 1.18.1-1
- Update to 1.18.1.

* Mon Oct 23 2017 Simone Caronni <negativo17@gmail.com> - 1.18.0-1
- Update to final 1.18.0.

* Sun Sep 17 2017 Simone Caronni <negativo17@gmail.com> - 1.18-2.20170915git0ceb1c1
- Update to latest snapshot post rc3.
- Remove RHEL 6 support.
- Clean up SPEC file.
- Trim changelog.

* Mon Sep 11 2017 Simone Caronni <negativo17@gmail.com> - 1.18-1.20170910git32d60ac
- Update to latest snapshot (post rc3).
- Version is now at 1.18.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-36.20170720gitab8c5b8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-35.20170720gitab8c5b8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Simone Caronni <negativo17@gmail.com> - 1.17-34.20170720gitab8c5b8
- Update to latest snapshot from the 1.18 release branch.
- Update license.

* Sun Jun 25 2017 Simone Caronni <negativo17@gmail.com> - 1.17-33.20170623gitcd6e602
- Update to latest snapshot.
- Update URL (#1463608, #1463547)

* Thu Jun 15 2017 Simone Caronni <negativo17@gmail.com> - 1.17-32.20170614git2cd69fb
- Update to latest snapshot, adjust build.
- Temporarily disable tests.

* Mon Mar 27 2017 Simone Caronni <negativo17@gmail.com> - 1.17-31.20170327git7532b89
- Update to latest snapshot.
- Use correct format for snapshots as per packaging guidelines.
- Use default compiler flags.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 09 2016 Than Ngo <than@redhat.com> - 1.17-29
- fix endian issues on s390x/ppc64

* Tue Feb 23 2016 Simone Caronni <negativo17@gmail.com> - 1.17-28
- Fix shared object name:
  https://github.com/libtom/libtomcrypt/commit/14272976d0615b546e9e0215ec4e2f01854a2dc9

* Tue Feb 23 2016 Simone Caronni <negativo17@gmail.com> - 1.17-27
- Fix FTBFS (#1307740).
- Update sources, requires libtommath 1.x, drop upstreamed patches.
- Update URL.
- Use license macro.
- Clean up SPEC file.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
