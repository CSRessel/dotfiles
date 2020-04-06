# Newer brew-installed ruby:
#export PATH="/usr/local/opt/ruby/bin:$PATH"
# (version 2.6.3 vs system 2.3.7)

export PS1="\u@\[$(tput sgr0)\]\[\033[38;5;10m\]\h\[$(tput sgr0)\]\[\033[38;5;15m\]:\[$(tput sgr0)\]\[\033[38;5;14m\]\W\[$(tput sgr0)\]\[\033[38;5;15m\] \\$ \[$(tput sgr0)\]"

# default to tmux sessions
#if [[ ! $TERM =~ screen ]]; then
#	exec tmux
#fi

alias kc=kubectl

#-------------------------------- porter
export PATH=$PATH:~/.porter

#-------------------------------- thefuck
# git tab complete
[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion || {
    # if not found in /usr/local/etc, try the brew --prefix location
    [ -f "$(brew --prefix)/etc/bash_completion.d/git-completion.bash" ] && \
        . $(brew --prefix)/etc/bash_completion.d/git-completion.bash
}

#-------------------------------- thefuck
eval $(thefuck --alias)
# You can use whatever you want as an alias, like for Mondays:
#eval $(thefuck --alias FUCK)
eval $(thefuck --alias asdf)

#-------------------------------- pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi

#-------------------------------- direnv
eval "$(direnv hook bash)"

