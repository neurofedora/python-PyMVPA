%global origname PyMVPA
%global modname mvpa2

Name:           python-%{origname}
Version:        2.4.0
Release:        3%{?dist}
Summary:        Multivariate pattern analysis

License:        MIT
URL:            http://www.pymvpa.org/
Source0:        https://github.com/PyMVPA/PyMVPA/archive/upstream/%{version}/%{origname}-%{version}.tar.gz
Patch0:         PyMVPA-force-system-libsvm.patch
BuildRequires:  git-core
BuildRequires:  libsvm-devel swig
# matplotlib requires $DISPLAY
BuildRequires:  /usr/bin/xvfb-run

%description
PyMVPA is a Python package intended to ease statistical learning analyses of
large datasets. It offers an extensible framework with a high-level interface
to a broad range of algorithms for classification, regression, feature
selection, data import and export. It is designed to integrate well with
related software packages, such as scikit-learn, shogun, MDP, etc. While it is
not limited to the neuroimaging domain, it is eminently suited for such
datasets. PyMVPA is free software and requires nothing but free-software to
run.

PyMVPA stands for MultiVariate Pattern Analysis (MVPA) in Python.

%package -n python2-%{origname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{origname}}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  numpy
# Test deps
BuildRequires:  python2-nose
BuildRequires:  scipy python2-nibabel
BuildRequires:  python-lxml h5py python-statsmodels python-shogun
BuildRequires:  python2-nipy lapack-devel
BuildRequires:  python2-pywt
Requires:       numpy
# Strongly
Recommends:     scipy python2-nibabel
# Suggestions
Recommends:     python-scikit-learn
Recommends:     python-matplotlib
Recommends:     python-reportlab
Recommends:     h5py
Recommends:     python-statsmodels
Recommends:     libsvm-python
Recommends:     python-lxml
Recommends:     python-shogun
Recommends:     lapack-devel
Recommends:     python2-pywt
Suggests:       ipython

%description -n python2-%{origname}
PyMVPA is a Python package intended to ease statistical learning analyses of
large datasets. It offers an extensible framework with a high-level interface
to a broad range of algorithms for classification, regression, feature
selection, data import and export. It is designed to integrate well with
related software packages, such as scikit-learn, shogun, MDP, etc. While it is
not limited to the neuroimaging domain, it is eminently suited for such
datasets. PyMVPA is free software and requires nothing but free-software to
run.

PyMVPA stands for MultiVariate Pattern Analysis (MVPA) in Python.

Python 2 version.

%package -n python3-%{origname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{origname}}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
# Test deps
BuildRequires:  python3-nose
BuildRequires:  python3-scipy python3-nibabel
BuildRequires:  python3-lxml python3-h5py python3-statsmodels python3-shogun
BuildRequires:  python3-nipy
BuildRequires:  python3-pywt
Requires:       python3-numpy
# Strongly
Recommends:     python3-scipy python3-nibabel
# Suggestions
Recommends:     python3-scikit-learn
Recommends:     python3-matplotlib
Recommends:     python3-reportlab
Recommends:     python3-h5py
Recommends:     python3-statsmodels
# TODO: add python3 subpackage
#Recommends:     libsvm-python
Recommends:     python3-lxml
Recommends:     python3-shogun
Recommends:     lapack-devel
Recommends:     python3-pywt
Suggests:       python3-ipython

%description -n python3-%{origname}
PyMVPA is a Python package intended to ease statistical learning analyses of
large datasets. It offers an extensible framework with a high-level interface
to a broad range of algorithms for classification, regression, feature
selection, data import and export. It is designed to integrate well with
related software packages, such as scikit-learn, shogun, MDP, etc. While it is
not limited to the neuroimaging domain, it is eminently suited for such
datasets. PyMVPA is free software and requires nothing but free-software to
run.

PyMVPA stands for MultiVariate Pattern Analysis (MVPA) in Python.

Python 3 version.

%prep
%autosetup -n %{origname}-upstream-%{version} -S git
# Remove bundled libraries
rm -rf 3rd/

%build
%py2_build
%py3_build

%install
%py3_install
%py2_install

# Rename binaries
pushd %{buildroot}%{_bindir}
  for mod in pymvpa2 pymvpa2-prep-afni-surf pymvpa2-prep-fmri pymvpa2-tutorial
  do
    mv $mod python3-$mod

    sed -i '1s|^.*$|#!/usr/bin/env %{__python3}|' python3-$mod
    for i in $mod $mod-3 $mod-%{python3_version}
    do
      ln -s python3-$mod $i
    done

    cp python3-$mod python2-$mod
    sed -i '1s|^.*$|#!/usr/bin/env %{__python2}|' python2-$mod

    for i in $mod-2 $mod-%{python2_version}
    do
      ln -s python2-$mod $i
    done
  done
popd

%check
# Many tests fails, because of extensions wasn't built inplace
# and other stuff. We will fix them eventually.
xvfb-run nosetests-%{python2_version} -v || :
xvfb-run nosetests-%{python3_version} -v || :

%files -n python2-%{origname}
%license COPYING
%doc doc/examples README.rst AUTHOR
%{_bindir}/pymvpa2-2
%{_bindir}/pymvpa2-%{python2_version}
%{_bindir}/python2-pymvpa2
%{_bindir}/pymvpa2-prep-afni-surf-2
%{_bindir}/pymvpa2-prep-afni-surf-%{python2_version}
%{_bindir}/python2-pymvpa2-prep-afni-surf
%{_bindir}/pymvpa2-prep-fmri-2
%{_bindir}/pymvpa2-prep-fmri-%{python2_version}
%{_bindir}/python2-pymvpa2-prep-fmri
%{_bindir}/pymvpa2-tutorial-2
%{_bindir}/pymvpa2-tutorial-%{python2_version}
%{_bindir}/python2-pymvpa2-tutorial
%{python2_sitearch}/%{modname}/
%{python2_sitearch}/py%{modname}*-egginfo

%files -n python3-%{origname}
%license COPYING
%doc doc/examples
%{_bindir}/pymvpa2
%{_bindir}/pymvpa2-3
%{_bindir}/pymvpa2-%{python3_version}
%{_bindir}/python3-pymvpa2
%{_bindir}/pymvpa2-prep-afni-surf
%{_bindir}/pymvpa2-prep-afni-surf-3
%{_bindir}/pymvpa2-prep-afni-surf-%{python3_version}
%{_bindir}/python3-pymvpa2-prep-afni-surf
%{_bindir}/pymvpa2-prep-fmri
%{_bindir}/pymvpa2-prep-fmri-3
%{_bindir}/pymvpa2-prep-fmri-%{python3_version}
%{_bindir}/python3-pymvpa2-prep-fmri
%{_bindir}/pymvpa2-tutorial
%{_bindir}/pymvpa2-tutorial-3
%{_bindir}/pymvpa2-tutorial-%{python3_version}
%{_bindir}/python3-pymvpa2-tutorial
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/py%{modname}*-egginfo

%changelog
* Wed Nov 11 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.0-3
- Binary without prefix uses py3
- Fix typo in build
- Provide python?-mvpa2 also

* Fri Nov 06 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.0-2
- Add pywt to Recommends/BuildRequires

* Sun Nov 01 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.0-1
- Initial package
