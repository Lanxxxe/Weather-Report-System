import time, pygame, datetime


def run_program():
    # Your program logic goes here
    print("Time being played: " + str(datetime.datetime.now().strftime("%I:%M %p")))
    pygame.mixer.init()
    pygame.mixer.music.load('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\weather.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def wait_until_next_interval():
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second

    # Calculate the remaining time until the next 30-minute interval
    minutes_remaining = 5 - ((minutes + 1)% 5)
    seconds_remaining = 60 - seconds

    # Check if the current time is close to the next hour boundary
    if minutes_remaining == 0 and seconds_remaining < 60:
        minutes_remaining = 5

    # Convert the remaining time to seconds
    total_seconds = (minutes_remaining * 60) + seconds_remaining

    # Wait until the next interval
    time.sleep(total_seconds)

# Example usage
print("Time Runned: " + str(datetime.datetime.now().strftime("%I:%M %p")))
while True:
    wait_until_next_interval()
    run_program()