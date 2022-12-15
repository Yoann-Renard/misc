import qrcode
import uuid
try:
    img = qrcode.make(input("Text to convert: ")).convert("RGB")
    _id = str(uuid.uuid4())
    while True:
        action = input("""Display or save QR code ?
    1: Display
    2: Save
    3: Display & save
    >> """)
        if action == "1":
            img.show()
            break
        elif action == "2":
            img.save(_id + ".jpg")
            print(f"QR code saved as {_id}.jpg")
            break
        elif action == "3":
            img.show()
            img.save(_id + ".jpg")
            print(f"QR code saved as {_id}.jpg")
            break
except KeyboardInterrupt:
    print('')
finally:
    print("Bye ^-^")
    exit(0)
