<p align="center">
  <img src="https://github.com/user-attachments/assets/14b2c4c2-4a11-4bea-85de-fa660dfe591e" alt="InzelSec Logo" width="150"/>
</p>


# Reverse Shell Listener

A Python implementation of a simple **reverse shell listener**.  
(like Netcat listener)

---

## Installation

Clone the repository and make the script executable:

```bash
git clone https://github.com/InzelSec/net-listener.git
cd reverse-shell-listener
chmod +x listener.py
```



Start listener (listens on port 4444 by default):
```
python3 listener.py
```
Start listener on a custom port:
```
python3 listener.py 9001
```
Once a reverse shell connects:
```
Shell> whoami
Shell> uname -a
Shell> exit
```

## Output Example:

<img width="891" height="344" alt="Screenshot 2025-08-28 at 11 06 19" src="https://github.com/user-attachments/assets/435f85ce-2f0d-4750-a45d-607ef341a958" />




