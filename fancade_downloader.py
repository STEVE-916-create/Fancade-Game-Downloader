# Fancade Downloader hack
# go brag about this in r/masterhacker
# 2025 version

import zlib, requests, os, io

VERBOSE = False
FIREBASE_HACK_1337 = "https://firebasestorage.googleapis.com/v0/b/fancade-live.appspot.com/o"
DEFAULT_PATCHING_FAIL_MESSAGE = "Please report this bug to me (STEVE). Tell me the game link and this exception message, so that I know what to look for."

def verbo(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

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
    print("Encrypting...")
    hack_data.seek(0)
    return io.BytesIO(zlib.compress(hack_data.read()))
def game_decrypt(hack_data):
    print("Decrypting...")
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
    name = list((name * 4).encode())
    for _ in range(2):
        name[1] *= name[3]
        name[3] *= name[4]
        name[2] *= name[1]
        name[3] *= name[2]
        name[4] *= name[2]
        name[1] *= name[4]
        name[2] *= name[3]
        name[4] *= name[1]
    return str(name[1] % 128) + "." + str(name[2] % 128) + "." + str(name[3] % 128) + "." + str(name[4] % 128)

# newer parser now yay
def hack_fancade_game_data_for_1337_access(hack_data):
    verbo("Game Information:")
    format_version = decrypt_short(hack_data)
    verbo(f"    Format Version: {format_version}")
    game_title = decrypt_str(hack_data)
    verbo(f"    Title: {game_title}")
    fancade_username = decrypt_str(hack_data)
    verbo(f"    By: {fancade_username}")
    game_description = decrypt_str(hack_data)
    verbo(f"    Description: {game_description}")
    custom_block_id_offset = decrypt_short(hack_data)
    objects = decrypt_short(hack_data)
    levels = []
    custom_blocks = []
    groups = {}
    print(f"Creator's IP Address: {hack_into_computer_by_user(fancade_username)}")
    print(f"Brute force counting objects...")
    if objects > 0:
        verbo(f"Counted {objects} objects! Hacking objects...")
        for _ in range(objects):
            chunk_before = hack_data.tell()
            hax = hex(chunk_before)
            verbo(f"Hacking object information at {hax}...:")
            hacking, exploiting = decrypt_char(hack_data), decrypt_char(hack_data)
            contains_type = exploiting & 0b00010000 != 0
            call_it_from_now_on = "Object"
            object_type = "UNKNOWN"
            if contains_type:
                object_type = decrypt_char(hack_data)
                if object_type == 0:
                    object_type = "BLOCK NORMAL"
                    call_it_from_now_on = "Custom Block"
                elif object_type == 1:
                    object_type = "BLOCK PHYSICS"
                    call_it_from_now_on = "Custom Block"
                elif object_type == 2:
                    object_type = "BLOCK SCRIPT"
                    call_it_from_now_on = "Script Block"
                elif object_type == 3:
                    object_type = "LEVEL"
                    call_it_from_now_on = "Level"
                else:
                    object_type = "UNKNOWN"
                verbo(f"    Object type: {object_type}")
                verbo(f"    (this Object will be called a {call_it_from_now_on} after this line)")
            contains_name = exploiting & 0b00001000 != 0
            object_name = None
            if contains_name:
                object_name = decrypt_str(hack_data)
                verbo(f"    {call_it_from_now_on} name: \"{object_name}\"")
            contains_misc1 = exploiting & 0b00000100 != 0
            if contains_misc1:
                hack_data.read(1)
            contains_misc2 = exploiting & 0b00000010 != 0
            if contains_misc2:
                hack_data.read(4)
            what_does_blue_mean = exploiting & 0b00000001 != 0
            if object_type == "LEVEL":
                if what_does_blue_mean:
                    verbo(f"    Level color: NOT BLUE!!!")
                    hack_data.read(1)
                else:
                    verbo(f"    Level color: BLUE!!!")
            else:
                if what_does_blue_mean:
                    verbo(f"    {call_it_from_now_on} has color byte (????? im confusion)")
                    hack_data.read(1)
            contains_phytype = hacking & 0b00100000 != 0
            if contains_phytype:
                hack_data.read(1)
            its_called_group_not_multiblock_ok = hacking & 0b00010000 != 0
            group_id = None
            if its_called_group_not_multiblock_ok:
                group_id = decrypt_short(hack_data)
                hack_data.read(3)
                verbo(f"    {call_it_from_now_on} is assigned a \"group\"! Group ID: {group_id}")
            contains_voxdata = hacking & 0b00001000 != 0
            if contains_voxdata:
                verbo(f"    {call_it_from_now_on} contains voxel data! Placing the ball in the orange box...")
                hack_data.read(0xC00)
            contains_blocks = hacking & 0b00000100 != 0
            if contains_blocks:
                verbo(f"    {call_it_from_now_on} contains block data! Bragging in r/masterhacker...")
                x, y, z = decrypt_short(hack_data), decrypt_short(hack_data), decrypt_short(hack_data)
                verbo(f"        {call_it_from_now_on} block data size: {x}x{y}x{z}")
                hack_data.read(x * y * z * 2)
            contains_configs = hacking & 0b00000010 != 0
            if contains_configs:
                verbo(f"    {call_it_from_now_on} contains block configurations! Programming Arduino ESP32...")
                amount = decrypt_short(hack_data)
                verbo(f"        {call_it_from_now_on} block configuration amount: {amount}")
                for _ in range(amount):
                    hack_data.read(1) # config index
                    cfg_type = decrypt_char(hack_data)
                    hack_data.read(6) # config target block position
                    if cfg_type == 1:
                        hack_data.read(1) # byte
                    elif cfg_type == 2:
                        hack_data.read(2) # short
                    elif cfg_type == 3:
                        hack_data.read(4) # int
                    elif cfg_type == 4:
                        hack_data.read(4) # float
                    elif cfg_type == 5:
                        hack_data.read(12) # 3 floats (4 bytes each)
                    else: # everything else is valued string
                        hack_data.read(decrypt_char(hack_data))
            contains_wires = hacking & 0b00000001 != 0
            if contains_wires:
                verbo(f"    {call_it_from_now_on} contains wires! Inserting Flipper Zero...")
                amount = decrypt_short(hack_data)
                verbo(f"        {call_it_from_now_on} wire amount: {amount}")
                hack_data.read(amount * 24)
            chunk_after = hack_data.tell()
            hack_data.seek(chunk_before)
            hack_data.write(bytes([hacking & 0b00111111, exploiting & 0b00111111]))
            hack_data.seek(chunk_after)
            verbo(f"This {call_it_from_now_on} object has been hacked by the skid who is using this program right now.")
            if object_type[0:5] == "LEVEL":
                if object_name is None:
                    object_name = "[no name]"
                levels.append(object_name)
            elif object_type[0:5] == "BLOCK":
                if object_name is None:
                    object_name = "[no name]"
                else:
                    if group_id is not None:
                        groups[group_id] = object_name
                custom_blocks.append([object_name, group_id])
        print("Successful hacker.")
        print("All this but summarized:")
        print(f"    Format Version: {format_version}")
        print(f"    Title: {game_title}")
        print(f"    By: {fancade_username}")
        print(f"    Description: {game_description}")
        print(f"    Custom Block ID Offset: {custom_block_id_offset}")
        print(f"    Number of objects: {objects}")
        print(f"    Parser start address: 0x0")
        print(f"    Parser end address: {hex(hack_data.tell())}")
        hack_data.read()
        print(f"    File end address: {hex(hack_data.tell())}")
        print(f"    Levels ({len(levels)}):")
        for i in range(len(levels)):
            print(f"        {i + 1}. {levels[i]}")
        print(f"    Custom Blocks ({len(custom_blocks)}):")
        for i in range(len(custom_blocks)):
            object_name, group_id = custom_blocks[i][0], custom_blocks[i][1]
            if object_name == "[no name]":
                if group_id is not None:
                    if groups.get(group_id) is not None:
                        object_name = f"[a block thats part of \"{groups[group_id]}\"]"
            print(f"        {i + 1}. {object_name}")
    else:
        print("Game empty. Successful hacker.")

def hollywood_1911():
    link = input("Enter Game Link to hack (https://play.fancade.com/ can be omitted): ")
    link = hack_filename_from_game_link(link)
    if link is None:
        print("Invalid link entered.")
        return True
    file_data = hack_fancade_server_for_game_data(link)
    file_data = game_decrypt(file_data)
    hack_fancade_game_data_for_1337_access(file_data)
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
