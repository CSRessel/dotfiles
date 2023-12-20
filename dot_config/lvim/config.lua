--[[
lvim is the global options object
]]
-- THESE ARE EXAMPLE CONFIGS FEEL FREE TO CHANGE TO WHATEVER YOU WANT

-- general
lvim.log.level = "warn"
-- to disable icons and use a minimalist setup, uncomment the following
-- lvim.use_icons = false

-- keymappings [view all the defaults by pressing <leader>Lk]
lvim.leader = "space"
-- add your own keymapping
lvim.keys.normal_mode["<C-s>"] = ":w<cr>"
lvim.keys.normal_mode["<S-l>"] = ":BufferLineCycleNext<CR>"
lvim.keys.normal_mode["<S-h>"] = ":BufferLineCyclePrev<CR>"
-- unmap a default keymapping
-- vim.keymap.del("n", "<C-Up>")
-- override a default keymapping
-- lvim.keys.normal_mode["<C-q>"] = ":q<cr>" -- or vim.keymap.set("n", "<C-q>", ":q<cr>" )

-- Change theme settings
lvim.builtin.theme.tokyonight.options.dim_inactive = true
lvim.builtin.theme.tokyonight.options.lualine_bold = false

-- Use which-key to add extra bindings with the leader-key prefix
-- lvim.builtin.which_key.mappings["P"] = { "<cmd>Telescope projects<CR>", "Projects" }
-- lvim.builtin.which_key.mappings["t"] = {
--   name = "+Trouble",
--   r = { "<cmd>Trouble lsp_references<cr>", "References" },
--   f = { "<cmd>Trouble lsp_definitions<cr>", "Definitions" },
--   d = { "<cmd>Trouble document_diagnostics<cr>", "Diagnostics" },
--   q = { "<cmd>Trouble quickfix<cr>", "QuickFix" },
--   l = { "<cmd>Trouble loclist<cr>", "LocationList" },
--   w = { "<cmd>Trouble workspace_diagnostics<cr>", "Workspace Diagnostics" },
-- }

lvim.builtin.alpha.active = false
lvim.builtin.alpha.mode = "dashboard"
lvim.builtin.terminal.active = true
lvim.builtin.nvimtree.setup.view.side = "left"
lvim.builtin.nvimtree.setup.renderer.icons.show.git = false

lvim.format_on_save.enabled = true

-- ----------------------------------------------------------------
-- Filetype and language configurations

require "lvim.lsp.null-ls.formatters".setup {
  {
    name = "black",
    args = { "--line-length", "120" },
  }
}

require "lvim.lsp.null-ls.linters".setup {
  {
    name = "flake8",
    args = { "--max-line-length", "120", "--ignore", "E203,W503" },
  }
}

require "lvim.lsp.null-ls.code_actions".setup { }

lvim.format_on_save.pattern = { "*.py" }

-- if you don't want all the parsers change this to a table of the ones you want
lvim.builtin.treesitter.ensure_installed = {
  "bash",
  "c",
  "javascript",
  "json",
  "lua",
  "python",
  "typescript",
  "tsx",
  "css",
  "rust",
  "java",
  "yaml",
}
vim.filetype.add({
  extension = {
    typ = 'typst',
  },
})

