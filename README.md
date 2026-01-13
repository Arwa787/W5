# Instructions

## Lab Setup

### A. Local Setup

1. Use `git clone` to clone the repository
2. Use `uv sync` to install the dependencies in a virtual environment

> [How to run VS Code Notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)

### B. Colab Setup

1. Open the notebook in Colab
2. Use `git clone` to clone the repository (to get helper files, assets, and datasets)
3. Run `%cd <path to the repository>`
4. Sync dependencies from `pyproject.toml` into the Colab system environment: `!uv sync --system` (notice the `!` prefix tells notebooks this is a shell command)

> Remember to save your work. Any files created in Colab will be lost if you don't save them elsewhere (Download).

### C. Code Locally, Run in Colab (Hybrid)

> See: [Connect notebooks to Colab servers](https://marketplace.visualstudio.com/items?itemName=google.colab)>