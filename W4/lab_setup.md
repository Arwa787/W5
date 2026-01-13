# Lab Setup

## Client-Server Architecture

Since CPUs are not enough for Deep Learning models; we'll need a GPU. Understanding the client-server interaction is crucial for working with remote code execution environments such as Google Colab.

![](./assets/jupyter-server.png){fig-align="center"}

The image above shows how we interact with remote servers, such as Google Colab, to run our code:

1. We write code in the browser using Jupyter Notebooks or VS Code
2. On save: the code is sent to the Juypter/Colab Server and stored there as `.ipynb` files
3. On run: the code is: 
   1. sent to the kernel for execution
   2. then back to the server to save the results
   3. which are then sent back to the browser


You may want to use [Google Colab for VS Code](https://marketplace.visualstudio.com/items?itemName=google.colab) extension allows you to work in VS Code while the code is sent and executed in Colab servers. However, the steps above are still required.

Otherwise:

- Open Colab and open the notebook file (either via an upload or from GitHub).
- After the notebook opens, make sure to drag and drop associated files like `helper_utils.py` into the side-panel to upload them.
