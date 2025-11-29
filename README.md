## Warachote's Hotel 🏨

Welcome to **Warachote's Hotel**, a programming project inspired by the famous **Hilbert's Grand Hotel paradox** managing an *infinite number of guests with finite rooms*! This project was developed as a group assignment (4 members) and demonstrates clever use of data structures to efficiently handle guest assignments, collisions, and room management.  

<br>

## 🛠 Features

- **Add guest groups**: Queue new guest groups from different channels/routes.  
- **Assign rooms automatically**: Uses **prime-numbered rooms** and resolves collisions with **quadratic probing**.  
- **Manual room management**: Add or remove guests from specific rooms.  
- **Search rooms efficiently**: O(1) lookups using Python dictionaries.  
- **Display sorted room list**: Rooms are sorted using **Heap Sort** before displaying.  
- **Save state to file**: Export current hotel state to a text file.  
- **Memory usage reporting**: Check the memory footprint of the main rooms dictionary.  
- **Performance tracking**: Function execution time is measured for performance insights.  

<br>

## 💡 Technical Highlights

- **Data Structures Used**:  
  - Dictionary (`dict`) for **O(1) room lookups**  
  - Heap for **sorting occupied rooms**  
  - Quadratic probing for **collision resolution**  
- **Algorithms**:  
  - Heap Sort for sorting rooms  
  - Prime-number generation for room assignments  
- **Python Techniques**:  
  - Decorators (`@time_it`) for performance tracking  
  - Classes for **modular design** (`Guest`, `HilbertHotel`)  
  - Clear console interface with dynamic banner  

<br>

## 👥 Project Group

- Developed collaboratively by **4 students**  
- Each member contributed to implementing and optimizing data structures, algorithms, and CLI management.  