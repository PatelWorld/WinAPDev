# WinAPDev

A lightweight **Windows PHP development environment** that launches **Apache + PHP** without bundling MySQL or other databases.  
Powered by **Python**, WinAPDev makes it easy to spin up a minimal PHP server with **virtual host management**, **service control**, and **SSL certificate support**.

---

## ✨ Features

- 🚀 Quick launch of **Apache + PHP** on Windows  
- 🐍 Python-powered control (start/stop/manage)  
- ⚡ Lightweight compared to full stacks like XAMPP/WAMP/Laragon  
- 🎯 Focused only on PHP development (no MySQL or extra services)  
- 🖥️ CLI commands for managing services & virtual hosts  
- 🔒 Supports self-signed SSL certificates for HTTPS projects  
- 📂 Virtual host manager with auto `hosts` file update  

---

## 📦 Requirements

- **Windows 10/11**  
- **Python 3.8+**  
- **Apache HTTP Server**  
- **PHP** (any supported version)  

---

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/WinAPDev.git
   cd WinAPDev
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

---

## 🖥️ Usage

Navigate to the project root folder and activate the virtual environment:

```bash
.venv\Scripts\activate
```

### CLI Commands

| Command                      | Description                                            |
|------------------------------|--------------------------------------------------------|
| `python run dev:setup`       | Setup Apache + PHP environment server                  |
| `python run dev:clear`       | Remove Apache + PHP environment server                 |
| `python run service:start`   | Start all services                                     |
| `python run service:stop`    | Stop all services                                      |
| `python run service:restart` | Restart all services                                   |
| `python run service:install` | Install all services as Windows services               |
| `python run service:remove`  | Remove all services                                    |
| `python run vhost:add`       | Add a new project to Apache virtual hosts              |
| `python run vhost:remove`    | Remove an existing virtual host configuration          |

---

## ⚙️ Configuration

- **Apache & PHP Path** → configure in `config/settings.json`  
- **Virtual Hosts** → managed under `conf/httpd-vhosts.conf`  
- **Certificates** → stored in `cert/` folder (auto-generated if SSL is enabled)  

---

## 🌐 Examples

Add a new project with virtual host:

```bash
python run vhost:add --hostname=project.local --dir=C:\Projects\myapp --port=8080
```

---

## 📂 Project Structure

```
WinAPDev/
│── src/                  # Core Python source code
│── run                   # CLI entry script
│── requirements.txt       # Python dependencies
│── README.md              # Documentation
```

---

## 🛠️ Development

- Fork the repo  
- Create a new branch (`feature/my-feature`)  
- Commit your changes  
- Submit a Pull Request  

---

## 📌 Roadmap

- [ ] Add PHP version switcher  
- [ ] Add GUI management tool  
- [ ] Add MySQL or any other database (optional, separate package, configuration based, command based)  
- [ ] Add project templates for Laravel / WordPress  

---

## 🤝 Contributing

Contributions are welcome! Please check the [issues](../../issues) page or open a new one for feature requests and bug reports.

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
