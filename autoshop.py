import time
import random
import utils
import keyboard

SCREENCAP_PATH = './screenshots/screen.png'
REFRESH_CONFIRM_PATH = './screenshots/refresh_confirm.png'

SHOP_ITEM_CONFIDENCE = 0.15
CONFIRM_CONFIDENCE = 0.30
REFRESH_CONFIRM_CONFIDENCE = 0.60

#TODO Remove x and y from parameters and pass coordinates instead
# device: device being operated on
# x, y: x and y coordinates of the button to be clicked
# confirm_button_path: path to the image containing the button to be checked for
# offset_id: id for getting random offsets based on button being clicked
# confidence: required confidence for image to pass
def click_loop(device, x, y, confirm_button_path, offset_id, confidence):
    x_offset, y_offset = utils.get_rand_offsets(device, offset_id)

    #Get random click length
    click_len = utils.get_rand_click_length()

    #Click on buy button
    device.shell(utils.get_adb_swipe_str(x + x_offset, y + y_offset, x + x_offset, y + y_offset, click_len))

    #Wait for screen to appear and take new screenshot
    time.sleep(random.uniform(0.25, 0.75))
    utils.get_screencap(device, 'screen.png')

    #Look for confirm button
    return utils.compare_images(confirm_button_path, SCREENCAP_PATH, confidence)

def refresh_shop(device):
    confirm_coords = None

    while not confirm_coords:
        confirm_coords = click_loop(device, 0, 0, REFRESH_CONFIRM_PATH, 2, REFRESH_CONFIRM_CONFIDENCE)

    x, y = confirm_coords    

    #Loop while the confirm button is still on the screen
    while confirm_coords:
        confirm_coords = click_loop(device, x, y, REFRESH_CONFIRM_PATH, 3, CONFIRM_CONFIDENCE)

def parse_shop(device):
        has_scrolled = False

        while keyboard.is_pressed('q') == False:
            if has_scrolled:
                scroll_len = utils.get_rand_scroll_length()
                scroll_coords = utils.get_rand_scroll(device, True)

                print('scrolling from (' + str(int(scroll_coords[0])) + ', ' + str(int(scroll_coords[2])) + ') to (' + str(int(scroll_coords[0])) + ', ' + str(int(scroll_coords[3])) + ')')

                device.shell(utils.get_adb_swipe_str(scroll_coords[0], scroll_coords[1], scroll_coords[2], scroll_coords[3], scroll_len))
                time.sleep(random.uniform(0.25, 0.5))

            utils.get_screencap(device, 'screen.png')

            #Look for covenants first, then mystics
            time.sleep(random.uniform(0.4, 0.75))

            for i in range(2):
                if i == 0:
                    image_path = './screenshots/covenant.png'
                    confirm_button_path = './screenshots/covenant_confirm.png'
                else:
                    image_path = './screenshots/mystic.png'
                    confirm_button_path = './screenshots/mystic_confirm.png'
 

                #Get coordinates for valid items in shop
                coords = utils.compare_images(image_path, SCREENCAP_PATH, SHOP_ITEM_CONFIDENCE)

                #Check if there is a valid item
                if not coords:
                    continue
                
                x, y = coords
                confirm_coords = None

                #Loop until the confirm button is found
                while not confirm_coords:
                    confirm_coords = click_loop(device, x, y, confirm_button_path, 0, CONFIRM_CONFIDENCE)

                x, y = confirm_coords

                #Loop until confirm button is clicked
                while confirm_coords:
                    confirm_coords = click_loop(device, x, y, confirm_button_path, 1, CONFIRM_CONFIDENCE)
                
                time.sleep(random.uniform(1.0, 1.5))
            
            if has_scrolled:
                refresh_shop(device)
                has_scrolled = False
            else:
                has_scrolled = True