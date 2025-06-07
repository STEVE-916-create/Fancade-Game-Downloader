# Fancade Downloader hack
# go brag about this in r/masterhacker
# 2025 version
# https://github.com/STEVE-916-create/Fancade-Game-Downloader
# ^ report issues at github or if you have my discord, that works too

import zlib, requests, os, io

FIREBASE_HACK_1337 = "https://firebasestorage.googleapis.com/v0/b/fancade-live.appspot.com/o"
DEFAULT_PATCHING_FAIL_MESSAGE = "Please report this bug to me (STEVE). Tell me the game link and this exception message, so that I know what to look for."

def hack_filename_from_game_link(link):
    # old conditions
    if link.find("https://play.fancade.com/") == 0:
        link = link[25:]
    # mistakenly placed http one time haha
    if link.find("http://play.fancade.com/") == 0:
        link = link[24:]
    # check by confirming
    # length is always 16
    if len(link) != 16:
        return None
    # its always in hex format right?
    try:
        bytes.fromhex(link)
    except ValueError:
        return None
    return link

def hack_fancade_server_for_game_data(link):
    link = hack_filename_from_game_link(link)
    if link is None:
        print("Invalid link entered.")
        return
    print("Downloading \"" + link + "\"...")
    print("Hacking the mainframe...")
    token_logger = requests.get(f"{FIREBASE_HACK_1337}?name=games%2F{link}")
    if token_logger.status_code != 200:
        print("Hack failed! Target invalid!!! u r not 1337 check ur link")
        return
    try:
        token_logger = token_logger.json()
    except:
        print("Hack failed! Received payload invalid!!! u r not 1337 check ur link")
        return
    datahacker = token_logger.get("size", "NULL")
    print(f"Content Size: {datahacker}")
    datahacker = token_logger.get("timeCreated", "NULL")
    print(f"Time Created: {datahacker}")
    datahacker = token_logger.get("updated", "NULL")
    print(f"Time Updated: {datahacker}")
    datahacker = token_logger.get("md5Hash", "NULL")
    print(f"MD5 Hash in Base64: {datahacker}")
    token_logger = token_logger.get("downloadTokens")
    if token_logger is None:
        print("Hack failed! NO DOWNLOAD TOKEN!!! u r not 1337 check ur link")
        return
    print("Hacking the Fancade server for game data...")
    hacked_game_data = requests.get(f"{FIREBASE_HACK_1337}?name=games%2F{link}&alt=media&token={token_logger}", stream=True)
    if hacked_game_data.status_code != 200:
        print("Hack failed! server file not found u r not 1337 check ur link")
        return
    hack_matrix_length = 0
    hack_data = io.BytesIO()
    for chunk in hacked_game_data.iter_content(chunk_size=64):
        hack_data.write(chunk)
        hack_matrix_length += len(chunk)
        print(f"\033[1K\rPirating... {int(hack_matrix_length / 100)}KB received.", end="")
    print(f"\033[1K\rPirated {int(hack_matrix_length / 100)}KB of game data.")
    hack_data.seek(0)
    print("I am in.")
    return hack_data

def game_encrypt(hack_data):
    hack_data.seek(0)
    return io.BytesIO(zlib.compress(hack_data.read()))
def game_decrypt(hack_data):
    hack_data.seek(0)
    return io.BytesIO(zlib.decompress(hack_data.read()))

def decrypt_char(hack_data):
    return hack_data.read(1)[0]
def decrypt_short(hack_data):
    return decrypt_char(hack_data) + decrypt_char(hack_data) * 256
def decrypt_str(hack_data):
    l = decrypt_char(hack_data)
    return hack_data.read(l).decode()

def hack_into_computer_by_user(name):
    name = (name * 4).encode()
    return str(name[1]) + "." + str(name[2]) + "." + str(name[3]) + "." + str(name[4])

