%define		crates_ver	0.8.3

Summary:	A smarter cd command
Name:		zoxide
Version:	0.8.3
Release:	1
License:	MIT
Group:		Applications
Source0:	https://github.com/ajeetdsouza/zoxide/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	43d35848583bba42752af70bbf9d189d
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	79b0c1f6d1e35b6ad0ee7d26799d539a
URL:		https://github.com/ajeetdsouza/zoxide
BuildRequires:	cargo
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Suggests:	fzf
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
zoxide is a blazing fast replacement for your cd command, inspired by
z and z.lua. It keeps track of the directories you use most
frequently, and uses a ranking algorithm to navigate to the best
match.

%package -n bash-completion-zoxide
Summary:	bash-completion for zoxide
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-zoxide
This package provides bash-completion for zoxide.

%package -n fish-completion-zoxide
Summary:	Fish completion for zoxide command
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-zoxide
Fish completion for zoxide command.

%package -n zsh-completion-zoxide
Summary:	Zsh completion for zoxide command
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-zoxide
Zsh completion for zoxide command.

%prep
%setup -q -a1

%{__mv} zoxide-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man1
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

install -Dp contrib/completions/zoxide.bash $RPM_BUILD_ROOT%{bash_compdir}/zoxide
install -Dp contrib/completions/zoxide.fish $RPM_BUILD_ROOT%{fish_compdir}/zoxide.fish
install -Dp contrib/completions/_zoxide $RPM_BUILD_ROOT%{zsh_compdir}/_zoxide

cp -p man/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/zoxide
%{_mandir}/man1/zoxide.1*
%{_mandir}/man1/zoxide-add.1*
%{_mandir}/man1/zoxide-import.1*
%{_mandir}/man1/zoxide-init.1*
%{_mandir}/man1/zoxide-query.1*
%{_mandir}/man1/zoxide-remove.1*

%files -n bash-completion-zoxide
%defattr(644,root,root,755)
%{bash_compdir}/zoxide

%files -n fish-completion-%{name}
%defattr(644,root,root,755)
%{fish_compdir}/zoxide.fish

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_zoxide
