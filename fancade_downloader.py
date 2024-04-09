import zlib
import requests
import os

file = input("Fancade Link (should have https://play.fancade.com/): ")
file = file.split(".com/")[1]
print("Downloading \"" + file + "\"...")
meta = requests.get("https://firebasestorage.googleapis.com/v0/b/fancade-live.appspot.com/o?name=games%2F"+file).json()
stream = requests.get("https://firebasestorage.googleapis.com/v0/b/fancade-live.appspot.com/o?name=games%2F"+file+"&alt=media&token="+meta["downloadTokens"], stream=True)
length = 0
with open(file, "wb") as f:
    for chunk in stream.iter_content(chunk_size=1024*1024):
        f.write(chunk)
        length += len(chunk)
        print("\033[1K\r" + str(int(length/10485.76)/100) + "MB so far...")
    f.close()
print("\033[1K\r" + str(int(length/10485.76)/100) + "MB of game box content downloaded.")
data = list(zlib.decompress(open(file, "rb").read()))
pointer = 2
print("Game name: " + bytes(data[pointer + 1:pointer + data[pointer] + 1]).decode())
pointer += data[pointer] + 1
print("By: " + bytes(data[pointer + 1:pointer + data[pointer] + 1]).decode())
pointer += data[pointer] + 1
print("Description: " + bytes(data[pointer + 1:pointer + data[pointer] + 1]).decode())
pointer += data[pointer] + 1
pointer += 4
chunks = data[pointer - 2]
diff = 0
if chunks > 0:
    aw = []
    print("\nPatching all "+str(chunks)+" chunks...")
    for _ in range(chunks):
        patchpp = pointer
        pointer += 2
        if data[pointer] == 3 and data[pointer - 1] in [0x18, 0x19]:
            print("Level found! Patching...")
            flag1 = data[pointer - 2]
            flag2 = data[pointer - 1] == 0x19
            print("Level name: " + bytes(data[pointer + 2:pointer + data[pointer + 1] + 2]).decode())
            pointer += data[pointer + 1] + 2
            if flag2:
                print("Level doesn't have color BLUE!")
                pointer += 1
            if flag1 & 0b100 != 0:
                print("Level has flag CONTAINSBLOCKS!")
                flag3 = 1
                for _ in range(3):
                    flag3 *= data[pointer] + (data[pointer + 1] * 256)
                    pointer += 2
                pointer += flag3 * 2
            else:
                print("Level has no blocks placed in it.")
            if flag1 & 0b10 != 0:
                print("Level has flag CONTAINSCONFIGS!")
                flag4 = data[pointer] + (data[pointer + 1] * 256)
                pointer += 2
                for _ in range(flag4):
                    if data[pointer + 1] <= 4:
                        pointer += 8 + data[pointer + 1]
                    elif data[pointer + 1] == 5:
                        pointer += 20
                    elif data[pointer + 1] == 6:
                        pointer += data[pointer + 8] + 9
            else:
                 print("Level doesn't contain configs.")
            if flag1 & 0b1 != 0:
                print("Level has flag CONTAINSWIRINGS!")
                pointer += ((data[pointer] + (data[pointer + 1] * 256)) * 24) + 2
            else:
                print("Level doesn't have wiring data.")
        else:
            if data[pointer - 2] & 8 != 0:
                if data[pointer - 1] & 8 != 0:
                    print("Custom Block found! Patching...")
                    flag0 = [data[pointer - 2] & 32 != 0, False]
                    flag1 = data[pointer - 2] & 0x10 != 0
                    flag2 = data[pointer - 2] & 0x07
                    if data[pointer - 1] & 0x10 != 0:
                        if data[pointer] == 1:
                            print("Custom Block is type Physics.")
                        elif data[pointer] == 2:
                            print("Custom Block is type Script.")
                            flag0[1] = True
                        pointer += 1
                    print("Custom Block name: " + bytes(data[pointer + 1:pointer + data[pointer] + 1]).decode())
                    pointer += data[pointer] + 1
                    if flag0[0] or flag0[1]:
                        pointer += 1
                    flag3 = data[pointer] + (data[pointer + 1] * 256)
                    pointer += 0xC00
                    if flag1:
                        print("Custom Block is flagged as MULTIBLOCK!")
                        pointer += 5
                        aw.append(flag3)
                    if flag2 != 0:
                        print("Custom Block has blocks inside!")
                        if flag2 & 4 != 0:
                            flag3 = 1
                            for _ in range(3):
                                flag3 *= data[pointer] + (data[pointer + 1] * 256)
                                pointer += 2
                            pointer += flag3 * 2
                        if flag2 & 2 != 0:
                            flag4 = data[pointer] + (data[pointer + 1] * 256)
                            pointer += 2
                            for _ in range(flag4):
                                if data[pointer + 1] <= 4:
                                    pointer += 8 + data[pointer + 1]
                                elif data[pointer + 1] == 5:
                                    pointer += 20
                                else:
                                    pointer += data[pointer + 8] + 9
                        if flag2 & 1 != 0:
                            pointer += ((data[pointer] + (data[pointer + 1] * 256)) * 24) + 2
                else:
                    print("Custom Block multiblock part found! Patching...")
                    flag0 = [data[pointer - 2] & 32 != 0, data[pointer] == 2, data[pointer - 1] & 0x10 != 0]
                    if flag0[0] or flag0[1]:
                        pointer += 1
                    if flag0[2]:
                        pointer += 1
                    pointer += 0xC05
            else:
                raise Exception(hex(pointer))
                pass
        data[patchpp] &= 0b10111111
        data[patchpp + 1] &= 0b10111111
    print("Saving file...")
    open(file, "wb").write(zlib.compress(bytes(data)))
else:
    print("\nYour game is empty.")
print("Remember: To import the game to Fancade, you must put the saved game file in a zip file. This was inserted to prevent kids from asking this.")
