import random
import cv2

MIN_CLICK_LEN = 100
MAX_CLICK_LEN = 200

WIDTH_MIN_OFFSET = 0.41
WIDTH_MAX_OFFSET = 0.53
HEIGHT_MIN_OFFSET = 0.07
HEIGHT_MAX_OFFSET = 0.12

BUY_MIN_X_OFFSET = 0.02
BUY_MAX_X_OFFSET = 0.2
BUY_MIN_Y_OFFSET = 0.01
BUY_MAX_Y_OFFSET = 0.07

def get_device(devices):
    for device in devices:
        try:
            device.shell('echo yeet')
            return device
        except:
            print('Device offline, trying next device...')

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

def get_rand_offsets(width, height):
    result = [float(width) * random.uniform(WIDTH_MIN_OFFSET, WIDTH_MAX_OFFSET), float(height) * random.uniform(HEIGHT_MIN_OFFSET, HEIGHT_MAX_OFFSET)]
    return result

def get_rand_buy_offsets(width, height):
    result = [float(width) * random.uniform(BUY_MIN_X_OFFSET, BUY_MAX_X_OFFSET), float(height) * random.uniform(BUY_MIN_Y_OFFSET, BUY_MAX_Y_OFFSET)]
    return result

def get_adb_click_str(x, y, click_len):
    return 'input touchscreen swipe ' + str(x) + ' ' + str(y) + ' ' + str(x) + ' ' + str(y) + ' ' + str(click_len)

def get_rand_click_length():
    return random.randrange(MIN_CLICK_LEN, MAX_CLICK_LEN)