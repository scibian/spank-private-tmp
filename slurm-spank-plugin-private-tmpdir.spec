%define __find_requires %{_builddir}/find-requires
%define __plugin private-tmpdir
%define __lib_dir %{_prefix}/lib
%define debug_package %{nil}

Summary: Slurm SPANK plugin for job private tmpdir
Name: slurm-spank-plugin-private-tmpdir
Version: 0.1.1
Release: 3%{?dist}.edf
License: GPL
Group: System Environment/Base
URL: https://github.com/scibian/spank-private-tmp
Source0: %{name}-%{version}.tar.gz
Patch0:  Implement-subdir-feature.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: slurm-devel >= 23, slurm-devel < 24, git
Requires: slurm >= 23, slurm < 24

%description
Slurm SPANK plugin that uses file system namespaces to create private
temporary directories for each job.

%prep
%setup -q
%patch0 -p1
# Dummy file used to get a RPM dependency on libslurm.so
echo 'int main(){}' > %{_builddir}/libslurm_dummy.c
cat <<EOF > %{_builddir}/find-requires
#!/bin/sh
# Add dummy to list of files sent to the regular find-requires
{ echo %{_builddir}/libslurm_dummy; cat; } | \
    /usr/lib/rpm/redhat/find-requires
EOF
chmod +x %{_builddir}/find-requires

%build
make all
#gcc -g -std=gnu99 -Wall -o %{__plugin}.o -fPIC -c %{__plugin}.c
#gcc -g -shared -o %{__plugin}.so %{__plugin}.o
gcc -g -lslurm -o %{_builddir}/libslurm_dummy %{_builddir}/libslurm_dummy.c

%install
install -d %{buildroot}%{__lib_dir}/slurm
#install -d %{buildroot}%{_sysconfdir}/slurm/plugstack.conf.d
install -m 755 %{__plugin}.so %{buildroot}%{__lib_dir}/slurm/
#install -m 644 plugstack.conf \
#    %{buildroot}%{_sysconfdir}/slurm/plugstack.conf.d/%{__plugin}.conf

%clean
rm -rf %{buildroot}

%files
%doc README LICENSE
%defattr(-,root,root,-)
%{__lib_dir}/slurm/%{__plugin}.so
#%config %{_sysconfdir}/slurm/plugstack.conf.d/%{__plugin}.conf

%changelog
* Wed Nov 15 2023 Mathieu Chouquet-Stringer <mathieu-externe.chouquet-stringer> - 0.1.1-3.edf
- Rebuild for slurm 23.02
* Mon Nov 02 2020 Thomas HAMEL <thomas-t.hamel@edf.fr> - 0.1.1-2.edf
- Rebuild for slurm 20.02
* Fri Jan 10 2020 Kwame Amedodji <kamedodji@yahoo.fr> - 0.1.1-1
- make plugin more generic / change some paths
* Thu Feb 02 2017 Pär Lindfors <paran@nsc.liu.se> - 0.0.2-1
- Support multiple base parameters
* Mon Feb 16 2015 Pär Lindfors <paran@nsc.liu.se> - 0.0.1-1
- Initial RPM packaging
