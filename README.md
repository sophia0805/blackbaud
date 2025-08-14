# blackbaud auto-login

> blackbaud is the grading/assignments system for my school, but unfortunately it takes way too long to log in (you have to type in your email, then click next, then click continue, then click your email AGAIN)
- so this basically simplies the process into one command!

## features
- checks if blackbaud is already open (in the first tab) and if not, opens it as a tab
- types in your email
- clicks next, then continue
- clicks your google account

## installation
1. Clone the repository
```bash
git clone https://github.com/sophia0805/blackbaud
cd blackbaud
```
2. Install dependencies
```bash
pip install python-dotenv
```
3. Create .env file
```bash
email=""
```
4. Run the script
```bash
python3 blackbaud.py
```

## demonstration  
![video](https://hc-cdn.hel1.your-objectstorage.com/s/v3/99d238d4426d954a2d3de64f52761e7d139192e3_blackbaud_script.mp4)