```
$ brew leaves --installed-on-request | xargs -n1 brew desc --eval-all

awscli: Official Amazon AWS command-line interface
chezmoi: Manage your dotfiles across multiple diverse machines, securely
colima: Container runtimes on MacOS (and Linux) with minimal setup
direnv: Load/unload environment variables based on $PWD
Warning: Treating docker as a formula. For the cask, use homebrew/cask/docker
docker: Pack, ship and run any application as a lightweight container
fd: Simple, fast and user-friendly alternative to find
fzf: Command-line fuzzy finder written in Go
gh: GitHub command-line tool
jq: Lightweight and flexible command-line JSON processor
minikube: Run a Kubernetes cluster locally
mkcert: Simple tool to make locally trusted development certificates
neovim: Ambitious Vim-fork focused on extensibility and agility
nginx: HTTP(S) server and reverse proxy, and IMAP/POP3 proxy server
openjdk@17: Development kit for the Java programming language
pipenv: Python dependency management tool
podman-compose: Alternative to docker-compose using podman
pyenv: Python version management
ripgrep: Search tool like grep and The Silver Searcher
tmux: Terminal multiplexer
zsh-completions: Additional completion definitions for zsh
```

---

| Date | Package |
| - | - |
| Oct 26 | awscli |
| Sep 13 | ca-certificates |
| Sep 13 | capstone |
| Oct 26 | cffi |
| Nov 13 | chezmoi |
| Sep 13 | colima |
| Sep 15 | direnv |
| Sep 28 | docker |
| Sep 28 | docker-completion |
| Oct 26 | docutils |
| Sep 13 | dtc |
| Sep 13 | gettext |
| Sep 13 | gh |
| Sep 13 | glib |
| Sep 13 | gmp |
| Sep 13 | gnutls |
| Sep 13 | jpeg-turbo |
| Sep 13 | jq |
| Sep 13 | kubernetes-cli |
| Sep 13 | libevent |
| Sep 13 | libidn2 |
| Sep 13 | libnghttp2 |
| Sep 13 | libpng |
| Sep 13 | libslirp |
| Sep 13 | libssh |
| Sep 13 | libtasn1 |
| Sep 13 | libtermkey |
| Sep 13 | libunistring |
| Sep 13 | libusb |
| Sep 13 | libuv |
| Sep 13 | libvterm |
| Sep 13 | libyaml |
| Sep 13 | lima |
| Sep 13 | luajit |
| Sep 13 | luv |
| Sep 13 | lz4 |
| Sep 13 | lzo |
| Sep 13 | minikube |
| Oct 17 | mkcert |
| Sep 13 | mpdecimal |
| Sep 13 | msgpack |
| Sep 13 | ncurses |
| Sep 13 | neovim |
| Sep 13 | nettle |
| Oct 17 | nginx |
| Sep 13 | oniguruma |
| Oct 26 | openssl@3 |
| Sep 13 | p11-kit |
| Sep 13 | pcre2 |
| Oct 26 | pipenv |
| Sep 13 | pixman |
| Sep 13 | podman |
| Sep 13 | podman-compose |
| Oct 26 | pycparser |
| Oct 26 | python-certifi |
| Oct 26 | python-setuptools |
| Oct 26 | python@3.11 |
| Oct 26 | python@3.12 |
| Sep 13 | pyyaml |
| Sep 13 | qemu |
| Sep 13 | readline |
| Sep 20 | ripgrep |
| Sep 13 | six |
| Sep 13 | snappy |
| Oct 26 | sqlite |
| Sep 13 | tmux |
| Sep 13 | tree-sitter |
| Sep 13 | unbound |
| Sep 13 | unibilium |
| Sep 13 | utf8proc |
| Sep 13 | vde |
| Sep 13 | xz |
| Oct  5 | zsh-completions |
| Sep 13 | zstd |

| Date | Package |
| - | - |
| Sep 13 | amethyst |
| Nov  8 | chromium |
| Sep 13 | discord |
| Sep 13 | font-fira-code-nerd-font |
| Sep 13 | font-fira-mono-nerd-font |
| Sep 13 | intellij-idea |
| Sep 13 | iterm2 |
| Sep 13 | podman-desktop |
| Sep 13 | slack |
| Sep 13 | spotify |
| Sep 13 | visual-studio-code |
| Sep 13 | warp |
| Sep 13 | zoom |

