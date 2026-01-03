--[[
lvim is the global options object
]]
-- THESE ARE EXAMPLE CONFIGS FEEL FREE TO CHANGE TO WHATEVER YOU WANT

-- lvim.colorscheme = "oxocarbon" -- the best color scheme, except I can't stand having diffs without red/green colros
-- lvim.colorscheme = "catppuccin-mocha"
lvim.colorscheme = "tokyonight-moon"

-- general
lvim.log.level = "warn"
-- to disable icons and use a minimalist setup, uncomment the following
-- lvim.use_icons = false

-- keymappings [view all the defaults by pressing <leader>Lk]
lvim.leader = "space"
-- add your own keymapping
lvim.keys.insert_mode["<Tab>"] = "<Tab>" -- disabled by default for some reason?
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

-- Mason doesn't setup rust-analyzer by default
vim.list_extend(lvim.lsp.automatic_configuration.skipped_servers, { "rust_analyzer" })
local opts = {
  -- Your custom rust-analyzer settings here
  settings = {
    ["rust-analyzer"] = {
      -- checkOnSave = {
      --   command = "clippy",
      -- },
    },
  },
}
-- Use the built-in lvim lsp manager to setup the server
require("lvim.lsp.manager").setup("rust_analyzer", opts)

local formatters = require "lvim.lsp.null-ls.formatters"
local linters = require "lvim.lsp.null-ls.linters"
local code_actions = require "lvim.lsp.null-ls.code_actions"

formatters.setup {
  {
    name = "black",
    -- args = { "--line-length", "120" },
  },
  {
    name = "ruff",
  },
}
linters.setup {
  {
    name = "ruff",
  },
  {
    name = "flake8",
    args = {
      -- "--max-line-length", "120",
      "--ignore", "E203,E501,W503",
    },
  },
  -- {
  --   name = "stylua",
  --   args = { "--indent-width", "2", "--indent-type", "Spaces" },
  -- },
}
code_actions.setup {}

lvim.format_on_save.pattern = { "*.py", "*.rs", "*.lua" }

-- if you don't want all the parsers change this to a table of the ones you want
lvim.builtin.treesitter.ensure_installed = {
  "bash",
  "c",
  "gdscript",
  "godot_resource",
  -- "gdshader",
  "javascript",
  "json",
  "lua",
  "python",
  "rust",
  "typescript",
  "tsx",
  "css",
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
-- lvim.builtin.treesitter.indent = {
--   -- Fix for treesitter indent affecting Python files
--   -- https://github.com/LunarVim/LunarVim/issues/2630
--   enable = true,
--   disable = { "yaml", "python" },
-- } -- treesitter is buggy for these languages :(
--require("nvim-treesitter.configs").setup({})
lvim.builtin.treesitter.incremental_selection = {
  enable = true,
  keymaps = {
    -- AST node-based selection
    init_selection = "<C-space>",
    node_incremental = "<C-space>",
    scope_incremental = false,
    node_decremental = "<bs>",
  },
}

lvim.builtin.treesitter.textobjects.select = {
  enable = true,

  keymaps = {
    -- You can use the capture groups defined in textobjects.scm
    ["a="] = { query = "@assignment.outer", desc = "Select outer part of an assignment" },
    ["i="] = { query = "@assignment.inner", desc = "Select inner part of an assignment" },
    ["l="] = { query = "@assignment.lhs", desc = "Select left hand side of an assignment" },
    ["r="] = { query = "@assignment.rhs", desc = "Select right hand side of an assignment" },

    ["aa"] = { query = "@parameter.outer", desc = "Select outer part of a parameter/argument" },
    ["ia"] = { query = "@parameter.inner", desc = "Select inner part of a parameter/argument" },

    ["ai"] = { query = "@conditional.outer", desc = "Select outer part of a conditional" },
    ["ii"] = { query = "@conditional.inner", desc = "Select inner part of a conditional" },

    ["al"] = { query = "@loop.outer", desc = "Select outer part of a loop" },
    ["il"] = { query = "@loop.inner", desc = "Select inner part of a loop" },

    ["af"] = { query = "@call.outer", desc = "Select outer part of a function call" },
    ["if"] = { query = "@call.inner", desc = "Select inner part of a function call" },

    ["am"] = { query = "@function.outer", desc = "Select outer part of a method/function definition" },
    ["im"] = { query = "@function.inner", desc = "Select inner part of a method/function definition" },

    ["ac"] = { query = "@class.outer", desc = "Select outer part of a class" },
    ["ic"] = { query = "@class.inner", desc = "Select inner part of a class" },
  },
}

-- For better Godot support
--
-- local is_godot_project = false
-- local godot_project_path = ''
-- local cwd = vim.fn.getcwd()
-- if vim.uv.fs_stat(cwd .. '/project.godot') then
--   is_godot_project = true
--   godot_project_path = cwd
-- end
-- if vim.uv.fs_stat(cwd .. '/../project.godot') then
--   is_godot_project = true
--   godot_project_path = cwd .. '/..'
-- end


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
      pattern = { "*.rs" },
      callback = function()
        vim.opt.tabstop = 4
        vim.opt.shiftwidth = 4
        vim.opt.shiftround = true
        vim.opt.expandtab = true
      end
    }
  },
}

