print("loading libraries...")
import pygame
pygame.init()
import glob
import os
print("loading opencv...")
import cv2
print("loading numpy...")
import numpy as np
print("loading model...")
import model as m
print("loading data...")
import data
print("<STARTING-DEBUG>")

screen_width = 640 * 2
screen_height = 700
clock = pygame.time.Clock()
center = [screen_width / 2, screen_height / 2]
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("DEBUG")

flag = True
file_list = glob.glob("processed_temp/*png")
file_index = 0
image_path = None
mask_path = None
data_path = None
model = m.create_model()
model.load_weights("brain")

letter_font = pygame.font.Font("freesansbold.ttf", 26)
skip = False
while flag:
    last_key = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                last_key = "Left"
            elif event.key == pygame.K_RIGHT:
                last_key = "Right"
            elif event.key == pygame.K_d:
                print("image", file_index, "deleting...")
                if (os.path.isfile(image_path) == True) and (os.path.isfile(mask_path) == True) and (os.path.isfile(data_path) == True):
                    r_image_path = image_path
                    r_mask_path = mask_path
                    r_data_path = data_path
                    skip = True

                image_path = None

    if (last_key in ["Left", "Right"]) or image_path == None:
        delta = 1

        if last_key == "Left":
            delta = -1

        while file_index >= 0 and file_index < 9999999:
            file_index += delta
            file_index = abs(file_index)
            image_path = "temp/frame_" + str(file_index) + ".png"
            mask_path = "processed_temp/frame_" + str(file_index) + ".png"
            data_path = "processed_temp/data_" + str(file_index) + ".txt"
            if (os.path.isfile(image_path) == True) and (os.path.isfile(mask_path) == True) and (os.path.isfile(data_path) == True):
                # print("image path valid")
                break

    image = pygame.image.load(image_path)
    mask = pygame.image.load(mask_path)

    image = pygame.transform.scale_by(image, 3)
    mask = pygame.transform.scale_by(mask, 2)

    output_data = data.read_output(data_path)
    # print(file_index, "human", output_data)

    input_list = [
        data.read_input(image_path)
    ]

    result = model.predict(
        np.array(input_list, dtype=np.float32),
        verbose=0,
    )[0]

    result = list(map(lambda x: round(x, 2), result))

    # print("tensorflow", result)

    if skip:
        os.remove(r_image_path)
        os.remove(r_mask_path)
        os.remove(r_data_path)
        print("DELETING", r_image_path)
        print("DELETING", r_mask_path)
        print("DELETING", r_data_path)
        skip = False

    screen.fill((0, 0, 0))

    screen.blit(image, (0, 0))
    screen.blit(mask, (640, 0))

    human_name = letter_font.render("human", True, (255, 255, 255))
    screen.blit(human_name, (50, 550))
    human = letter_font.render(str(output_data), True, (255, 255, 255))
    screen.blit(human, (50, 600))

    machine_name = letter_font.render("machine", True, (255, 255, 255))
    screen.blit(machine_name, (900, 550))
    tf_m = letter_font.render(str(result), True, (255, 255, 255))
    screen.blit(tf_m, (900, 600))

    file_number = letter_font.render("image " + str(file_index), True, (255, 255, 255))
    screen.blit(file_number, (600, 600))

    clock.tick(30)
    pygame.display.update()

pygame.quit()
quit()