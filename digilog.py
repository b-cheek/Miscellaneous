import datetime
import math
import os
import sys
import time

font_aspect_ratio = 2.5 # how to adjust pixel clock to fit font aspect ratio? idk
clock_radius = 10 # Direction from centerpoint on each side; radius of 10 equals diameter of 21 so clock is centered
clock_diameter = clock_radius*2+1
hour_hand_ratio = 0.3
minute_hand_ratio = 0.8
second_hand_ratio = 0.9
hour_hand_len = round(hour_hand_ratio*clock_radius)
minute_hand_len = round(minute_hand_ratio*clock_radius)
second_hand_len = round(second_hand_ratio*clock_radius)

# Use point slope form to trace line on pixel clock
# y - y1 = m(x-x1) (x1, y1 are 0,0 at center of clock)
# Check points on horizontal and vertical rays
# Horizontal (y=n): n = m(x) -> x = n/m
# Vertical (x=n): y = mn
def trace_hand(clock_pixels, clock_radius, hand_x, hand_y, value):
    if hand_x == 0:
        hand_slope = sys.maxsize
    else: hand_slope = hand_y/hand_x

    # Vertical rays (in range of hand)
    for x in range(round(min(0, hand_x)), round(max(0, hand_x))):
        # Find intersection with hand
        write_hand_num(clock_pixels, round(clock_radius-hand_slope*x), clock_radius+x, value) # Note that the difference from radius point is negative since 2d array y works from top to bottom
        # clock_pixels[round(clock_radius-hand_slope*x)][clock_radius+x] = True # Note that the difference from radius point is negative since 2d array y works from top to bottom
        # print(round(clock_radius-hand_slope*x), clock_radius+x)

    # Vertical rays (in range of hand)
    for y in range(round(min(0, hand_y)), round(max(0, hand_y))):
        # Find intersection with hand
        write_hand_num(clock_pixels, clock_radius-y, round(clock_radius+y/hand_slope), value)
        # clock_pixels[clock_radius-y][round(clock_radius+y/hand_slope)] = True 
        # print(clock_radius-y, (round(clock_radius+y/hand_slope))) # minus used again for same reason

def write_hand_num(clock_pixels, num_y, num_x, value): # x and y are in this order when indexing 2d arrays
    if len(value)==1:
        clock_pixels[num_y][num_x] = value
        return

    val_radius = len(value)//2
    write_pos = num_x-val_radius
    for pos in range(write_pos, write_pos+len(value)):
        if pos not in range(0, clock_diameter) or num_y not in range(0, clock_diameter):
            # print("pos out of range")
            return
        if clock_pixels[num_y][pos] != " ":
            # print(value, "overlap with", clock_pixels[num_y][pos])
            return
    for char in value:
        clock_pixels[num_y][write_pos] = char
        write_pos += 1

def print_clock(clock_pixels):
    for i in clock_pixels:
        for j in i:
            print(j, end="")
        print("")

def update_time():
    clock_pixels = [[" "]*clock_diameter for _ in range(clock_diameter)]
    # Find angle of each hand on the clock
    now = datetime.datetime.now()
    last_12 = min(
        now.replace(hour=0, minute = 0, second = 0),
        now.replace(hour=12, minute = 0, second = 0)
    )
    seconds_since_12 = (now-last_12).total_seconds() + now.microsecond/1000000
    seconds_since_hour = (now-now.replace(minute=0, second=0)).total_seconds() + now.microsecond/1000000
    seconds_since_minute = (now-now.replace(second=0)).total_seconds() + now.microsecond/1000000

    hour_angle = seconds_since_12/43200*2*math.pi # % of half day complete * 2pi (radians in circle)
    minute_angle = seconds_since_hour/3600*2*math.pi # % of hour complete * 2pi (radians)
    second_angle = seconds_since_minute/60*2*math.pi # % of minute complete * 2pi

    hour_end_x = hour_hand_len*math.sin(hour_angle)
    hour_end_y = hour_hand_len*math.cos(hour_angle)

    minute_end_x = minute_hand_len*math.sin(minute_angle)
    minute_end_y = minute_hand_len*math.cos(minute_angle)

    second_end_x = second_hand_len*math.sin(second_angle)
    second_end_y = second_hand_len*math.cos(second_angle)

    # print(second_end_x, second_end_y)
    # print(seconds_since_minute)

    trace_hand(clock_pixels, clock_radius, hour_end_x, hour_end_y, str(now.hour%12))
    trace_hand(clock_pixels, clock_radius, minute_end_x, minute_end_y, str(now.minute))
    trace_hand(clock_pixels, clock_radius, second_end_x, second_end_y, str(now.second))
    clock_pixels[clock_radius][clock_radius] = "X"
    print_clock(clock_pixels)

update_count = 0
while(True):
    os.system('cls')
    # print("Update count:", update_count)
    update_time()
    update_count += 1
    time.sleep(0.1)