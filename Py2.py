        print("Path clear. Normal walking.")
        normal_step()  # Return to normal walking
        crawler.do_action('forward', 1, speed)
        time.sleep(0.2)

def main():
    show_info()
    mode = "manual"
    obstacle_detection_enabled = False
    double_height_enabled = False
    camera_feed_enabled = False
    
    while True:
        if mode == "manual":
            key = readchar.readkey()
            key = key.lower()
            if key in ('wsad'):
                if 'w' == key:
                    if obstacle_detection_enabled:
                        distance = get_ultrasonic_distance()
                        if distance > 0 and distance <= alert_distance:
                            if is_view_blocked():
                                print("Obstacle detected, attempting to step over")
                                high_step()
                            else:
                                crawler.do_action('forward', 1, speed)
                        else:
                            crawler.do_action('forward', 1, speed)
                    else:
                        crawler.do_action('forward', 1, speed)
                elif 's' == key:
                    crawler.do_action('backward', 1, speed)          
                elif 'a' == key:
                    crawler.do_action('turn left', 1, speed)           
                elif 'd' == key:
                    crawler.do_action('turn right', 1, speed)
                sleep(0.05)
                show_info()
            elif key == '0':
                print("Switching to obstacle avoidance mode")
                mode = "obstacle_avoidance"
            elif key == '1':
                obstacle_detection_enabled = not obstacle_detection_enabled
                print(f"Obstacle detection {'enabled' if obstacle_detection_enabled else 'disabled'}")
                if not obstacle_detection_enabled and double_height_enabled:
                    print("Returning to standard stance")
                    normal_step()
                    double_height_enabled = False
            elif key == '2':
                double_height_enabled = not double_height_enabled
                if double_height_enabled:
                    print("Double height and step height enabled")
                    double_height_step()
                else:
                    print("Double height and step height disabled")
                    normal_step()
            elif key == '3':
                speed = 70
                print("Speed set to 70%")
            elif key == '4':
                speed = 100
                print("Speed set to 100%")
            elif key == '5':
                speed = 150
                print("Speed set to 150%")
            elif key == 'c':
                camera_feed_enabled = not camera_feed_enabled
                if camera_feed_enabled:
                    print("Camera feed enabled")
                    cap = cv2.VideoCapture(0)
                    while camera_feed_enabled:
                        ret, frame = cap.read()
                        if not ret:
                            print("Failed to capture image")
                            break
                        cv2.imshow('Camera Feed', frame)
                        if cv2.waitKey(1) & 0xFF == ord('c'):
                            camera_feed_enabled = False
                            cv2.destroyAllWindows()
                            cap.release()
                            print("Camera feed disabled")
                            break
            elif key == 'u':
                print("Looking up")
                look_up()
            elif key == 'j':
                print("Looking down")
                look_down()
            elif key == readchar.key.CTRL_C:
                print("\n Quit") 
                break    
            sleep(0.02)
        elif mode == "obstacle_avoidance":
            obstacle_avoidance_mode()
            key = readchar.readkey()
            if key == '0':
                print("Switching to manual control mode")
                mode = "manual"
            elif key == readchar.key.CTRL_C:
                print("\n Quit") 
                break

if __name__ == "__main__":
    main()
