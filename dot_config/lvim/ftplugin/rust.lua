require("lvim.lsp.manager").setup("rust_analyzer", {
  -- doesn't work by default on LunarVim's version of `nvim-lspconfig`
  settings = {
    ["rust-analyzer"] = {
      cargo = { allFeatures = true },
      procMacro = { enable = true },
    },
  },
})
