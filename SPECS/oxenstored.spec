%global package_speccommit ef3ed5a07ec6a214089c0fa9d1e89ba85afc8a9b
%global package_srccommit v26.0.0
# -*- rpm-spec -*-

Name:           oxenstored
Version: 26.0.0
Release: 3%{?xsrel}%{?dist}
Summary:        oxenstored - OCaml Xenstore daemon
License:        LGPL-2.1-only WITH OCaml-LGPL-linking-exception
Source0: oxenstored-26.0.0.tar.gz

Patch1: configure-build.patch
Patch2: oxenstore-censor-sensitive-data.patch
Patch3: xsa483-xapi.patch

BuildRequires:  xs-opam-repo >= 6.77.0-1

BuildRequires:  ocaml
BuildRequires:  xen-devel
BuildRequires:  xen-dom0-libs-devel
# Locally, we use dune-built interface and plugin, but final builds
# use the plugin provided by xen
BuildRequires:  xen-dom0-tools
BuildRequires: xen-ocaml-libs

Provides: oxenstored
Obsoletes: xen-oxenstored < 5.0

%global ocaml_dir %{_opamroot}/ocaml-system
%global ocaml_libdir %{ocaml_dir}/lib

%description
OCaml Xenstore daemon

%prep
%autosetup -p1

%build
make

%install
rm -rf ./xsd_glue ./tests # we are taking the plugin built by upstream xen.spec instead, otherwise there are issues.
rm LICENSE README.md
export OCAMLPATH=%{_libdir}/ocaml
DESTDIR=%{buildroot} %{__make} install
%{__install} -D -m 0755 _build/install/default/sbin/oxenstored %{buildroot}%{_sbindir}/oxenstored

%check
make test

%files
%{_sbindir}/oxenstored
%exclude %{ocaml_dir}/sbin/oxenstored
%exclude %{ocaml_libdir}/oxenstored/xsdglue/*
%exclude %{ocaml_libdir}/oxenstored/META
%exclude %{ocaml_libdir}/oxenstored/dune-package
%exclude %{ocaml_libdir}/oxenstored/opam

%changelog
* Mon Apr 20 2026 Andrew Cooper <andrew.cooper3@citrix.com> - 26.0.0-3
- Fix for XSA-483 CVE-2026-23556

* Mon Mar 30 2026 Christian Lindig <christian.lindig@citrix.com> - 26.0.0-2
- meta: move comment to avoid ocamlformat from getting confused
- meta: reformat
- CP-311786 reformat *.ml files
- CP-311786 reformat *.c files
- CP-311786 xenmmap_stubs.c release OCaml global lock
- CP-311786 xenmmap_stubs.c use size_t/Long_val
- CP-311880 avoid naked pointer in eventchn_stubs.c
- CP-311880 don't use perror

* Fri Nov 07 2025 Steven Woods <steven.woods@citrix.com> - 25.3.0-1
- Fix path handling when loading the plugins

* Tue Nov 04 2025 Steven Woods <steven.woods@citrix.com> - 25.2.0-1
- oxenstored: Add 'depth' parameter handling for special watches
- oxenstored: Prepare xenstored.ml to be called in the unit tests
- tests: Test special watches with dying domains
- oxenstored: Fix releaseDomain events not being sent on domains shutting down
- oxenstored: Don't send multiple generic @releaseDomain events in a single update
- ocaml-evtchn: drop dependency on xenctrl, and use xenevtchn.h instead
- ocaml-evtchn: drop outdated -L

* Thu Oct 16 2025 Rob Hoes <rob.hoes@citrix.com> - 25.1.0-1
- Add missing dependencies
- Update to dune 3.20
- Avoid compiler warnings
- Revert "oxenstored: Add 'depth' parameter handling for special watches"

* Thu Oct 02 2025 Rob Hoes <rob.hoes@citrix.com> - 25.0.0-1
- oxenstored/connection: Remove unused module
- oxenstored/connection: Avoid double traversal over a hash table
- oxenstored/utils: Add optional 'unsigned' parameter to int_of_string_exn
- oxenstored: Add optional 'depth' parameter to watches
- oxenstored: Add 'depth' parameter handling for special watches

* Mon Mar 24 2025 Andrii Sultanov <andrii.sultanov@cloud.com> - 0.0.2
- Various optimizations speeding up oxenstored 4-5 times, improving scalability with
  the number of watches, simultaneous connections, and calls.
- Add unit tests
- Avoid double grant unmapping on domain cleanup
- Implement XS_DIRECTORY_PART call, dropping the non-standard "big packet" quirks

* Tue Oct 01 2024 Andrii Sultanov <andrii.sultanov@cloud.com> - 0.0.1-1
- First release
