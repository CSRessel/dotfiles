-- vim.g.rustaceanvim.server.logfile = "/tmp/rustaceanvim.log"
-- local bufnr = vim.api.nvim_get_current_buf()
-- vim.keymap.set(
--   "n",
--   "K", -- Override Neovim's built-in hover keymap with rustaceanvim's hover actions
--   function()
--     vim.cmd.RustLsp({ 'hover', 'actions' })
--   end,
--   { silent = true, buffer = bufnr }
-- )

vim.opt_local.tabstop = 4
vim.opt_local.shiftwidth = 4
vim.opt_local.expandtab = true
