#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Full standard library replacement for OCaml
Summary(pl.UTF-8):	Pełny zamiennik biblioteki standardowej dla OCamla
Name:		ocaml-base
Version:	0.14.2
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/janestreet/base/releases
Source0:	https://github.com/janestreet/base/archive/v%{version}/base-%{version}.tar.gz
# Source0-md5:	0d1a2d0322b8c446e5dda20290112e5c
URL:		https://opensource.janestreet.com/base/
BuildRequires:	ocaml >= 1:4.07.0
BuildRequires:	ocaml-dune-devel >= 2.0.0
BuildRequires:	ocaml-sexplib0-devel >= 0.14
BuildRequires:	ocaml-sexplib0-devel < 0.15
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
Base is a complete and portable alternative to the OCaml standard
library. It provides all standard functionalities one would expect
from a language standard library. It uses consistent conventions
across all of its module.

Base aims to be usable in any context. As a result system dependent
features such as I/O are not offered by Base. They are instead
provided by companion libraries such as stdio.

This package contains files needed to run bytecode executables using
base library.

%description -l pl.UTF-8
Base to kompletna i przenośna alternatywa dla biblioteki standardowej
OCamla. Zapewnia całą standardową funkcjonalność, której należałoby
oczekiwać od biblioteki standardowej języka programowania.
Wykorzystuje spójne konwencje w całym module.

Biblioteka base ma być użyteczna w dowolnym kontekście - w efekcie
funkcje zależne od systemu, takie jak wejście/wyjście, nie są w niej
oferowane - są udostępniane przez biblioteki towarzyszące, takie jak
stdio.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki base.

%package devel
Summary:	Full standard library replacement for OCaml - development part
Summary(pl.UTF-8):	Pełny zamiennik biblioteki standardowej dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-dune-devel >= 2.0.0
Requires:	ocaml-sexplib0-devel >= 0.14
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
base library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki base.

%prep
%setup -q -n base-%{version}

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/base/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/base/*/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/base/base_internalhash_types/*.h
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/base

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.org ROADMAP.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllbase_stubs.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllbase_internalhash_types_stubs.so
%dir %{_libdir}/ocaml/base
%{_libdir}/ocaml/base/META
%{_libdir}/ocaml/base/*.cma
%{_libdir}/ocaml/base/runtime.js
%dir %{_libdir}/ocaml/base/base_internalhash_types
%{_libdir}/ocaml/base/base_internalhash_types/*.cma
%{_libdir}/ocaml/base/base_internalhash_types/runtime.js
%dir %{_libdir}/ocaml/base/caml
%{_libdir}/ocaml/base/caml/*.cma
%dir %{_libdir}/ocaml/base/md5
%{_libdir}/ocaml/base/md5/*.cma
%dir %{_libdir}/ocaml/base/shadow_stdlib
%{_libdir}/ocaml/base/shadow_stdlib/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/base/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/base/base_internalhash_types/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/base/caml/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/base/md5/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/base/shadow_stdlib/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/base/libbase_stubs.a
%{_libdir}/ocaml/base/*.cmi
%{_libdir}/ocaml/base/*.cmt
%{_libdir}/ocaml/base/*.cmti
%{_libdir}/ocaml/base/*.mli
%{_libdir}/ocaml/base/base_internalhash_types/libbase_internalhash_types_stubs.a
%{_libdir}/ocaml/base/base_internalhash_types/*.cmi
%{_libdir}/ocaml/base/base_internalhash_types/*.cmt
%{_libdir}/ocaml/base/caml/*.cmi
%{_libdir}/ocaml/base/caml/*.cmt
%{_libdir}/ocaml/base/md5/*.cmi
%{_libdir}/ocaml/base/md5/*.cmt
%{_libdir}/ocaml/base/md5/*.cmti
%{_libdir}/ocaml/base/md5/*.mli
%{_libdir}/ocaml/base/shadow_stdlib/*.cmi
%{_libdir}/ocaml/base/shadow_stdlib/*.cmt
%{_libdir}/ocaml/base/shadow_stdlib/*.cmti
%{_libdir}/ocaml/base/shadow_stdlib/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/base/base.a
%{_libdir}/ocaml/base/*.cmx
%{_libdir}/ocaml/base/*.cmxa
%{_libdir}/ocaml/base/base_internalhash_types/base_internalhash_types.a
%{_libdir}/ocaml/base/base_internalhash_types/*.cmx
%{_libdir}/ocaml/base/base_internalhash_types/*.cmxa
%{_libdir}/ocaml/base/caml/caml.a
%{_libdir}/ocaml/base/caml/*.cmx
%{_libdir}/ocaml/base/caml/*.cmxa
%{_libdir}/ocaml/base/md5/md5_lib.a
%{_libdir}/ocaml/base/md5/*.cmx
%{_libdir}/ocaml/base/md5/*.cmxa
%{_libdir}/ocaml/base/shadow_stdlib/shadow_stdlib.a
%{_libdir}/ocaml/base/shadow_stdlib/*.cmx
%{_libdir}/ocaml/base/shadow_stdlib/*.cmxa
%endif
%{_libdir}/ocaml/base/dune-package
%{_libdir}/ocaml/base/opam
