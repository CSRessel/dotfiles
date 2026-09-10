# Shared by interactive shells and explicitly sourced by noninteractive jobs.
# Add each path once; preserve a Nix shell's existing PATH precedence.
dev_tools_prepend() {
    case ":$PATH:" in
        *":$1:"*) ;;
        *)
            if [ -n "${IN_NIX_SHELL:-}" ]; then
                PATH="$PATH:$1"
            else
                PATH="$1:$PATH"
            fi
            ;;
    esac
    export PATH
}

dev_tools_prepend "${CARGO_HOME:-$HOME/.cargo}/bin"
# Bun global applications use this directory; mise shims precede an old Bun binary.
dev_tools_prepend "${BUN_INSTALL:-$HOME/.bun}/bin"
dev_tools_prepend "$HOME/.local/bin"
dev_tools_prepend "${MISE_DATA_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/mise}/shims"
unset -f dev_tools_prepend

# Respect an explicit wrapper, including an explicitly empty opt-out.
if [ "${RUSTC_WRAPPER+x}" != x ] && [ -z "${IN_NIX_SHELL:-}" ] && command -v sccache >/dev/null 2>&1; then
    export RUSTC_WRAPPER=sccache
fi
if [ "$(uname -s)" = Linux ] && [ -n "${CODEX_THREAD_ID:-}" ] && [ "${SCCACHE_SERVER_UDS+x}" != x ]; then
    export SCCACHE_SERVER_UDS="/tmp/sccache-${CODEX_THREAD_ID}.sock"
fi
