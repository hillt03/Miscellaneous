from imagesearch import *
import sys
import time as t
from RepeatedTimer import RepeatedTimer
from time import sleep


def move_and_click(image, precision=0.8, display_unavailable=True, sleep_before=0, sleep_after=0):
    """
    Scans for an image, moves to it, and clicks on it if available.
    Returns True if image exists, otherwise returns False.
    """
    sleep(sleep_before)
    image_available = False
    pos = imagesearch(image, precision=precision)
    if pos[0] != -1:
        # print(f"position of {image}: {pos[0]} {pos[1]}")
        # left click image at its found position after tasking 0.2s to reach the image
        sleep(0.5)
        click_image(image, pos, "left", 0.2, 1)
        sleep(sleep_after)
        image_available = True
    else:
        image_available = False
        if display_unavailable:
            print(f"{image} not available.")
    sleep(sleep_after)
    return image_available


def mouse_move_and_click_coords(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


def image_exists(image, precision=0.8):
    pos = imagesearch(image, precision=precision)
    return pos[0] != -1


class image_wait_retry_exceeded(Exception): pass

def wait_for_image_then_click(image, precision=0.8, sleep_before_searching=0, retry_interval=4, max_retries=3, sleep_before_click=0, sleep_after_click=0):
    counter = 1
    sleep(sleep_before_searching)
    while not image_exists(image, precision):
        if counter == max_retries:
            raise image_wait_retry_exceeded("Image: " + image)
        sleep(retry_interval)
        counter += 1
    move_and_click(image, precision, sleep_before=sleep_before_click, sleep_after=sleep_after_click)



def reset_cursor():
    pyautogui.moveTo(944, 567)


def collect_rest_xp_initial():
    path = "images/restxp/"
    initial_xp = move_and_click(path + "claimrestxpinitial.png", precision=0.5)
    if initial_xp:
        sleep(3)


def collect_rest_xp():
    path = "images/restxp/"
    xp = move_and_click(path + "restxp.png", precision=0.7)
    if xp:
        sleep(1)
        move_and_click(path + "claimxp.png")
    sleep(3)


def recruit():
    path = "images/recruit/"
    recruit = move_and_click(path + "recruit_available.png", precision=0.9)
    if recruit:
        sleep(1)
        # TODO: Check the normal (10 times(s))

        # Check the normal (1 time(s))
        if image_exists(path + "1available.png"):
            click_dont_show = True
            for i in range(9):
                if image_exists(path + "not_enough.png"):
                    break
                move_and_click(path + "recruit_normal.png")
                if click_dont_show:
                    move_and_click(path + "dont_show.png")
                    move_and_click(path + "normal_ok.png")
                    click_dont_show = False
                move_and_click(path + "newhero_ok.png", display_unavailable=False)

        # Check the free elite (1 times(s))
        sleep(0.5)
        move_and_click(path + "elite.png")
        if image_exists(path + "free.png"):
            move_and_click(path + "1available_elite.png", precision=0.9)
            sleep(1)
            move_and_click(path + "newhero_ok.png", display_unavailable=False)

        # Check ritual
        move_and_click(path + "ritual.png")
        if image_exists(path + "ritual_free.png"):
            move_and_click(path + "ritual_1available.png")

        # Close the window
        move_and_click(path + "close.png", precision=0.5)
        move_and_click(path + "after_okay.png", display_unavailable=False)
        reset_cursor()
        sleep(2)


def claim_reward_hall():
    path = "images/reward_hall/"
    reward_hall_init_image = path + "reward_hall2.png"

    # Stamina images
    claim_stamina_image = path + "stamina/claim_stamina.png"
    cherry_image = path + "stamina/cherry.png"
    cake_image = path + "stamina/cake.png"
    turkey_image = path + "stamina/turkey.png"
    stamina_images = [cherry_image, cake_image, turkey_image]

    reward_hall = move_and_click(reward_hall_init_image)
    if reward_hall:
        sleep(1)
        # TODO: Bottom claim

        # Claim stamina
        # Todo: check for red circle
        # claim first meal
        move_and_click(claim_stamina_image)
        for image in stamina_images:
            move_and_click(image)
            reward_hall_check_stamina_recharge()

        # Close the window
        move_and_click(path + "close.png")
        reset_cursor()
        sleep(1)


def reward_hall_check_stamina_recharge():
    path = "images/reward_hall/stamina/"
    recharge_image = path + "recharge.png"
    purchase_ok_image = path + "stamina_purchase.png"
    close_recharge_image = path + "close_recharge.png"

    if image_exists(recharge_image):
        move_and_click(close_recharge_image)
        sleep(1)
    else:
        move_and_click(purchase_ok_image, display_unavailable=False)


def level_up_gift():
    path = "images/level_up_gift/"
    claim_image = path + "claim.png"
    level_up_gift_image = path + "level_up_gift.png"
    level_up_close_image = path + "close_level_up_gift.png"

    level_up_gift_available = move_and_click(level_up_gift_image)
    if level_up_gift_available:
        sleep(1)
        while image_exists(claim_image, precision=1):
            move_and_click(claim_image, precision=0.8)
            sleep(0.5)
        move_and_click(level_up_close_image)
        sleep(1)


def scan_for_multiple_images(image_paths, looped=True, sleep_time=5):
    """
    Scans for multiple images in a loop, returns the first image path that's found
    image_paths: list of image paths you want to scan for
    looped: set to False to disable looping
    Returns False if looped disabled and no image found, returns image path if one is found.
    """
    searching = True
    img = region_grabber((0, 0, scr_res["x"], scr_res["y"]))
    if looped:
        while searching:
            for image in image_paths:
                img_coords = imagesearcharea(
                    image, 0, 0, scr_res["x"], scr_res["y"], 0.8, img
                )
                if img_coords[0] != -1:
                    searching = False
                    return image
            sleep(sleep_time)
    else:
        for image in image_paths:
            img_coords = imagesearcharea(
                image, 0, 0, scr_res["x"], scr_res["y"], 0.8, img
            )
            if img_coords[0] != -1:
                return image
        return False


def elite_stage_automation():
    path = "images/stage/"
    stage_init_image = path + "stage.png"

    elite_new_image = path + "elite/elite_new.png"
    left_arrow_image = path + "elite/left_arrow.png"
    ok_image = path + "elite/ok.png"
    stage_exit_image = path + "elite/stage_exit.png"
    clear_normal_image = path + "elite/clear_normal.png"
    victory_image = path + "elite/victory.png"
    defeat_image = path + "elite/defeat.png"
    possibilities = [victory_image, defeat_image]

    grinding = True

    while grinding:
        init = move_and_click(stage_init_image)
        if init:
            counter = 0
            while not image_exists(elite_new_image):
                if counter == 6:
                    print("Counter exceeded, stopping.")
                    move_and_click(stage_exit_image)
                    sleep(1)
                    break
                move_and_click(left_arrow_image, precision=0.5)
                sleep(1.3)
                counter += 1
            sleep(1)
            move_and_click(elite_new_image)
            sleep(1.4)
            mouse_move_and_click_coords(x=1351, y=726)  # Clicks elite "Challenge"
            sleep(1.3)
            if image_exists(clear_normal_image, 0.7):
                print(
                    "###########################################################\n"
                    + "You must clear normal stages with 3 stars before continuing elite challenges.\n"
                    + "###########################################################"
                )
                print("Attempting normal challenge...")
                mouse_move_and_click_coords(x=1361, y=594)  # Clicks normal "Challenge"

            result = scan_for_multiple_images(possibilities, sleep_time=3)
            if result == victory_image:
                print("Battle won.")
            else:
                print("Battle lost. Stopping this task.")
                grinding = False
            move_and_click(ok_image)
            wait_for_image_then_click(stage_exit_image, sleep_after_click=1)


def achievement():
    path = "images/achievement/"
    achievement_image = path + "achievement.png"
    claim = path + "claim.png"
    close = path + "close.png"

    challenge = path + "challenge.png"
    misc = path + "misc.png"
    tabs = [challenge, misc]

    achievement_available = move_and_click(achievement_image)
    if achievement_available:
        move_and_click_recursive(claim)
        for tab in tabs:
            move_and_click(tab)
            move_and_click_recursive(claim)
    move_and_click(close)
    sleep(1)




def move_and_click_recursive(image_path, sleep_time=0.5):
    """Click on an image until it can't be found."""
    claiming = True
    while claiming:
            result = move_and_click(image_path, display_unavailable=False)
            if result == False:
                claiming = False
            sleep(sleep_time)

def realm():
    pass


def arena():
    path = "images/arena/"
    arena_image = path + "arena.png"
    recommended_image = path + "recommended.png"
    ok_image = path + "ok.png"
    ok2_image = path + "ok2.png"
    salute_image = path + "salute.png"

    grinding = True
    arena_available = move_and_click(arena_image)
    if arena_available:
        sleep(1)
        while grinding:
            move_and_click(salute_image, display_unavailable=False)
            move_and_click(recommended_image)
            while not image_exists(ok_image):
                sleep(5)
            move_and_click(ok_image)
            sleep(6)
            move_and_click(ok2_image, display_unavailable=True) #TODO:False
            while not image_exists(recommended_image):
                sleep(3)
    # Issues: Recommended not always available, need OCR. Divide BR, if pos proceed? If OCR works..

def toil_checker():
    """We'll be running this every 30 seconds to see if we need to restart the bot."""
    images_to_look_for = []
    raise NotImplemented()


if __name__ == "__main__":


    # Screen resolution
    global scr_res
    scr_res = {"x": 1920, "y": 1080}
    enabled = False

    tasks = {
        "rest_xp_initial": {
            "image": "images/restxp/claimrestxpinitial.png",
            "function": collect_rest_xp_initial,
            "precision": 0.6,
            "description": "collecting rest XP.",
            "enabled": enabled,
            "priority": 0,
            "ignore_scan": False,
        },
        "rest_xp": {
            "image": "images/restxp/restxp.png",
            "function": collect_rest_xp,
            "precision": 0.7,
            "description": "collecting rest XP.",
            "enabled": enabled,
            "priority": 0,
            "ignore_scan": False,
        },
        "achievement": {
            "image": "images/achievement/achievement.png",
            "function": achievement,
            "precision": 0.7,
            "description": "claiming achievement rewards.",
            "enabled": enabled,
            "priority": 0,
            "ignore_scan": False,
        },
        "recruit": {
            "image": "images/recruit/recruit_available.png",
            "function": recruit,
            "precision": 0.9,
            "description": "recruiting heroes.",
            "enabled": enabled,
            "priority": 0,
            "ignore_scan": False,
        },
        "reward_hall": {
            "image": "images/reward_hall/reward_hall2.png",
            "function": claim_reward_hall,
            "precision": 0.9,
            "description": "claiming items from the reward hall.",
            "enabled": enabled,
            "priority": 0,
            "ignore_scan": False,
        },
        "level_up_gift": {
            "image": "images/level_up_gift/level_up_gift.png",
            "function": level_up_gift,
            "precision": 0.8,
            "description": "claiming level up gift(s).",
            "enabled": enabled,
            "priority": 0,
            "ignore_scan": False,
        },
        "elite_stage_automation": {
            "image": "images/stage/stage.png",
            "function": elite_stage_automation,
            "precision": 0.7,
            "description": "completing elite missions until failure.",
            "enabled": True,
            "priority": 0,
            "ignore_scan": True,
        },
        "arena": {
            "image": "images/arena/arena.png",
            "function": arena,
            "precision": 0.8,
            "description": "completing all arena attempts.",
            "enabled": enabled,
            "priority": 0,
            "ignore_scan": False,
        },
    }

    # Tasks that need to be done will be added to the task_queue
    task_queue = []

    # Check each image in the tasks dict to determine if the task is available
    img = region_grabber((0, 0, scr_res["x"], scr_res["y"]))
    for task in tasks.keys():
        if tasks[task]["enabled"] == False:
            print(task + " task is disabled.")
            continue
        img_coords = imagesearcharea(
            tasks[task]["image"],
            0,
            0,
            scr_res["x"],
            scr_res["y"],
            tasks[task]["precision"],
            img,
        )
        if img_coords[0] != -1:
            task_queue.append((tasks[task]["function"], tasks[task]["description"]))

    if not task_queue:
        print("There are no tasks available, closing.")
        sys.exit(0)


    #toil = RepeatedTimer(30, toil_checker) # Unimplemented


    # for task, description in task_queue:
    #    print("Task :: " + description)
    total_tasks = len(task_queue)
    for task, description in task_queue:
        print("Current task: " + description)
        task()

        total_tasks -= 1
        print("Task complete. " + str(total_tasks) + " task(s) remaining.")
