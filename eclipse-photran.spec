%define gcj_support             0
%define major                   4
%define minor                   0  
%define patch                   0
%define majmin                  %{major}.%{minor}
%define eclipse_base            %{_libdir}/eclipse

Summary:        Eclipse Fortran Development Tools (Photran) plugin
Name:           eclipse-photran
Version:        %{majmin}.%{patch}
Release:        %mkrel 4.b4.3.1
License:        EPL
Group:          Development/Other
URL:            http://www.eclipse.org/photran
Requires:       eclipse-platform

# The following tarball was generated by the makesource.sh script
Source0: org.eclipse.photran-v20080808_4_0_0_Beta4.tar.gz
Source1: makesource.sh
BuildRequires: eclipse-pde
BuildRequires: eclipse-cdt >= 4.0.1
BuildRequires: tomcat5-jsp-2.0-api
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 1.0.64
%endif

BuildRequires:  java-rpmbuild
BuildRequires:  zip
Requires:       gdb make gcc-gfortran
Requires:       eclipse-platform >= 1:3.3.0

# Currently, upstream CDT only supports building on the platforms listed here.
ExclusiveArch: %{ix86} x86_64 ppc ia64
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root


%description
The eclipse-photran package contains the Photran Eclipse feature and plugins
that are useful for Fortran development.

%package        xlf
Summary:        IBM XL Fortran compiler support for Photran
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    xlf
%{summary}.

%prep
%setup -q -n org.eclipse.photran-v20080808_4_0_0_Beta4
# Fixup to use 1.5 source level
find -name \*.prefs | xargs sed -i -e 's/source=1.3/source=1.5/'


%build
export JAVA_HOME=%{java_home}
export PATH=%{java_bin}:/usr/bin:$PATH
for feature in org.eclipse.photran_feature org.eclipse.photran.intel org.eclipse.photran.vpg_feature \
               org.eclipse.photran.xlf_feature
do
  %{eclipse_base}/buildscripts/pdebuild -D -d cdt \
    -f $feature -a "-DjavacSource=1.5 -DjavacTarget=1.5"
done

%install
rm -rf ${RPM_BUILD_ROOT}

for feature in photran photran.vpg photran.xlf
do
  install -d -m755 ${RPM_BUILD_ROOT}%{eclipse_base}/dropins/${feature}
  
  unzip -o -d ${RPM_BUILD_ROOT}%{eclipse_base}/dropins/${feature} \
              build/rpmBuild/org.eclipse.${feature}_feature.zip
  mv ${RPM_BUILD_ROOT}%{eclipse_base}/dropins/${feature}/eclipse/* \
     ${RPM_BUILD_ROOT}%{eclipse_base}/dropins/${feature}
  rmdir ${RPM_BUILD_ROOT}%{eclipse_base}/dropins/${feature}/eclipse
done

%{gcj_compile}

%clean 
rm -rf ${RPM_BUILD_ROOT}


%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif


%files
%defattr(-,root,root,-)
%doc org.eclipse.photran-feature/epl-v10.html
%{eclipse_base}/dropins/photran
%{eclipse_base}/dropins/photran.vpg
%{gcj_files}

%files xlf
%defattr(-,root,root,-)
%{eclipse_base}/dropins/photran.xlf


