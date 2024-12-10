# Vite Fusion: Integrating Vite with Flask

**Author**: Claudio González © 2024 Banshee  
**Website**: [https://www.banshee.pro/](https://www.banshee.pro/)  
**License**: MIT License

---

This module provides functions to register and serve Vite generated assets in Flask applications. It supports both the Vite development server and production environments using the `manifest.json` file.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Parameters](#parameters)
- [Examples](#examples)
- [License](#license)

---

## Installation

On your Python interpreter `pip install vite-fusion` then:

1. Install the required dependencies for Flask and Vite.
2. Copy the `register_vite_assets` function into your project.

---

## Usage

After initializing your Flask application, call the `register_vite_assets` function to integrate Vite assets.

### Example Usage:

```python
from vite_fusion import register_vite_assets

app = Flask(__name__)

register_vite_assets(
    app,
    dev_mode=True,
    dev_server_url="http://localhost:5173",
    manifest_path="src/dist/.vite/manifest.json",
    nonce_provider=my_nonce_provider,  # Optional
    logger=my_logger                   # Optional
)
```

---

## Parameters

| Parameter        | Type                 | Description                                                                                     | Default Value                  |
|-------------------|----------------------|-------------------------------------------------------------------------------------------------|--------------------------------|
| `app`            | `Flask`             | The Flask application instance.                                                                | **Required**                  |
| `dev_mode`       | `bool`              | Indicates if the Vite development server is running.                                           | `True`                        |
| `dev_server_url` | `str`               | URL of the Vite development server (e.g., `http://localhost:5173`).                            | `"http://localhost:5173"`     |
| `manifest_path`  | `str`               | Path to the production `manifest.json` generated by Vite.                                      | `"src/dist/.vite/manifest.json"` |
| `nonce_provider` | `callable` or `None`| Function returning a `nonce` (string) for CSP headers. If `None`, no `nonce` attribute is added.| `None`                        |
| `logger`         | `logging.Logger` or `None` | Logger instance for errors and warnings. If `None`, logging is disabled.                      | `None`                        |

---

## manifest.json in dev mode?

Although accessing the `manifest.json` file in development mode is not a common practice, we concluded that searching for and loading files directly from it in development mode, without needing to set up an array of files, is the most appropriate approach. As a result, the `manifest.json` file must be available in both development and production environments. This is why we recommend running npm run build before starting to use this integration.

---

## Examples

### Registering Vite Assets in Development Mode

```python
register_vite_assets(
    app,
    dev_mode=True,
    dev_server_url="http://localhost:5173",
    manifest_path="src/dist/.vite/manifest.json"
)
```

### Registering Vite Assets in Production Mode

```python
register_vite_assets(
    app,
    dev_mode=False,
    manifest_path="src/dist/.vite/manifest.json",
    nonce_provider=my_nonce_provider
)
```

or

```python
register_vite_assets(
    homedock_www,
    dev_mode=False,
    manifest_path="src/dist/.vite/manifest.json",
    nonce_provider=nonce_value,
    logger=None
)
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## About This Integration

This integration was created to work seamlessly with our project, **HomeDock OS**. HomeDock OS is a powerful and flexible platform for home automation and cloud management. Learn more at [homedock.cloud](https://www.homedock.cloud).

---

## Contributing and Support

Feel free to fork this repository and contribute! For any bug fixes, security concerns, or other issues, please email us at [claudio@banshee.pro](mailto:claudio@banshee.pro).
