-- per rustaceanvim:
-- Do not call the nvim-lspconfig.rust_analyzer setup or set up the LSP client for rust-analyzer manually, as doing so may cause conflicts.
-- require("lvim.lsp.manager").setup("rust_analyzer", {
--   -- doesn't work by default on LunarVim's version of `nvim-lspconfig`
--   settings = {
--     ["rust-analyzer"] = {
--       cargo = { allFeatures = true },
--       procMacro = { enable = true },
--     },
--   },
-- })

vim.g.rustaceanvim.server.logfile = "/tmp/rustaceanvim.log"

local bufnr = vim.api.nvim_get_current_buf()

vim.keymap.set(
  "n",
  "K", -- Override Neovim's built-in hover keymap with rustaceanvim's hover actions
  function()
    vim.cmd.RustLsp({ 'hover', 'actions' })
  end,
  { silent = true, buffer = bufnr }
)
