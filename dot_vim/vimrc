" github.com/CSRessel/dotvim
" vimrc
" Created 6/16/13
"---------------------------------------------------------------

" Preamble and vim-plug ----------------------------------------{{{

" Automatically reload vimrc when it's saved
autocmd BufWritePost .vimrc so ~/.vimrc

set nocompatible              " be iMproved, required
filetype off                  " required

if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" Specify a directory for plugins
" - Avoid using standard Vim directory names like 'plugin'
call plug#begin('~/.vim/plugged')

" Make sure you use single quotes

Plug 'altercation/vim-colors-solarized'
Plug 'bronson/vim-trailing-whitespace'
Plug 'christoomey/vim-tmux-navigator'
Plug 'kien/ctrlp.vim'
Plug 'scrooloose/nerdtree'
Plug 'Townk/vim-autoclose'
Plug 'tpope/vim-fugitive'
Plug 'vim-airline/vim-airline'
Plug 'vim-syntastic/syntastic'
Plug 'VundleVim/Vundle.vim'

" Initialize plugin system
call plug#end()

" }}}

" Options ------------------------------------------------------{{{

" Mouse isn't ALL bad
set mouse=a
" Search as you type
set incsearch
" highlight search matches
set hlsearch
" Ignore case if all lowercase, case sensitive otherwise
set smartcase
" Remove annoying errors
set t_vb=
set tm=500
" Tabs w/ tab char equiv to four spaces
set tabstop=4
set shiftwidth=4
" Plenty of history
set history=1000
" Lots of undo levels
set undolevels=1000
" Have vim as title in a shell
set title
" Have backspace act as it should
set backspace=eol,start,indent
" Add chars for unwrapped lines
set listchars=extends:❯,precedes:❮
" Fold text between {{{ and }}} (in comments)
set foldmethod=marker
" Show matching brackets when text indicator is over them
set showmatch
" How many tenths of a second to blink when matching brackets
set mat=2
" Set utf8 as standard encoding and en_US as the standard language
set encoding=utf8
" Don't redraw while executing macros (good performance config)
set lazyredraw
" Repeats previous line spacing (tabs + comments)
set autoindent
" Wrap lines
set wrap
" Line numbs
set number
" Relative line numbs
set rnu

" Time out on key codes but not mappings.
" Basically this makes terminal Vim work sanely.
set notimeout
set ttimeout
set ttimeoutlen=10
set noesckeys

" Remove any trailing whitespace that is in the file
autocmd BufRead,BufWrite * if ! &bin | silent! %s/\s\+$//ge | endif

" Goodbye annoying modeline error messages
set modelines=0

" Restore cursor position on file open {{{
augroup JumpCursorOnEdit
	au!
	autocmd BufReadPost *
	\ if expand("<afile>:p:h") !=? $TEMP |
	\	if line("'\"") > 1 && line("'\"") <= line("$") |
	\		let JumpCursorOnEdit_foo = line("'\"") |
	\		let b:doopenfold = 1 |
	\		if (foldlevel(JumpCursorOnEdit_foo) > foldlevel(JumpCursorOnEdit_foo - 1)) |
	\			let JumpCursorOnEdit_foo = JumpCursorOnEdit_foo - 1 |
	\			let b:doopenfold = 2 |
	\		endif |
	\		exe JumpCursorOnEdit_foo |
	\	endif |
	\ endif
	" Need to postpone using "zv" until after reading the modelines.
	autocmd BufWinEnter *
	\ if exists("b:doopenfold") |
	\	exe "normal zv" |
	\	if(b:doopenfold > 1) |
	\		exe  "+".1 |
	\	endif |
	\	unlet b:doopenfold |
	\ endif
augroup END
" }}}

" Set the colorscheme for gvim
if has('gui_running')
	set background =dark
	colorscheme solarized
endif

" }}}

" Plugin stuff -------------------------------------------------{{{

" Plugin mappings are in 'Keybindings/remappings' or 'Leaders'

" For syntastic {{{
hi clear SignColumn " for plugins like Syntastic putting symbols in sign column

let g:syntastic_error_symbol = '✘'
let g:syntastic_warning_symbol = "▲"
augroup mySyntastic
	au!
	au FileType tex let b:syntastic_mode = "passive"
augroup END
" }}}

" For autoclose {{{
let g:AutoClosePairs = "() [] \" '"
" }}}

" For ctrlp {{{
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
let g:ctrlp_working_path_mode = 'ra'
" }}}

" For nerdtree {{{
set autochdir
let NERDTreeChDirMode=2
" }}}

" For conqueterm {{{
"let g:ConqueTerm_Color = 1
" }}}

