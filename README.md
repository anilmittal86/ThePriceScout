
# Steam Price Drop Tracker

A Telegram bot that tracks Steam game prices and notifies you of drops.

## How to Run

### Option 1: Keep it Visible (Recommended for now)
Run this command in your terminal:
```bash
python main.py
```
**Note**: You must keep the terminal window **OPEN** for the bot to check prices. If you close the window, the bot stops.

### Option 2: Run in Background (Hidden)
If you want it to run even after you close the window, use `pythonw` (Windows only):
```bash
pythonw main.py
```
*   **To Stop it**: Open Task Manager, find `pythonw.exe`, and end the task.
*   **Logs**: Check `bot.log` to see what it's doing since you won't have a visible window.

## Commands
- `/add <app_id>`: Add a game (e.g., `813780` for AoE II: DE).
- `/list`: See your watchlist.
- `/remove <app_id>`: Remove a game.

## Configuration
- **Frequency**: Checks prices every 24 hours.
- **Data**: Stored in `steam_tracker.db`.