lvim.builtin.treesitter.ignore_install = { "haskell" }
lvim.builtin.treesitter.highlight.enable = true
lvim.builtin.treesitter.indent = {
  -- Fix for treesitter indent affecting Python files
  -- https://github.com/LunarVim/LunarVim/issues/2630
  enable = true,
  disable = { "yaml", "python" },
} -- treesitter is buggy for these languages :(

-- Autocommands (https://neovim.io/doc/user/autocmd.html)
-- vim.api.nvim_create_autocmd("BufEnter", {
--   pattern = { "*.json", "*.jsonc" },
--   -- enable wrap mode for json files only
--   command = "setlocal wrap",
-- })
-- vim.api.nvim_create_autocmd("FileType", {
--   pattern = "zsh",
--   callback = function()
--     -- let treesitter use bash highlight for zsh files as well
--     require("nvim-treesitter.highlight").attach(0, "bash")
--   end,
-- })
lvim.autocommands = {
  {
    "BufEnter", -- see `:h autocmd-events`
    {
      pattern = { "*.py" },
      callback = function()
        vim.opt.expandtab = true
        vim.opt.shiftwidth = 4
        vim.opt.shiftround = true
        vim.opt.tabstop = 4
      end
    }
  },
}

-- ----------------------------------------------------------------
-- Plugins and their specific config
lvim.plugins = {
  {
    "zbirenbaum/copilot.lua",
    cmd = "Copilot",
    event = "InsertEnter",
    config = function()
      require("copilot").setup({
        suggestion = {
          enabled = true,
          auto_trigger = true,
          debounce = 75,
          keymap = {
            accept = "<Tab>",
            accept_word = false,
            accept_line = false,
            next = "<M-]>",
            prev = "<M-[>",
            dismiss = "<C-]>",
          },
        },
        filetypes = {
          ["*"] = false,
          ["c"] = true,
          ["c++"] = true,
          ["dockerfile"] = true,
          ["go"] = true,
          ["javascript"] = true,
          ["lua"] = true,
          ["python"] = true,
          ["sh"] = true,
          ["rust"] = true,
          ["terraform"] = true,
          ["typescript"] = true,
          ["yaml"] = true,
        },
      })
    end,
  },
  {
    "jackMort/ChatGPT.nvim",
    event = "VeryLazy",
    config = function()
      require("chatgpt").setup()
    end,
    dependencies = {
      "MunifTanjim/nui.nvim",
      "nvim-lua/plenary.nvim",
      "nvim-telescope/telescope.nvim"
    }
  },
  {
    "ggandor/leap.nvim",
    config = function()
      -- require('leap').add_default_mappings()
    end,
    dependencies = {
      "tpope/vim-repeat",
    }
  },
  { "NoahTheDuke/vim-just" },
  {"IndianBoy42/tree-sitter-just"},
  { "nyoom-engineering/oxocarbon.nvim" },
  { "catppuccin/nvim" },
  { "folke/tokyonight.nvim" },
}

-- vim.g.copilot_assume_mapped = true
-- vim.g.copilot_no_tab_map = true
-- vim.api.nvim_set_keymap("n", "<c-s>", "<cmd>lua require('copilot.suggestion').toggle_auto_trigger()<CR>", opts)
vim.api.nvim_set_keymap("i", "<Tab>", 'copilot#Accept("<Tab>")', { silent = true, expr = true })
vim.api.nvim_set_keymap("i", "<C-S-j>", 'copilot#Next("<CR>")', { silent = true, expr = true })
vim.api.nvim_set_keymap("i", "<C-S-k>", 'copilot#Prev("<CR>")', { silent = true, expr = true })
-- vim.api.nvim_set_keymap("i", "<Tab>", 'copilot#Accept("<Tab>")', { silent = true, expr = true })
-- vim.api.nvim_set_keymap("i", "<C-.>", 'copilot#Next("<C-.>")', { silent = true, expr = true })
-- vim.api.nvim_set_keymap("i", "<C-Space>", 'copilot#Next("<C-Space>")', { silent = true, expr = true })

-- lvim.colorscheme = "oxocarbon" -- the best color scheme, except I can't stand having diffs without red/green colros
-- lvim.colorscheme = "catppuccin-mocha"
lvim.colorscheme = "tokyonight-night"

lvim.builtin.which_key.mappings["a"] = {
  name = "AI (ChatGPT)",
  a = { "<cmd>ChatGPTCompleteCode<CR>", "Complete Code" },
  c = { "<cmd>ChatGPT<CR>", "ChatGPT Prompt" },
  e = { "<cmd>ChatGPTEditWithInstruction<CR>", "Edit with instruction", mode = { "n", "v" } },
  g = { "<cmd>ChatGPTRun grammar_correction<CR>", "Grammar Correction", mode = { "n", "v" } },
  t = { "<cmd>ChatGPTRun translate<CR>", "Translate", mode = { "n", "v" } },
  k = { "<cmd>ChatGPTRun keywords<CR>", "Keywords", mode = { "n", "v" } },
  d = { "<cmd>ChatGPTRun docstring<CR>", "Docstring", mode = { "n", "v" } },
  u = { "<cmd>ChatGPTRun add_tests<CR>", "Add Tests", mode = { "n", "v" } },
  o = { "<cmd>ChatGPTRun optimize_code<CR>", "Optimize Code", mode = { "n", "v" } },
  s = { "<cmd>ChatGPTRun summarize<CR>", "Summarize", mode = { "n", "v" } },
  f = { "<cmd>ChatGPTRun fix_bugs<CR>", "Fix Bugs", mode = { "n", "v" } },
  x = { "<cmd>ChatGPTRun explain_code<CR>", "Explain Code", mode = { "n", "v" } },
  r = { "<cmd>ChatGPTRun roxygen_edit<CR>", "Roxygen Edit", mode = { "n", "v" } },
  l = { "<cmd>ChatGPTRun code_readability_analysis<CR>", "Code Readability Analysis", mode = { "n", "v" } },
}


