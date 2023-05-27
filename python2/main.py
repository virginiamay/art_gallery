#VIRGINIA LYNCH

#######################################################################################

import pygame
import os
import pathlib

pygame.init()

scale = 1

#SCREEN SIZE
screen_width = 612 * scale
screen_height = 408 * scale
screen = pygame.display.set_mode((screen_width, screen_height))

#MAIN LIST: room_name = total_costumes, painting_position
#ROOMS_LIST: room_index = room_name

main_list = [("green",
              [(2, (0.051, 0.27)),
               (2, (0.345, 0.21)),
               (2, (0.715, 0.27))]),
             ("gray",
              [(2, (0.12, 0.2)),
               (2, (0.14, 0.55)),
               (2, (0.41, 0.33)),
               (2, (0.71, 0.18)),
               (2, (0.725, 0.55))]),
             ("red",
              [(2, (0.12, 0.22)),
               (2, (0.41, 0.22)),
               (2, (0.71, 0.22))])]

#ROOM NAMES FROM MAIN_LIST 
rooms_list = [room_name[0] for room_name in main_list]

#SET STARTING ROOM
starting_room = rooms_list[1]

print("MAIN_LIST", main_list)
print("ROOMS_LIST", rooms_list)

#######################################################################################

image_directory = pathlib.Path().resolve()

#GET IMAGE PATH
def get_image_path(image_name): 
    return os.path.join(image_directory, (image_name + ".png"))

#GET PAINTING NAME
def get_painting_name(room_name, painting_num, costume_num): 
    return room_name + "_" + str(painting_num) + "(" + str(costume_num) + ")"

#GET FRAME NAME
def get_frame_name(room_name, painting_num): return room_name + "_" + str(painting_num)

#######################################################################################

#IMAGE_DICT: image_name = file_name
#COORDS_DICT: image_name = painting_coords
#NUM_PAINTINGS_DICT: room_name = total_paintings

image_dict = {"arrow_left": "arrow_left.png",
              "arrow_right": "arrow_right.png"}
coords_dict = {"arrow_left": (0.033, 0.735),
               "arrow_right": (0.890, 0.735)}
num_paintings_dict = {}

# UPDATE IMAGE_DICT, COORDS_DICT, NUM_PAINTINGS_DICT
for room_info in main_list:
    room_name, painting_info_list = room_info

    image_dict[room_name] = get_image_path("room_" + room_name)
    painting_num = 1

    for painting_info in painting_info_list:
        num_costumes, painting_position = painting_info

        for i in range(num_costumes):
            costume_num = i + 1
            painting_name = get_painting_name(room_name, painting_num, costume_num)

            image_path = get_image_path(painting_name)
            image_dict[painting_name] = image_path
            coords_dict[painting_name] = (painting_position[0], painting_position[1])

            num_paintings_dict[room_name] = painting_num
        
        painting_num = painting_num + 1

for image_name in coords_dict:
    x_pos = int(coords_dict[image_name][0] * screen_width)
    y_pos = int(coords_dict[image_name][1] * screen_height)
    coords_dict[image_name] = x_pos, y_pos

print("IMG_DICT", image_dict)
print("COORDS_DICT", coords_dict)
print("NUM_PAINTINGS_DICT", num_paintings_dict)

#######################################################################################

#COSTUME_NUM_DICT: frame_name = costume_num

costume_num_dict = {}

for image_name in image_dict:

    #IS A PAINTING
    if "(" in image_name:
        frame_name = image_name.split("(")[0]

        if frame_name not in costume_num_dict:
            costume_num_dict[frame_name] = 1

print("COSTUME_NUM_DICT", costume_num_dict)

#######################################################################################

#PAINTING_SIZE_DICT: painting_name = image_name

painting_size_dict = {}

for image_name in image_dict:
    if "(" in image_name:
        painting_name = image_name

        painting_size_dict[painting_name] = (
            int(pygame.image.load(image_dict[painting_name]).get_width() * scale),
            int(pygame.image.load(image_dict[painting_name]).get_height() * scale))

#######################################################################################

#CREATE BACKGROUND SPRITE
background_layer = pygame.sprite.LayeredUpdates()
background = pygame.sprite.Sprite()
background_layer.add(background)

arrow_size = (45 * scale, 45 * scale)

