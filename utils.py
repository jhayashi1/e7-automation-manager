import random
import cv2

MIN_CLICK_LEN = 100
MAX_CLICK_LEN = 200

MIN_SCROLL_LEN = 50
MAX_SCROLL_LEN = 52

SCROLL_MIN_X_OFFSET = 0.52
SCROLL_MAX_X_OFFSET = 0.81
SCROLL_MIN_Y_OFFSET = 0.13
SCROLL_MAX_Y_OFFSET = 0.96

WIDTH_MIN_OFFSET = 0.41
WIDTH_MAX_OFFSET = 0.53
HEIGHT_MIN_OFFSET = 0.07
HEIGHT_MAX_OFFSET = 0.12

BUY_MIN_X_OFFSET = 0.02
BUY_MAX_X_OFFSET = 0.2
BUY_MIN_Y_OFFSET = 0.01
BUY_MAX_Y_OFFSET = 0.07

REFRESH_MIN_X_OFFSET = 0.07
REFRESH_MAX_X_OFFSET = 0.27
REFRESH_MIN_Y_OFFSET = 0.89
REFRESH_MAX_Y_OFFSET = 0.95

REFRESH_CONFIRM_MIN_X_OFFSET = 0.03
REFRESH_CONFIRM_MAX_X_OFFSET = 0.15
REFRESH_CONFIRM_MIN_Y_OFFSET = 0.01
REFRESH_CONFIRM_MAX_Y_OFFSET = 0.07

def get_device(devices):
    for device in devices:
        try:
            device.shell('echo yeet')
            return device
        except:
            print('Device offline, trying next device...')

def get_resolution(device):
    return device.shell('wm size').split()[-1].split('x')

def get_screencap(device, name):
    image = device.screencap()

    if image == None:
        print('Could not get image, device is probably offline')
        quit()

    with open('./screenshots/' + name, 'wb') as f:
        f.write(image)

def compare_images(image_path, sample_path, confidence):
    image = cv2.imread(image_path)
    sample = cv2.imread(sample_path)

    #Match the two images
    result = cv2.matchTemplate(image, sample, cv2.TM_SQDIFF_NORMED)
    cov_mn,_,cov_mnLoc,_ = cv2.minMaxLoc(result)

    #Don't return any coords if confidence is less than 90%
    if cov_mn > confidence:
        return None

    #Get coords of matched image
    MPx, MPy = cov_mnLoc
    coords = [MPx, MPy]

    return coords

def get_rand_offsets(device, offset_id):
    width, height = get_resolution(device)
    #0 = buy button, 1 = buy confirm button, 2 = refresh button, 3 = refresh confirm button
    offset_arr = offset_id_cases(offset_id)

    result = [float(width) * random.uniform(offset_arr[0], offset_arr[1]), float(height) * random.uniform(offset_arr[2], offset_arr[3])]
    return result

def offset_id_cases(id):
    return {
        0 : [WIDTH_MIN_OFFSET, WIDTH_MAX_OFFSET, HEIGHT_MIN_OFFSET, HEIGHT_MAX_OFFSET],
        1 : [BUY_MIN_X_OFFSET, BUY_MAX_X_OFFSET, BUY_MIN_Y_OFFSET, BUY_MAX_Y_OFFSET],
        2 : [REFRESH_MIN_X_OFFSET, REFRESH_MAX_X_OFFSET, REFRESH_MIN_Y_OFFSET, REFRESH_MAX_Y_OFFSET],
        3 : [REFRESH_CONFIRM_MIN_X_OFFSET, REFRESH_CONFIRM_MAX_X_OFFSET, REFRESH_CONFIRM_MIN_Y_OFFSET, REFRESH_CONFIRM_MAX_Y_OFFSET]
    }[id]

def get_adb_swipe_str(x1, y1, x2, y2, click_len):
    return 'input touchscreen swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(click_len)

def get_rand_click_length():
    return random.randrange(MIN_CLICK_LEN, MAX_CLICK_LEN)

def get_rand_scroll_length():
    return random.randrange(MIN_SCROLL_LEN, MAX_SCROLL_LEN)

def get_rand_scroll(device, is_down):
    width, height = get_resolution(device)
    x_offset = random.uniform(SCROLL_MIN_X_OFFSET, SCROLL_MAX_X_OFFSET)
    rand_x_offset_offset = x_offset / 10
    avg_y = (SCROLL_MIN_Y_OFFSET + SCROLL_MAX_Y_OFFSET) / 2

    result = [float(width) * x_offset, float(height) * random.uniform(SCROLL_MIN_Y_OFFSET, avg_y - (avg_y / 10)),
    float(width) * (x_offset - (rand_x_offset_offset) + (random.uniform(0.0, rand_x_offset_offset))),
    float(height) * random.uniform(avg_y + (avg_y / 10), SCROLL_MAX_Y_OFFSET)]

    #Change y positions if scrolling down
    if is_down:
        result[1], result[3] = result[3], result[1]

    return result

