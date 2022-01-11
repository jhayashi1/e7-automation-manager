import time
import random
import utils
import keyboard

SCREENCAP_PATH = './screenshots/screen.png'

def click_loop(device, x, y, width, height, confirm_path, is_buy_confirm):
    #Get random offsets based if the confirm menu is currently displayed
    if is_buy_confirm:
        x_offset, y_offset = utils.get_rand_buy_offsets(width, height)
        confidence = 0.30
    else:
        x_offset, y_offset = utils.get_rand_offsets(width, height)
        confidence = 0.40

    #Get random click length
    click_len = utils.get_rand_click_length()

    #Click on buy button
    device.shell(utils.get_adb_click_str(x + x_offset, y + y_offset, click_len))

    #Wait for screen to appear and take new screenshot
    time.sleep(random.uniform(0.25, 0.75))
    utils.get_screencap(device, 'screen.png')

    #Look for confirm button
    return utils.compare_images(confirm_path, SCREENCAP_PATH, confidence)

def refresh_shop(device):
    pass

def parse_shop(device):
        resolution = device.shell('wm size').split()[-1].split('x')
        width, height = resolution[:2]
        utils.get_screencap(device, 'screen.png')
        has_scrolled = False

        while keyboard.is_pressed('q') == False:
            #Look for covenants first, then mystics
            for i in range(2):
                if i == 0:
                    image_path = './screenshots/covenant.png'
                    confirm_path = './screenshots/covenant_confirm.png'
                else:
                    image_path = './screenshots/mystic.png'
                    confirm_path = './screenshots/mystic_confirm.png'


                #Get coordinates for valid items in shop
                coords = utils.compare_images(image_path, SCREENCAP_PATH, 0.40)

                #Check if there is a valid item
                if not coords:
                    continue

                #Get x and y values
                x, y = coords
                confirm_coords = None
                
                #Loop until the confirm button is found
                while not confirm_coords:
                    confirm_coords = click_loop(device, x, y, width, height, confirm_path, False)
                
                #Get x and y values
                buy_x, buy_y = confirm_coords

                while confirm_coords:
                    confirm_coords = click_loop(device, buy_x, buy_y, width, height, confirm_path, True)
                
                if has_scrolled:
                    refresh_shop(device)