# WinAPDev

A lightweight Windows development environment that launches **Apache + PHP** without bundling MySQL or other
databases.  
Powered by **Python**, WinAPDev makes it easy to spin up a minimal PHP development server on Windows.

---

## ✨ Features

- 🚀 Quick launch of **Apache + PHP** on Windows
- 🐍 Python-powered control (start/stop/manage)
- ⚡ Lightweight compared to full stacks like XAMPP/WAMP
- 🎯 Focused only on PHP development (no MySQL or extra services)
- 🔒 Simple, portable, and easy to set up

---

## 📦 Requirements

- Windows 10/11
- Python 3.8+
- Apache HTTP Server
- PHP (any supported version)

---

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/WinAPDev.git
   cd WinAPDev
   uv venv   
   
   .venv\Scripts\activate
   uv pip install -r requirements.txt   
   ```   

## 🖥️ Commands

You have to navigate to project root folder first and activate the venv by hitting the below command

```bash
   .venv\Scripts\activate
```

| Command                      | Description                                            |
|------------------------------|--------------------------------------------------------|
| `python run dev:setup`       | Setup Apache + PHP environment server                  |
| `python run dev:clear`       | Remove Apache + PHP environment server                 |
| `python run service:stop`    | Stop the All services                                  |
| `python run service:start`   | Start all services                                     |
| `python run service:restart` | Restart all services                                   |
| `python run service:remove`  | Remove all services                                    |
| `python run service:install` | Install all services                                   |
| `python run vhost:add`       | Adding additional name in virtual host for new project |
| `python run vhost:remove`    | Removing existing vhost names from configuration       |