" For airline {{{
"let g:airline_powerline_fonts = 1
" Always show airline status
set laststatus=2
" Hide the default mode text (e.g. -- INSERT -- below the statusline
set noshowmode
" }}}

" }}}

" Keybindings/remappings ---------------------------------------{{{

noremap H ^
noremap L $
inoremap {<CR> {<CR>}<Esc>O
cmap W w<CR>
cmap Q q<CR>
cmap w! !sudo tee %
noremap / /\v
noremap S :%s/

" }}}

" Leaders ------------------------------------------------------{{{

" Map the leader to...
let mapleader =","
" And the localleader to...
let maplocalleader ="\\"

nnoremap <Leader>c :setlocal spell!<CR>
nnoremap <Leader>x :ConqueTermVSplit bash --norc<CR>
nnoremap <Leader>z :ConqueTermSplit bash --norc<CR>
nnoremap <Leader>n :NERDTreeToggle .<CR>
nnoremap <Leader><Space> :let @/ = ""<CR>

nnoremap <Leader>\ :vertical resize 80<CR>
nnoremap <Leader>[ :vertical resize -10<CR>
nnoremap <Leader>] :vertical resize +10<CR>
nnoremap <Leader>{ :vertical resize -1<CR>
nnoremap <Leader>} :vertical resize +1<CR>

nnoremap <Leader>- :resize -10<CR>
nnoremap <Leader>= :resize +10<CR>
nnoremap <Leader>_ :resize -1<CR>
nnoremap <Leader>+ :resize +1<CR>

" }}}

" Filetype options ---------------------------------------------{{{

" augroup stops autocmd spam caused by repeated reloading of vimrc
augroup vimrc_autocmd
	autocmd!

	" C and C++ {{{
	autocmd FileType c setlocal comments-=://
	autocmd FileType c setlocal comments+=://
	" }}}
	" HTML {{{
	autocmd FileType html set tabstop=2
	autocmd FileType html set shiftwidth=2
	autocmd FileType html set expandtab
	" }}}
	" Java {{{
	autocmd FileType java setlocal comments-=://
	autocmd FileType java setlocal comments+=f://
	" }}}
	" Perl {{{
	autocmd FileType perl setlocal comments-=:#
	autocmd FileType perl setlocal comments+=:#
	" }}}
	" Ruby {{{
	autocmd FileType ruby setlocal comments-=:#
	autocmd FileType ruby setlocal comments+=f:#
	autocmd FileType ruby set tabstop=2
	autocmd FileType ruby set shiftwidth=2
	autocmd FileType ruby set expandtab
	autocmd FileType ruby imap <S-CR> <CR><CR>end<Esc>-cc
	" }}}
	" Shell {{{
	autocmd FileType sh setlocal comments-=:#
	autocmd FileType sh setlocal comments+=:#
	" }}}
	" Vim {{{
	autocmd Filetype vim let g:AutoClosePairs = "() []"
	" }}}

augroup END

" }}}

"" ## added by OPAM user-setup for vim / base ## 93ee63e278bdfc07d1139a748ed3fff2 ## you can edit, but keep this line {{{
"let s:opam_share_dir = system("opam config var share")
"let s:opam_share_dir = substitute(s:opam_share_dir, '[\r\n]*$', '', '')
"
"let s:opam_configuration = {}
"
"function! OpamConfOcpIndent()
"  execute "set rtp^=" . s:opam_share_dir . "/ocp-indent/vim"
"endfunction
"let s:opam_configuration['ocp-indent'] = function('OpamConfOcpIndent')
"
"function! OpamConfOcpIndex()
"  execute "set rtp+=" . s:opam_share_dir . "/ocp-index/vim"
"endfunction
"let s:opam_configuration['ocp-index'] = function('OpamConfOcpIndex')
"
"function! OpamConfMerlin()
"  let l:dir = s:opam_share_dir . "/merlin/vim"
"  execute "set rtp+=" . l:dir
"endfunction
"let s:opam_configuration['merlin'] = function('OpamConfMerlin')
"
"let s:opam_packages = ["ocp-indent", "ocp-index", "merlin"]
"let s:opam_check_cmdline = ["opam list --installed --short --safe --color=never"] + s:opam_packages
"let s:opam_available_tools = split(system(join(s:opam_check_cmdline)))
"for tool in s:opam_packages
"  " Respect package order (merlin should be after ocp-index)
"  if count(s:opam_available_tools, tool) > 0
"    call s:opam_configuration[tool]()
"  endif
"endfor
"" ## end of OPAM user-setup addition for vim / base ## keep this line }}}

