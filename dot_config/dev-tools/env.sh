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

dev_tools_prepend "$HOME/.local/bin"
dev_tools_prepend "${MISE_DATA_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/mise}/shims"
unset -f dev_tools_prepend