-- ----------------------------------------------------------------
-- Plugins and their specific config
lvim.plugins = {

  -- --------------------------------------------------------------
  -- TOOLS
  { "tpope/vim-fugitive" },
  {
    "epwalsh/obsidian.nvim",
    dependencies = {
      "nvim-lua/plenary.nvim",
    },
    config = function()
      require("obsidian").setup({
        workspaces = {
          {
            name = "knowledgebase",
            path = "~/Documents/knowledgebase/",
          },
        },
        -- Optional, boolean or a function that takes a filename and returns a boolean.
        -- `true` indicates that you don't want obsidian.nvim to manage frontmatter.
        disable_frontmatter = true,
      })
    end,
  },
  {
    "folke/zen-mode.nvim",
    opts = {
      -- your configuration comes here
      -- or leave it empty to use the default settings
      -- refer to the configuration section below
    }
  },

  -- --------------------------------------------------------------
  -- THEMING AND ERGONOMICS
  { "nyoom-engineering/oxocarbon.nvim" },
  { "catppuccin/nvim" },
  { "folke/tokyonight.nvim" },
  {
    "alexghergh/nvim-tmux-navigation",
    config = function()
      require 'nvim-tmux-navigation'.setup {
        -- disable_when_zoomed = true, -- defaults to false
        keybindings = {
          left = "<C-h>",
          down = "<C-j>",
          up = "<C-k>",
          right = "<C-l>",
          -- last_active = "<C-\\>",
          -- next = "<C-Space>",
        }
      }
    end,
  },

  -- --------------------------------------------------------------
  -- LANGUAGES
  -- {
  --   'mrcjkb/rustaceanvim',
  --   version = '^6', -- Recommended
  --   lazy = false,   -- This plugin is already lazy
  --   -- opt = {},
  -- },
}

lvim.builtin.which_key.mappings["G"] = {
  name = "Git",
  o = { "<cmd>!open_github.sh<CR>", "Open on GitHub", mode = { "n" } },
  s = { "<cmd>Git status<CR>", "status", mode = { "n" } },
  d = { "<cmd>Gvdiff<CR>", "diff", mode = { "n" } },
  D = { "<cmd>Gvdiff HEAD<CR>", "diff HEAD", mode = { "n" } },
  l = { "<cmd>Git log<CR>", "log", mode = { "n" } },
  L = { "<cmd>Git logg<CR>", "log --graph", mode = { "n" } },
}

lvim.builtin.which_key.mappings["r"] = {
  name = "Rust",
  -- r = { "<cmd>RustLsp runnables<CR>", "Runnables" },
  -- t = { "<cmd>RustLsp testables<CR>", "Testables" },
  -- e = { "<cmd>RustLsp expandMacro<CR>", "Macro Expand" },
  -- h = { "<cmd>RustLsp hover actions<CR>", "Hover" },
  -- p = { "<cmd>RustLsp rebuildProcMacros<CR>", "Rebuild Macros" },
  -- g = { "<cmd>RustLsp codeAction<CR>", "Code Action" },
  -- x = { "<cmd>RustLsp explainError<CR>", "Explain Error" },
  -- d = { "<cmd>RustLsp renderDiagnostic<CR>", "Diagnostic" },
  -- c = { "<cmd>RustLsp flyCheck<CR>", "Check" },
  c = { "<cmd>!cargo check<CR>", "Check" },
  r = { "<cmd>!cargo run<CR>", "Run" },
  t = { "<cmd>!cargo test<CR>", "Test" },
}
