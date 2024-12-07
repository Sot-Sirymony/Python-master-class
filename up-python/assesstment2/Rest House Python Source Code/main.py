from rest_house_manager import RestHouseManager

def main():
    manager = RestHouseManager()

    print("Welcome to the Rest House Management System!")
    
    while True:
        print("\n1. Add Room")
        print("2. Add Guest")
        print("3. Make Reservation")
        print("4. Check Available Rooms")
        print("5. Check In")
        print("6. Check Out")
        print("7. Exit")

        choice = input("\nSelect an option: ")

        if choice == '1':
            room_number = input("Enter room number: ")
            room_type = input("Enter room type (Single/Double/Suite): ")
            manager.add_room(room_number, room_type)
            print(f"Room {room_number} added successfully.")
        
        elif choice == '2':
            guest_name = input("Enter guest name: ")
            contact = input("Enter guest contact: ")
            manager.add_guest(guest_name, contact)
            print(f"Guest {guest_name} added successfully.")
        
        elif choice == '3':
            guest_id = input("Enter guest ID: ")
            room_id = input("Enter room ID: ")
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            check_out = input("Enter check-out date (YYYY-MM-DD): ")
            manager.make_reservation(guest_id, room_id, check_in, check_out)
            print(f"Reservation made successfully.")
        
        elif choice == '4':
            rooms = manager.get_available_rooms()
            if rooms:
                print("Available Rooms:")
                for room in rooms:
                    print(f"Room ID: {room[0]}, Room Number: {room[1]}, Type: {room[2]}")
            else:
                print("No available rooms.")
        
        elif choice == '5':
            room_id = input("Enter room ID to check-in: ")
            manager.check_in(room_id)
            print(f"Room {room_id} checked in successfully.")
        
        elif choice == '6':
            room_id = input("Enter room ID to check-out: ")
            manager.check_out(room_id)
            print(f"Room {room_id} checked out successfully.")
        
        elif choice == '7':
            print("Exiting system.")
            break
        
        else:
            print("Invalid option. Please try again.")
    
    manager.close()

if __name__ == "__main__":
    main()