#LEFT ARROW
arrow_left = pygame.sprite.Sprite()
image_name = pygame.image.load(image_dict["arrow_left"]).convert()
arrow_left.image = pygame.transform.scale(image_name, arrow_size)
arrow_left_rect = pygame.Rect(
                    coords_dict["arrow_left"][0],
                    coords_dict["arrow_left"][1],
                    arrow_size[0],
                    arrow_size[1])
#RIGHT ARROW
arrow_right = pygame.sprite.Sprite()
image_name = pygame.image.load(image_dict["arrow_right"]).convert()
arrow_right.image = pygame.transform.scale(image_name, arrow_size)
arrow_right_rect = pygame.Rect(
                    coords_dict["arrow_right"][0],
                    coords_dict["arrow_right"][1],
                    arrow_size[0],
                    arrow_size[1])

#INITAL STATUSES
room_name = starting_room
running = True
update = True

#######################################################################################

#MAIN LOOP
while running:
    
    #EVENTS
    for event in pygame.event.get():

        #CLOSE PROGRAM
        if event.type == pygame.QUIT:
            running = False
        
        #KEY PRESSED
        if event.type == pygame.KEYDOWN:
            
            room_index = rooms_list.index(room_name)

            
            #KEY (A) PRESSED
            if event.key == pygame.K_a:
                if room_index != 0:
                    room_name = rooms_list[room_index - 1]
                    update = True

            #KEY (D) PRESSED
            if event.key == pygame.K_d:
                if room_index != len(rooms_list) - 1:
                    room_name = rooms_list[room_index + 1]
                    update = True
        
        #MOUSE BUTTON DOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
                
            #LEFT MOUSE BUTTON
            if event.button == 1:
                room_index = rooms_list.index(room_name)
                
                #CHECK ARROWS
                #GO LEFT
                if arrow_left_rect.collidepoint(event.pos):
                    if room_index != 0:
                        room_name = rooms_list[room_index - 1]
                        update = True

                #GO RIGHT
                if arrow_right_rect.collidepoint(event.pos):
                    if room_index != len(rooms_list) - 1:
                        room_name = rooms_list[room_index + 1]
                        update = True
                
                #CHECK PAINTINGS
                for frame_name in costume_num_dict:
                    if frame_name.startswith(room_name):
                        painting_name = frame_name + "(" + str(costume_num_dict[frame_name]) + ")"
                        
                        painting_rect = pygame.Rect(
                            coords_dict[painting_name],
                            painting_size_dict[painting_name])                        
                        
                        if painting_rect.collidepoint(event.pos):
                            
                            room_num = rooms_list.index(room_name)
                            painting_num = int(frame_name.split("_")[1])
                            costume_num = costume_num_dict[frame_name]

                            room_info = main_list[room_num]
                            painting_info = room_info[1][painting_num - 1]
                            total_costumes, painting_coords = painting_info

                            #RESET TO 1
                            if costume_num == total_costumes:
                                next_costume_num = 1
                                
                            #INCREASE BY 1
                            else:
                                next_costume_num = costume_num + 1
                            
                            new_painting_name = get_painting_name(room_name, painting_num, next_costume_num)
                            image_dict[new_painting_name] = get_image_path(new_painting_name)
                            costume_num_dict[frame_name] = next_costume_num

                            update = True

    #ROOM OR COSTUME CHANGED
    if update:

        #BACKGROUND IMAGE
        image_name = pygame.image.load(image_dict[room_name]).convert()
        background.image = pygame.transform.scale(
            image_name, 
            (screen_width, 
             screen_height))
        screen.blit(background.image, (0, 0))

        #ADD PAINTINGS
        for i in range(num_paintings_dict[room_name]):
            painting_num = i + 1
            frame_name = get_frame_name(room_name, painting_num)

            painting_name = get_painting_name(room_name, painting_num, costume_num_dict[frame_name])
            
            if painting_name in image_dict:
                image_name = pygame.image.load(image_dict[painting_name]).convert()
                painting = pygame.sprite.Sprite()
                painting.image = pygame.transform.scale(image_name, painting_size_dict[painting_name])

                if painting_name in coords_dict:
                    painting_coords = coords_dict[painting_name]
                    screen.blit(painting.image, painting_coords)        
        #SHOW ARROWS
        room_index = rooms_list.index(room_name)

        if room_index != 0:
            screen.blit(arrow_left.image, coords_dict["arrow_left"])
        if room_index != len(rooms_list) - 1:
            screen.blit(arrow_right.image, coords_dict["arrow_right"])

        #UPDATE DISPLAY
        pygame.display.flip()
        update = False
        
pygame.quit()

#######################################################################################
