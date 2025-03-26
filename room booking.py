import sqlite3
import smtplib
from email.message import EmailMessage

def initialize_db():
    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        room_type TEXT,
                        nights INTEGER,
                        total_cost REAL)''')
    conn.commit()
    conn.close()

def book_room(name, email, room_type, nights):
    rates = {"Single": 50, "Double": 80, "Suite": 150}
    if room_type not in rates:
        print("Invalid room type!")
        return
    
    total_cost = rates[room_type] * nights
    
    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (name, email, room_type, nights, total_cost) VALUES (?, ?, ?, ?, ?)",
                   (name, email, room_type, nights, total_cost))
    conn.commit()
    conn.close()
    
    send_email(email, name, room_type, nights, total_cost)
    print(f"Booking successful! Bill sent to {email}")

def send_email(to_email, name, room_type, nights, total_cost):
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"
    
    msg = EmailMessage()
    msg['Subject'] = "Hotel Booking Confirmation"
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(f"Dear {name},\n\nYour booking is confirmed.\n"
                    f"Room Type: {room_type}\n"
                    f"Nights: {nights}\n"
                    f"Total Cost: ${total_cost}\n\nThank you for choosing our hotel!")
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)

def view_bookings():
    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()
    
    if not bookings:
        print("No bookings found.")
    else:
        for booking in bookings:
            print(f"ID: {booking[0]}, Name: {booking[1]}, Email: {booking[2]}, Room: {booking[3]}, Nights: {booking[4]}, Cost: ${booking[5]}")

def cancel_booking(booking_id):
    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    print(f"Booking ID {booking_id} has been canceled.")

def main():
    initialize_db()
    
    while True:
        print("\nHotel Booking System")
        print("1. Book a Room")
        print("2. View Bookings")
        print("3. Cancel Booking")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            room_type = input("Enter room type (Single/Double/Suite): ")
            nights = int(input("Enter number of nights: "))
            book_room(name, email, room_type, nights)
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            booking_id = int(input("Enter booking ID to cancel: "))
            cancel_booking(booking_id)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()