import time

loading_animation = ["⠠", "⠤", "⠴", "⠶", "⠷", "⠿"]
animation_index = 0

try:
    while True:
        print(f"\r{loading_animation[animation_index]}", end="", flush=True)
        animation_index = (animation_index + 1) % len(loading_animation)
        time.sleep(0.2)  # Adjust sleep duration as needed
except KeyboardInterrupt:
    print("\nLoading stopped.")