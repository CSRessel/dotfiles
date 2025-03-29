vim.opt.expandtab = false
local opts = {}

require("lvim.lsp.manager").setup("gdscript", opts)
