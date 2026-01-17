import win32com.client

acad = win32com.client.Dispatch("AutoCAD.Application")
acad.Visible = True

print("AutoCAD version:", acad.Version)
input("AutoCAD запущен. Нажми Enter для выхода...")

acad.Quit()