---

```
$ brew deps --tree --installed

amethyst

autoconf
└── m4

awscli
├── cffi
│   ├── pycparser
│   └── python-setuptools
├── docutils
├── openssl@3
│   └── ca-certificates
├── pycparser
├── python@3.11
│   ├── mpdecimal
│   ├── openssl@3
│   │   └── ca-certificates
│   ├── sqlite
│   │   └── readline
│   └── xz
└── six

ca-certificates

cairo
├── fontconfig
│   └── freetype
│       └── libpng
├── freetype
│   └── libpng
├── glib
│   ├── pcre2
│   └── gettext
├── libpng
├── libx11
│   ├── libxcb
│   │   ├── libxau
│   │   │   └── xorgproto
│   │   └── libxdmcp
│   │       └── xorgproto
│   └── xorgproto
├── libxcb
│   ├── libxau
│   │   └── xorgproto
│   └── libxdmcp
│       └── xorgproto
├── libxext
│   ├── libx11
│   │   ├── libxcb
│   │   │   ├── libxau
│   │   │   │   └── xorgproto
│   │   │   └── libxdmcp
│   │   │       └── xorgproto
│   │   └── xorgproto
│   └── xorgproto
├── libxrender
│   ├── libx11
│   │   ├── libxcb
│   │   │   ├── libxau
│   │   │   │   └── xorgproto
│   │   │   └── libxdmcp
│   │   │       └── xorgproto
│   │   └── xorgproto
│   └── xorgproto
├── lzo
└── pixman

capstone

cffi
├── pycparser
└── python-setuptools

chezmoi

chromium

colima
└── lima
    └── qemu
        ├── capstone
        ├── dtc
        ├── glib
        │   ├── pcre2
        │   └── gettext
        ├── gnutls
        │   ├── ca-certificates
        │   ├── gmp
        │   ├── libidn2
        │   │   ├── libunistring
        │   │   └── gettext
        │   ├── libtasn1
        │   ├── libunistring
        │   ├── nettle
        │   │   └── gmp
        │   ├── p11-kit
        │   │   ├── ca-certificates
        │   │   └── libtasn1
        │   └── unbound
        │       ├── libevent
        │       │   └── openssl@3
        │       │       └── ca-certificates
        │       ├── libnghttp2
        │       └── openssl@3
        │           └── ca-certificates
        ├── jpeg-turbo
        ├── libpng
        ├── libslirp
        │   └── glib
        │       ├── pcre2
        │       └── gettext
        ├── libssh
        │   └── openssl@3
        │       └── ca-certificates
        ├── libusb
        ├── lzo
        ├── ncurses
        ├── nettle
        │   └── gmp
        ├── pixman
        ├── snappy
        ├── vde
        └── zstd
            ├── lz4
            └── xz

direnv

discord

docker
└── docker-completion

docker-completion

docutils

dtc

fd

font-fira-code-nerd-font

font-fira-mono-nerd-font

fontconfig
└── freetype
    └── libpng

freetype
└── libpng

fzf

gettext

gh

giflib

glib
├── pcre2
└── gettext

gmp

gnutls
├── ca-certificates
├── gmp
├── libidn2
│   ├── libunistring
│   └── gettext
├── libtasn1
├── libunistring
├── nettle
│   └── gmp
├── p11-kit
│   ├── ca-certificates
│   └── libtasn1
└── unbound
    ├── libevent
    │   └── openssl@3
    │       └── ca-certificates
    ├── libnghttp2
    └── openssl@3
        └── ca-certificates

graphite2

harfbuzz
├── cairo
│   ├── fontconfig
│   │   └── freetype
│   │       └── libpng
│   ├── freetype
│   │   └── libpng
│   ├── glib
│   │   ├── pcre2
│   │   └── gettext
│   ├── libpng
│   ├── libx11
│   │   ├── libxcb
│   │   │   ├── libxau
│   │   │   │   └── xorgproto
│   │   │   └── libxdmcp
│   │   │       └── xorgproto
│   │   └── xorgproto
│   ├── libxcb
│   │   ├── libxau
│   │   │   └── xorgproto
│   │   └── libxdmcp
│   │       └── xorgproto
│   ├── libxext
│   │   ├── libx11
│   │   │   ├── libxcb
│   │   │   │   ├── libxau
│   │   │   │   │   └── xorgproto
│   │   │   │   └── libxdmcp
│   │   │   │       └── xorgproto
│   │   │   └── xorgproto
│   │   └── xorgproto
│   ├── libxrender
│   │   ├── libx11
│   │   │   ├── libxcb
│   │   │   │   ├── libxau
│   │   │   │   │   └── xorgproto
│   │   │   │   └── libxdmcp
│   │   │   │       └── xorgproto
│   │   │   └── xorgproto
│   │   └── xorgproto
│   ├── lzo
│   └── pixman
├── freetype
│   └── libpng
├── glib
│   ├── pcre2
│   └── gettext
├── graphite2
└── icu4c

icu4c

intellij-idea

iterm2

jpeg-turbo

jq
└── oniguruma

kubernetes-cli

libevent
└── openssl@3
    └── ca-certificates

libidn2
├── libunistring
└── gettext

libnghttp2

libpng

libslirp
└── glib
    ├── pcre2
    └── gettext

libssh
└── openssl@3
    └── ca-certificates

libtasn1

libtermkey
└── unibilium

libtiff
├── jpeg-turbo
├── xz
└── zstd
    ├── lz4
    └── xz

libunistring

libusb

libuv

libvterm

libx11
├── libxcb
│   ├── libxau
│   │   └── xorgproto
│   └── libxdmcp
│       └── xorgproto
└── xorgproto

libxau
└── xorgproto

libxcb
├── libxau
│   └── xorgproto
└── libxdmcp
    └── xorgproto

libxdmcp
└── xorgproto

libxext
├── libx11
│   ├── libxcb
│   │   ├── libxau
│   │   │   └── xorgproto
│   │   └── libxdmcp
│   │       └── xorgproto
│   └── xorgproto
└── xorgproto

libxrender
├── libx11
│   ├── libxcb
│   │   ├── libxau
│   │   │   └── xorgproto
│   │   └── libxdmcp
│   │       └── xorgproto
│   └── xorgproto
└── xorgproto

libyaml

lima
└── qemu
    ├── capstone
    ├── dtc
    ├── glib
    │   ├── pcre2
    │   └── gettext
    ├── gnutls
    │   ├── ca-certificates
    │   ├── gmp
    │   ├── libidn2
    │   │   ├── libunistring
    │   │   └── gettext
    │   ├── libtasn1
    │   ├── libunistring
    │   ├── nettle
    │   │   └── gmp
    │   ├── p11-kit
    │   │   ├── ca-certificates
    │   │   └── libtasn1
    │   └── unbound
    │       ├── libevent
    │       │   └── openssl@3
    │       │       └── ca-certificates
    │       ├── libnghttp2
    │       └── openssl@3
    │           └── ca-certificates
    ├── jpeg-turbo
    ├── libpng
    ├── libslirp
    │   └── glib
    │       ├── pcre2
    │       └── gettext
    ├── libssh
    │   └── openssl@3
    │       └── ca-certificates
    ├── libusb
    ├── lzo
    ├── ncurses
    ├── nettle
    │   └── gmp
    ├── pixman
    ├── snappy
    ├── vde
    └── zstd
        ├── lz4
        └── xz

little-cms2
├── jpeg-turbo
└── libtiff
    ├── jpeg-turbo
    ├── xz
    └── zstd
        ├── lz4
        └── xz

luajit

luv
└── libuv

lz4

lzo

m4

minikube
└── kubernetes-cli

mkcert

mpdecimal

msgpack

ncurses

neovim
├── gettext
├── libtermkey
│   └── unibilium
├── libuv
├── libvterm
├── luajit
├── luv
│   └── libuv
├── msgpack
├── tree-sitter
└── unibilium

nettle
└── gmp

nginx
├── openssl@3
│   └── ca-certificates
└── pcre2

oniguruma

openjdk@17
├── giflib
├── harfbuzz
│   ├── cairo
│   │   ├── fontconfig
│   │   │   └── freetype
│   │   │       └── libpng
│   │   ├── freetype
│   │   │   └── libpng
│   │   ├── glib
│   │   │   ├── pcre2
│   │   │   └── gettext
│   │   ├── libpng
│   │   ├── libx11
│   │   │   ├── libxcb
│   │   │   │   ├── libxau
│   │   │   │   │   └── xorgproto
│   │   │   │   └── libxdmcp
│   │   │   │       └── xorgproto
│   │   │   └── xorgproto
│   │   ├── libxcb
│   │   │   ├── libxau
│   │   │   │   └── xorgproto
│   │   │   └── libxdmcp
│   │   │       └── xorgproto
│   │   ├── libxext
│   │   │   ├── libx11
│   │   │   │   ├── libxcb
│   │   │   │   │   ├── libxau
│   │   │   │   │   │   └── xorgproto
│   │   │   │   │   └── libxdmcp
│   │   │   │   │       └── xorgproto
│   │   │   │   └── xorgproto
│   │   │   └── xorgproto
│   │   ├── libxrender
│   │   │   ├── libx11
│   │   │   │   ├── libxcb
│   │   │   │   │   ├── libxau
│   │   │   │   │   │   └── xorgproto
│   │   │   │   │   └── libxdmcp
│   │   │   │   │       └── xorgproto
│   │   │   │   └── xorgproto
│   │   │   └── xorgproto
│   │   ├── lzo
│   │   └── pixman
│   ├── freetype
│   │   └── libpng
│   ├── glib
│   │   ├── pcre2
│   │   └── gettext
│   ├── graphite2
│   └── icu4c
├── jpeg-turbo
├── libpng
└── little-cms2
    ├── jpeg-turbo
    └── libtiff
        ├── jpeg-turbo
        ├── xz
        └── zstd
            ├── lz4
            └── xz

openssl@3
└── ca-certificates

p11-kit
├── ca-certificates
└── libtasn1

pcre2

pipenv
├── python-certifi
│   └── ca-certificates
├── python@3.12
│   ├── mpdecimal
│   ├── openssl@3
│   │   └── ca-certificates
│   ├── sqlite
│   │   └── readline
│   └── xz
└── virtualenv
    ├── python-distlib
    ├── python-filelock
    ├── python-platformdirs
    └── python@3.12
        ├── mpdecimal
        ├── openssl@3
        │   └── ca-certificates
        ├── sqlite
        │   └── readline
        └── xz

pixman

pkg-config

podman
└── qemu
    ├── capstone
    ├── dtc
    ├── glib
    │   ├── pcre2
    │   └── gettext
    ├── gnutls
    │   ├── ca-certificates
    │   ├── gmp
    │   ├── libidn2
    │   │   ├── libunistring
    │   │   └── gettext
    │   ├── libtasn1
    │   ├── libunistring
    │   ├── nettle
    │   │   └── gmp
    │   ├── p11-kit
    │   │   ├── ca-certificates
    │   │   └── libtasn1
    │   └── unbound
    │       ├── libevent
    │       │   └── openssl@3
    │       │       └── ca-certificates
    │       ├── libnghttp2
    │       └── openssl@3
    │           └── ca-certificates
    ├── jpeg-turbo
    ├── libpng
    ├── libslirp
    │   └── glib
    │       ├── pcre2
    │       └── gettext
    ├── libssh
    │   └── openssl@3
    │       └── ca-certificates
    ├── libusb
    ├── lzo
    ├── ncurses
    ├── nettle
    │   └── gmp
    ├── pixman
    ├── snappy
    ├── vde
    └── zstd
        ├── lz4
        └── xz

podman-compose
├── podman
│   └── qemu
│       ├── capstone
│       ├── dtc
│       ├── glib
│       │   ├── pcre2
│       │   └── gettext
│       ├── gnutls
│       │   ├── ca-certificates
│       │   ├── gmp
│       │   ├── libidn2
│       │   │   ├── libunistring
│       │   │   └── gettext
│       │   ├── libtasn1
│       │   ├── libunistring
│       │   ├── nettle
│       │   │   └── gmp
│       │   ├── p11-kit
│       │   │   ├── ca-certificates
│       │   │   └── libtasn1
│       │   └── unbound
│       │       ├── libevent
│       │       │   └── openssl@3
│       │       │       └── ca-certificates
│       │       ├── libnghttp2
│       │       └── openssl@3
│       │           └── ca-certificates
│       ├── jpeg-turbo
│       ├── libpng
│       ├── libslirp
│       │   └── glib
│       │       ├── pcre2
│       │       └── gettext
│       ├── libssh
│       │   └── openssl@3
│       │       └── ca-certificates
│       ├── libusb
│       ├── lzo
│       ├── ncurses
│       ├── nettle
│       │   └── gmp
│       ├── pixman
│       ├── snappy
│       ├── vde
│       └── zstd
│           ├── lz4
│           └── xz
├── python@3.12
│   ├── mpdecimal
│   ├── openssl@3
│   │   └── ca-certificates
│   ├── sqlite
│   │   └── readline
│   └── xz
└── pyyaml
    └── libyaml

podman-desktop
└── podman
    └── qemu
        ├── capstone
        ├── dtc
        ├── glib
        │   ├── pcre2
        │   └── gettext
        ├── gnutls
        │   ├── ca-certificates
        │   ├── gmp
        │   ├── libidn2
        │   │   ├── libunistring
        │   │   └── gettext
        │   ├── libtasn1
        │   ├── libunistring
        │   ├── nettle
        │   │   └── gmp
        │   ├── p11-kit
        │   │   ├── ca-certificates
        │   │   └── libtasn1
        │   └── unbound
        │       ├── libevent
        │       │   └── openssl@3
        │       │       └── ca-certificates
        │       ├── libnghttp2
        │       └── openssl@3
        │           └── ca-certificates
        ├── jpeg-turbo
        ├── libpng
        ├── libslirp
        │   └── glib
        │       ├── pcre2
        │       └── gettext
        ├── libssh
        │   └── openssl@3
        │       └── ca-certificates
        ├── libusb
        ├── lzo
        ├── ncurses
        ├── nettle
        │   └── gmp
        ├── pixman
        ├── snappy
        ├── vde
        └── zstd
            ├── lz4
            └── xz

pycparser

pyenv
├── autoconf
│   └── m4
├── openssl@3
│   └── ca-certificates
├── pkg-config
└── readline

python-certifi
└── ca-certificates

python-setuptools

python@3.11
├── mpdecimal
├── openssl@3
│   └── ca-certificates
├── sqlite
│   └── readline
└── xz

python@3.12
├── mpdecimal
├── openssl@3
│   └── ca-certificates
├── sqlite
│   └── readline
└── xz

pyyaml
└── libyaml

qemu
├── capstone
├── dtc
├── glib
│   ├── pcre2
│   └── gettext
├── gnutls
│   ├── ca-certificates
│   ├── gmp
│   ├── libidn2
│   │   ├── libunistring
│   │   └── gettext
│   ├── libtasn1
│   ├── libunistring
│   ├── nettle
│   │   └── gmp
│   ├── p11-kit
│   │   ├── ca-certificates
│   │   └── libtasn1
│   └── unbound
│       ├── libevent
│       │   └── openssl@3
│       │       └── ca-certificates
│       ├── libnghttp2
│       └── openssl@3
│           └── ca-certificates
├── jpeg-turbo
├── libpng
├── libslirp
│   └── glib
│       ├── pcre2
│       └── gettext
├── libssh
│   └── openssl@3
│       └── ca-certificates
├── libusb
├── lzo
├── ncurses
├── nettle
│   └── gmp
├── pixman
├── snappy
├── vde
└── zstd
    ├── lz4
    └── xz

readline

ripgrep
└── pcre2

six

slack

snappy

spotify

sqlite
└── readline

tmux
├── libevent
│   └── openssl@3
│       └── ca-certificates
├── ncurses
└── utf8proc

tree-sitter

unbound
├── libevent
│   └── openssl@3
│       └── ca-certificates
├── libnghttp2
└── openssl@3
    └── ca-certificates

unibilium

utf8proc

vde

visual-studio-code

warp

xorgproto

xz

zoom

zsh-completions

zstd
├── lz4
└── xz
```
