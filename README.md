# Attendance
Attendance parser for my mother's biometric scanner.

## How to run
1. `pip3 install -r requirements.txt`
2. Save your attendance file as attendance.txt
3. `python3 attendance.py`
4. See attendance data on localhost:5000 on your browser.

## TODO

1. [] Better UX
2. [] Ease of setup (should not need flask server, should be selfhostable with ease, etc.)
3. [] Easier workflows (email support, file upload?)
4. [] Code cleanup

## Notes
- This was supposed to be a one off project but due to the lack of better parsing software, I will polish this a little so its useable for non-tech folk, or maybe self host this.
- I know the code is not good, this was not meant to be public. It is a solution that is for my mother's business needs.
- This is compatible and only tested with the data from [Realtime Eco S C101 Biometric Attendance](https://www.amazon.in/Realtime-Biometric-Attendance-Systems-Excel/dp/B084S5XP7H). It's a big pain to use, hence I have made this to makes sense of the weird format it gives data in.
