import time
import sys
import os
import math

def time_it(func):
    """A decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"\n[Performance] Function '{func.__name__}' took {(end_time - start_time) * 1000:.4f} ms to execute.")
        return result
    return wrapper

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def find_next_prime(number: int) -> int:
    """Finds the next prime number strictly greater than the given number."""
    next_num = number + 1
    while True:
        is_current_num_prime = True
        if next_num < 2:
            is_current_num_prime = False
        elif next_num == 2:
            is_current_num_prime = True
        elif next_num % 2 == 0:
            is_current_num_prime = False
        else:
            # Check for factors from 3 up to the square root of the number
            for i in range(3, int(math.sqrt(next_num)) + 1, 2):
                if next_num % i == 0:
                    is_current_num_prime = False
                    break
        if is_current_num_prime:
            return next_num
        next_num += 1

def print_banner():
    """Prints the application's welcome banner."""
    banner = r"""
 __        __                   _           _       
 \ \      / /_ _ _ __ __ _  ___| |__   ___ | |_ ___ 
  \ \ /\ / / _` | '__/ _` |/ __| '_ \ / _ \| __/ _ \
   \ V  V / (_| | | | (_| | (__| | | | (_) | ||  __/
    \_/\_/ \__,_|_|  \__,_|\___|_| |_|\___/ \__\___|

--> Welcome to Warachote's Hotel <--
            ( ͡° ͜ʖ ͡°)
Manage infinite guests with finite rooms using Warachote's paradox of the Grand Hotel.
          Developed by KPAT@CE KMITL
"""
    print(banner)

class Guest:
    """Represents a single guest with their origin channel, sequence, and arrival round."""
    def __init__(self, channel, sequence, round_num):
        self.channel = channel
        self.sequence_number = sequence
        self.round = round_num

    def __repr__(self):
        return (f"Guest(Ch={self.channel}, Seq={self.sequence_number}, Round={self.round})")

