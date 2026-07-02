```markdown
# 🛒 Project Order Management Bot (Binary Secrets Ecosystem)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Bot API](https://img.shields.io/badge/Bot%20Platform-Bale-green.svg)](https://github.com/python-bale-bot/bale.py)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated backend infrastructure and interactive messaging agent built for the development team **Binary secrets**. This system manages client project requests from initial submission to admin evaluation (Accept/Reject Workflow) using an asynchronous state machine architecture over the Bale Messenger Bot API and a highly optimized relational SQLite database.

---

## ✨ Key Features & Enhancements

### 👥 1. Client Interactive Interface (User UI)
* **Step-by-Step Order Wizard:** Guides users through a structured state machine to collect `Project Title`, `Description`, and `Budget/Suggested Amount`.
* **Dynamic Inline Menus:** Rich graphical layout using inline keyboards for seamless navigation (`ثبت سفارش🖌️⚙️`, `سفارش‌های من`, `راهنما🔍`, `پشتیبانی🛡️`).
* **Order Tracking:** Clients can check their active and previous requests fetched in real-time from the ledger.

### 👑 2. Admin Panel & Decision Engine
* **Gateway Authentication:** Dedicated administrative functions restricted to verified team chat IDs.
* **Queue Inspection (`/inline_orders`):** Spawns a dedicated dashboard displaying raw pending orders.
* **One-Click Evaluation:** Admins utilize inline callback buttons to instantly **Accept** or **Reject** proposals.
* **Automated Dispatch:** When an order is approved, the system automatically triggers a confirmation broadcast back to the client, facilitating subsequent deposit/advanced payment interactions.

### ⚡ 3. Performance & Structural Optimizations
* **Persistent Cursor Lifecycle:** Shared execution pool Utilizing a singular global `self.dat` and `self.cursor` instance initialized once at startup. This prevents excessive database connection spawns, drastically lowering host RAM/CPU consumption.
* **Refined Admin Resolution:** Corrected administrative routing identifiers preventing gateway bypassing or failed operational handshakes.

---

## 🧰 Tech Stack & Modules

* **Core Language:** `Python 3.8+`
* **Bot Framework:** `bale` library (Asynchronous event-driven wrapper for the Bale bot platform).
* **Storage Layer:** `sqlite3` (Relational ledger with persistent query filters and structural optimization).
* **System Utilities:** `os`, `json`.

---

## 🚀 Installation & Infrastructure Setup

### 1. Clone the Source
```bash
git clone [https://github.com/mrtprogrammer1389-ctrl/Data-hider.git](https://github.com/mrtprogrammer1389-ctrl/Data-hider.git)
cd Data-hider

```
### 2. Install Framework Core
Ensure the official asynchronous Bale wrapper is installed:
```bash
pip install bale

```
### 3. Deploy the Pipeline
Run the main script orchestrator to establish the event loop:
```bash
python order_bot.py

```
## 💻 System Architecture & Bot Commands
### Local Data Architecture
The relational database utilizes a high-performance tracking schema in orders.db:
 * **State Management:** Rows maintain status_of_process (e.g., Done, Pending), accept flags (True/False), and a logical erasure flag is_deleted to protect data persistence without data loss.
### Command Matrix
| Command / Trigger | Target Access | Operational Action |
|---|---|---|
| /start | Public / Client | Initializes the workspace interaction and loads the primary entry menu. |
| /inline_orders | Hardcoded Admins Only | Fetches the raw active queue of pending projects with assessment controls. |
| add_order (Callback) | Public / Client | Initiates the multi-state collection script for new project parameters. |
| accept_order:<id> | Hardcoded Admins Only | Approves the target ID, updates the schema, and notifies the end-user. |
| reject_order:<id> | Hardcoded Admins Only | Denies the target ID and updates the execution flag. |
## 📂 Repository Layout
```text
Data-hider/
│
├── data_base.py    # Optimized Database Layer: Controls persistent SQL schemas, order records, and state cursors.
├── order_bot.py    # Main Orchestrator: Event loops, multi-state user dialogues, and administrative validation.
└── orders.db       # Persistent Storage: Auto-generated SQLite container hosting order ledgers.

```
## 🤝 Contributing
 1. Fork the Workspace
 2. Branch your feature updates (git checkout -b feature/DatabaseOptimization)
 3. Commit codebase enhancements (git commit -m 'Optimized SQLite cursor connection')
 4. Push to your upstream branch (git push origin feature/DatabaseOptimization)
 5. Open a professional Pull Request
## 📄 License
Distributed under the MIT License.
## 👤 Author
 * **Lead Engineer:** Mohammad Reza Taghdiri
 * **Organization:** Binary secrets
 * **GitHub Profile:** @mrt-prog
 * **Email:** mrt.programmer1389@gmail.com
 * **Telegram:** @Mohammadhhawhd
*"Turning logic into operational reality."* ⚙️🌐
```

```
