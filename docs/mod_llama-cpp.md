# Local inference

The `llama-cpp` module installs llama.cpp for Linux x86_64 and supplies a systemd
user service. Its built-in chat UI and OpenAI-compatible API use the same local
server, without a separate desktop application.

## Setup

Add `"llama-cpp"` to `[data].modules` with `chezmoi edit-config`, then run
`chezmoi apply`. Installation requires `curl`, `tar`, `sha256sum`, `libvulkan1`,
a compatible Vulkan GPU driver, and a working systemd user session. These system
dependencies must already be installed.

The [installer](../run_onchange_after_install_llama_cpp.sh.tmpl) downloads the
official Ubuntu Vulkan archive for release `b10948`, verifies its pinned SHA-256,
and checks that the binary runs before publishing the runtime. It lives under
`~/.local/share/llama.cpp/b10948`; `current` selects the installed release.
Versions and checksums are maintained together in the installer.

Place a compatible GGUF model at `~/.local/share/llama.cpp/models/model.gguf`,
symlink that path to an existing model, or choose a path in the optional settings:

```toml
[data.llamaCpp]
model = "/absolute/path/to/model.gguf"
context = 16384
device = "Vulkan0"
port = 8080
```

These machine-specific settings are preserved when rerunning `chezmoi init`.

Models are neither downloaded nor tracked by this module. Existing LM Studio
GGUF files can be reused; preserve their directory structure when moving split
models so all shards remain together. LM Studio removal and model migration are
separate machine-local operations, not recurring apply actions.

## Running

Apply installs the runtime and reloads systemd's user units; it does not start or
enable the service. After selecting a model:

```sh
systemctl --user start llama-server
systemctl --user status llama-server
journalctl --user -u llama-server -f
```

The chat UI is at `http://127.0.0.1:8080` and the API base URL is
`http://127.0.0.1:8080/v1` with the default port. The server binds only to
loopback and restricts allowed CORS origins to localhost. Use
`systemctl --user enable llama-server` if it should start with the user session.

The [environment template](../dot_config/llama.cpp/server.env.tmpl) uses native
llama-server settings: the default context is 16K tokens, Flash Attention is
enabled, GPU layer offload is requested, and one inference slot is used. The
default device is `Vulkan0`, the first Vulkan GPU. Run `llama-server --list-devices`
and set `device` to the desired GPU on machines with multiple adapters. Actual
GPU use depends on the model, available memory, and Vulkan driver. Service logs
show device selection and loading errors.

The [service](../dot_config/systemd/user/llama-server.service) reads the rendered
`~/.config/llama.cpp/server.env` on startup. After changing chezmoi settings, run
`chezmoi apply` and explicitly restart the service. The `llama-server` command in
`~/.local/bin` points directly to the runtime: it does not load the service's
environment file. Supply flags such as `--model /path/to/model.gguf` when running
it directly, and stop the service first if using its port.

## Retiring the module

Run `systemctl --user disable --now llama-server` before removing `"llama-cpp"`
from the module selection. Disabling management does not remove deployed files,
installed runtimes, or models.