class HilbertHotel:
    """Manages the hotel rooms and guest assignments."""
    def __init__(self):
        self.rooms = {}
        self.pending_requests = {}
        self.thod = {}
        self.last_prime_room = [2, 3]

    @time_it
    def add_guest_group(self, channel_id: int, num_guests: int):
        """Stores a request to add guests. This method is loop-free."""
        print(f"\n[State] Occupied rooms before adding to queue: {len(self.rooms)}")
        if num_guests < 1:
            print("Error: Number of guests must be at least 1.")
            return

        self.pending_requests.setdefault(channel_id, 0)
        self.pending_requests[channel_id] += num_guests
        print(f"Queued a request for {num_guests} guests from route {channel_id}.")

    @time_it
    def assign_pending_guests(self):
        """
        Assigns all pending guests from the queue to unique rooms.
        Handles collisions with pre-existing rooms using quadratic probing.
"""
        if not self.pending_requests:
            print("No new guest requests in the queue to assign.")
            return

        print("\n[Assignment] Preparing to assign new guests to prime-numbered rooms...")
        total_new_guests = sum(self.pending_requests.values())
        processed_channels_this_batch = set()
        assigned_count = 0
        k = 1

        while assigned_count < total_new_guests:
            def create_and_assign(ch, seq):
                nonlocal assigned_count
                if ch not in processed_channels_this_batch:
                    self.thod.setdefault(ch, 0)
                    self.thod[ch] += 1
                    processed_channels_this_batch.add(ch)
                current_round = self.thod[ch]
                guest_to_assign = Guest(ch, seq, current_round)
                
                # Calculate the unique room number using the two base prime numbers.
                base_prime_1 = self.last_prime_room[0]
                base_prime_2 = self.last_prime_room[1]
                final_room_num = (base_prime_1 ** seq) * (base_prime_2 ** ch)
                
                if final_room_num in self.rooms:
                    print(f"  [Collision] Room {final_room_num} is occupied. Probing for a new room...")
                    original_room_num = final_room_num
                    i = 1
                    while final_room_num in self.rooms:
                        # Quadratic probing formula: new = original + i^2
                        final_room_num = original_room_num + (i * i)
                        i += 1
                    print(f"  [Resolved] Found vacant Room {final_room_num} for {guest_to_assign}.")

                self.rooms[final_room_num] = guest_to_assign
                print(f"  Assigning {guest_to_assign} -> Room {final_room_num}")
                
                assigned_count += 1

            # Traverse down the k-th column
            for row in range(1, k + 1):
                ch, seq = k, row
                if assigned_count < total_new_guests and self.pending_requests.get(ch, 0) >= seq:
                    create_and_assign(ch, seq)

            # Traverse across the k-th row (excluding the corner)
            for col in range(1, k):
                ch, seq = col, k
                if assigned_count < total_new_guests and self.pending_requests.get(ch, 0) >= seq:
                    create_and_assign(ch, seq)
            
            k += 1
            if k > total_new_guests * 2: # Safety break
                print("\n[Warning] Assignment loop terminated early to prevent infinite execution.")
                break
        
        # Find the next two primes for the next batch of assignments
        self.last_prime_room = [find_next_prime(self.last_prime_room[0]), find_next_prime(self.last_prime_room[1])]
        self.pending_requests.clear()
        print("\n[Assignment] Finished assigning all pending guests.")


    @time_it
    def manual_add_room(self, room_number: int, channel: int, sequence: int):
        """Manually adds a single guest to a specific room."""
        if room_number in self.rooms:
            print(f"Room {room_number} is already occupied by {self.rooms[room_number]}.")
            return False
        
        self.thod.setdefault(channel, 0)
        self.thod[channel] += 1
        current_channel_round = self.thod[channel]

        new_guest = Guest(channel, sequence, current_channel_round)
        self.rooms[room_number] = new_guest
        print(f"Successfully added {new_guest} to room {room_number}.")
        return True

    @time_it
    def manual_delete_room(self, room_number: int):
        """Manually removes a guest from a specific room."""
        if room_number in self.rooms:
            guest = self.rooms.pop(room_number)
            print(f"Successfully removed {guest} from room {room_number}.")
        else:
            print(f"Error: Room {room_number} is not occupied.")

    @time_it
    def search_room(self, room_number: int):
        """Searches for a guest in a specific room."""
        if room_number in self.rooms:
            print(f"Room {room_number} is occupied by: {self.rooms[room_number]}")
            return self.rooms[room_number]
        print(f"Room {room_number} is vacant.")
        return None

    @time_it
    def get_sorted_room_numbers(self) -> list:
        """Sorts the occupied room numbers using Heap Sort."""
        arr = list(self.rooms.keys())
        n = len(arr)
        if n <= 1:
            return arr

        def sift_down(start, end):
            root = start
            while True:
                child = 2 * root + 1
                if child > end:
                    break
                if child + 1 <= end and arr[child] < arr[child + 1]:
                    child += 1
                if arr[root] < arr[child]:
                    arr[root], arr[child] = arr[child], arr[root]
                    root = child
                else:
                    break

        # Heapify
        for start in range((n // 2) - 1, -1, -1):
            sift_down(start, n - 1)
        
        # Sort
        for end in range(n - 1, 0, -1):
            arr[end], arr[0] = arr[0], arr[end]
            sift_down(0, end - 1)

        return arr

    @time_it
    def display_all_rooms(self):
        """Displays a sorted list of all occupied rooms."""
        if not self.rooms:
            print("\nThe hotel is currently empty.")
            return

        print("\n" + "="*30)
        print("   Hotel Residents List")
        print("="*30)
        for room_num in self.get_sorted_room_numbers():
            guest = self.rooms[room_num]
            print(f"Room {room_num:<6}: {guest}")
        print("="*30)

    def get_memory_usage(self):
        """Prints the memory usage of the main rooms dictionary."""
        size = sys.getsizeof(self.rooms)
        print(f"\n[Memory] The 'rooms' dictionary is using approximately {size} bytes.")

    @time_it
    def save_to_file(self, filename: str):
        """Saves the current state of the hotel to a text file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Total Occupants: {len(self.rooms)}\n")
                f.write(f"{'='*30}\n")
                for room_num in self.get_sorted_room_numbers():
                    guest = self.rooms[room_num]
                    f.write(f"Room: {room_num}\n")
                    f.write(f" - Route: {guest.channel}\n")
                    f.write(f" - Sequence: {guest.sequence_number}\n")
                    f.write(f" - Round: {guest.round}\n\n")
            print(f"Successfully saved hotel data to '{filename}'.")
        except IOError as e:
            print(f"Error: Could not write to file '{filename}'. Reason: {e}")


def main():
    sys.set_int_max_str_digits(0) # <-- ADD THIS LINE
    """Main function to run the command-line interface for the hotel management system."""
    clear_screen()
    print_banner()
    hotel = HilbertHotel()

    while True:
        print("\n" + "="*30)
        print("    Warachote's Hotel Menu")
        print("="*30)
        print("1. Add group to queue")
        print("2. Assign all rooms")
        print("3. Display all rooms")
        print("4. Search for a room")
        print("5. Manually add a guest")
        print("6. Manually remove a guest")
        print("7. Save to file")
        print("8. Check memory usage")
        print("0. Exit")
        print("="*30)

        choice = input("Enter your choice: ")
        clear_screen()
        print_banner()

        if choice == '1':
            try:
                channel = int(input("Enter the route ID for the new group (> 0): "))
                if channel < 1:
                    print("Error: Route ID must be 1 or greater.")
                    input("\nPress Enter to continue...")
                    continue
                count = int(input(f"Enter the number of guests for route {channel}: "))
                hotel.add_guest_group(channel, count)
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")

        elif choice == '2':
            hotel.assign_pending_guests()

        elif choice == '3':
            hotel.display_all_rooms()
            print(f"amount{len(hotel.rooms)}")

        elif choice == '4':
            try:
                room_num = int(input("Enter the room number to search for: "))
                hotel.search_room(room_num)
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                
        elif choice == '5':
            room_num = int(input("Enter the room number to add to: "))
            if room_num < 1:
                print('Room number must be at least 1. Please try again.')
                input("Press smth to continue...")
                continue
            ch = "Manual"
            seq = "Manual"
            hotel.manual_add_room(room_num, ch, seq,)
            
        elif choice == '6':
            try:
                room_num = int(input("Enter the room number to remove: "))
                if room_num < 1:
                    print('Error: Room number must be 1 or greater.')
                    input("\nPress Enter to continue...")
                    continue
                hotel.manual_delete_room(room_num)
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")

        elif choice == '7':
            filename = input("Enter the filename (e.g., hotel_data.txt): ")
            hotel.save_to_file(filename)

        elif choice == '8':
            hotel.get_memory_usage()

        elif choice == '0':
            print("Thank you for using the Warachote's Hotel system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()
        print_banner()


if __name__ == "__main__":
    main()