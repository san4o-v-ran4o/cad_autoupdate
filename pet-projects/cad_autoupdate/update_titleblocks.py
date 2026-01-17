import os
import sys
import json
import time
import shutil
import win32com.client


def get_base_dir():
    """
    Корректный базовый каталог:
    - для .py
    - для PyInstaller --onefile (.exe)
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def process_dwg(path, block_name, attrs_to_update):
    print(f"\nОткрывается: {path}")

    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = False

    doc = acad.Documents.Open(path)
    time.sleep(0.5)

    found_block = False

    spaces = [doc.ModelSpace]
    for i in range(doc.Layouts.Count):
        spaces.append(doc.Layouts.Item(i).Block)

    for space in spaces:
        for entity in space:
            try:
                if entity.ObjectName != "AcDbBlockReference":
                    continue
            except Exception:
                continue

            if entity.Name != block_name:
                continue

            found_block = True
            print(f"  ✔ найден блок {block_name}")

            for att in entity.GetAttributes():
                if att.TagString in attrs_to_update:
                    old = att.TextString
                    new = attrs_to_update[att.TagString]
                    att.TextString = new
                    print(f"    {att.TagString}: '{old}' → '{new}'")


    if not found_block:
        print(f"  ⚠ блок {block_name} НЕ найден")

    # --- БЕЗОПАСНОЕ СОХРАНЕНИЕ ---
    tmp_path = path + ".tmp.dwg"
    try:
        doc.SaveAs(tmp_path)
    finally:
        doc.Close()
        acad.Quit()

    shutil.move(tmp_path, path)
    print("  💾 сохранено")


def main():
    base_dir = get_base_dir()
    dwg_dir = os.path.join(base_dir, "dwg")
    config_path = os.path.join(base_dir, "config.json")

    if not os.path.isdir(dwg_dir):
        raise RuntimeError(f"Папка dwg не найдена: {dwg_dir}")

    if not os.path.isfile(config_path):
        raise RuntimeError(f"Файл config.json не найден: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    block_name = config["block_name"]
    attrs_to_update = config["attributes"]

    for filename in os.listdir(dwg_dir):
        if filename.lower().endswith(".dwg"):
            path = os.path.join(dwg_dir, filename)
            process_dwg(path, block_name, attrs_to_update)

    print("\nГОТОВО")


if __name__ == "__main__":
    main()