def hack_fancade_game_data_for_1337_access(hack_data):
    format_version = decrypt_short(hack_data)
    print("Game Information:")
    print(f"    Title: {decrypt_str(hack_data)}")
    fancade_username = decrypt_str(hack_data)
    print(f"    By: {fancade_username}")
    print(f"    Description: {decrypt_str(hack_data)}")
    game_version = decrypt_short(hack_data)
    chunks = decrypt_short(hack_data)
    print(f"Creator's IP Address: {hack_into_computer_by_user(fancade_username)}")
    print(f"Brute force counting blocks...")
    if chunks > 0:
        multiblocks = []
        print(f"Counted {chunks} blocks! Hacking the blocks...")
        for _ in range(chunks):
            chunk_before = hack_data.tell()
            one, three, seven = decrypt_char(hack_data), decrypt_char(hack_data), decrypt_char(hack_data)
            if seven == 3 and three in [0x18, 0x19]:
                print("Block type: Level // Hacking into level...")
                contains_flags = one
                is_not_blue = three == 0x19
                print(f"    Level name: {decrypt_str(hack_data)}")
                if is_not_blue:
                    print("    Level is not BLUE. Brute forcing level color...")
                    hack_data.read(1)
                if contains_flags & 0b100 != 0:
                    print("    Level contains placed blocks! Bragging in r/masterhacker...")
                    dimensional = 1
                    for _ in range(3):
                        dimensional *= decrypt_short(hack_data)
                    hack_data.read(dimensional * 2)
                else:
                    print("    No placed blocks found in level.")
                if contains_flags & 0b10 != 0:
                    print("    Level contains block configurations! Programming Arduino ESP32...")
                    cfg_amount = decrypt_short(hack_data)
                    for _ in range(cfg_amount):
                        kind_of_wire = decrypt_short(hack_data)
                        if kind_of_wire <= 0x4FF:
                            hack_data.read(6 + (kind_of_wire // 0x100))
                        elif kind_of_wire <= 0x5FF:
                            hack_data.read(18)
                        else: # assuming everything thats not a valid type is string
                            hack_data.read(6)
                            hack_data.read(decrypt_char(hack_data))
                else:
                    print("    No block configurations found in level.")
                if contains_flags & 0b1 != 0:
                    print("    Level contains wires! Inserting Flipper Zero...")
                    hack_data.read(decrypt_short(hack_data) * 24)
                else:
                    print("    No wires found in level.")
            elif one & 8 != 0:
                if three & 8 != 0:
                    print("Block type: Custom Block // Hacking into custom block...")
                    is_not_normal_block = three & 0x10 != 0
                    is_script_block = False
                    is_multiblocks = one & 0x10 != 0
                    contains_flags = one & 0x07
                    if not is_not_normal_block:
                        hack_data.seek(hack_data.tell() - 1)
                    print(f"    Custom Block name: {decrypt_str(hack_data)}")
                    if is_not_normal_block:
                        if seven == 1:
                            print("    Custom Block is type Physics. Hacking NASA...")
                        elif seven == 2:
                            print("    Custom Block is type Script. Injecting Roblox exploit...")
                            is_script_block = True
                        else:
                            raise Exception(f"Custom Block type reading error at {hex(hack_data.tell())}! {DEFAULT_PATCHING_FAIL_MESSAGE}")
                    else:
                        print("    Custom Block is type Normal. Grounding the mainframe...")
                    if is_script_block:
                        hack_data.read(1) # skip something i forgot here
                    elif one & 32 != 0:
                        hack_data.read(1) # skip collider type i think
                    block_id = decrypt_short(hack_data)
                    hack_data.read(0xBFE)
                    if is_multiblocks:
                        print("    Custom Block is flagged as MULTIBLOCK!")
                        hack_data.read(5)
                        multiblocks.append(block_id)
                    if contains_flags != 0:
                        print("    Custom Block has world inside! Placing the ball in the orange box...")
                        if contains_flags & 0b100 != 0:
                            dimensional = 1
                            for _ in range(3):
                                dimensional *= decrypt_short(hack_data)
                            hack_data.read(dimensional * 2)
                        if contains_flags & 0b10 != 0:
                            cfg_amount = decrypt_short(hack_data)
                            for _ in range(cfg_amount):
                                kind_of_wire = decrypt_short(hack_data)
                                if kind_of_wire <= 0x4FF:
                                    hack_data.read(6 + (kind_of_wire // 0x100))
                                elif kind_of_wire <= 0x5FF:
                                    hack_data.read(18)
                                else: # assuming everything thats not a valid type is string
                                    hack_data.read(6)
                                    hack_data.read(decrypt_char(hack_data))
                        if contains_flags & 0b1 != 0:
                            hack_data.read(decrypt_short(hack_data) * 24)
                else:
                    print("Block type: Custom Block Multipart // Hacking into custom block multipart...")
                    flag0 = [one & 32 != 0, seven == 2, three & 0x10 != 0]
                    if flag0[0] or flag0[1]:
                        hack_data.read(1)
                    if flag0[2]:
                        hack_data.read(1)
                    hack_data.read(0xC04)
            else:
                raise Exception(f"Chunk type reading error at {hex(chunk_before)}! {DEFAULT_PATCHING_FAIL_MESSAGE}")
            chunk_after = hack_data.tell()
            hack_data.seek(chunk_before)
            hack_data.write(bytes([one & 0b10111111, three & 0b10111111]))
            hack_data.seek(chunk_after)
        print("Successful hacker.")
    else:
        print("Game empty. Successful hacker.")

def hollywood_1911():
    link = input("Enter Game Link to hack (https://play.fancade.com/ can be omitted): ")
    link = hack_filename_from_game_link(link)
    if link is None:
        print("Invalid link entered.")
        return True
    file_data = hack_fancade_server_for_game_data(link)
    print("Decrypting...")
    file_data = game_decrypt(file_data)
    hack_fancade_game_data_for_1337_access(file_data)
    print("Encrypting...")
    file_data = game_encrypt(file_data)
    print("Saving file...")
    with open(link, "wb") as f:
        f.write(file_data.read())
        f.close()
    print("Remember: To import the game to Fancade, you must put the saved game file in a zip file. This was inserted to prevent kids from asking this.")
    return False

print("Fancade Game Downloader hack 31337 version")
print(" created using `hollywood`")
print("imagine music is https://youtube.com/watch?v=e2CIvm1TiaQ")
while hollywood_1911():
    pass
