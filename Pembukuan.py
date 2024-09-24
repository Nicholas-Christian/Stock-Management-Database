import os
import psycopg2
import pytz
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import *
from tkinter import messagebox, font

# Koneksi ke database

conn = psycopg2.connect(os.environ["DATABASE_URL"])

# Definisi user dan admin
USER_CREDENTIALS = {
    'admin': {'username': 'admin', 'password': 'admin123', 'role': 'admin', 'user_id': '1'},
    'user': {'username': 'user', 'password': 'user123', 'role': 'user', 'user_id': '2'}
}

# Fungsi untuk login
def login():
    username = entry_username.get()
    password = entry_password.get()

    for key, cred in USER_CREDENTIALS.items():
        if cred['username'] == username and cred['password'] == password:
            global user_role
            user_role = cred['role']
            global user_id
            user_id = cred['user_id']
            root.withdraw()
            show_main_menu()
            return
    
    messagebox.showerror("Login Error", "Username atau password salah")

# Fungsi untuk menampilkan menu utama
def show_main_menu():
    global main_window
    main_window = Toplevel(root)
    main_window.title("Menu Utama")
    main_window.geometry("800x600")
    
    Label(main_window, text="Menu Utama", font=('Helvetica', 16)).pack(pady=10)
    button_frame = Frame(main_window)
    button_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
    
    Button(button_frame, text="Barang Masuk", command=barang_masuk_action, font=('Helvetica', 16), width=20).pack(pady=10)
    Button(button_frame, text="Barang Keluar", command=barang_keluar_action, font=('Helvetica', 16), width=20).pack(pady=10)
    Button(button_frame, text="Return Barang", command=return_barang_action, font=('Helvetica', 16), width=20).pack(pady=10)
    Button(button_frame, text="Cek Stok", command=show_cek_stok, font=('Helvetica', 16), width=20).pack(pady=10)
    Button(button_frame, text="History", command=show_history, font=('Helvetica', 16), width=20).pack(pady=10)
    Button(button_frame, text="Pengaturan", command=show_pengaturan, font=('Helvetica', 16), width=20).pack(pady=10)
    Button(button_frame, text="Logout", command=logout, font=('Helvetica', 16), width=20).pack(pady=20)
    
    main_window.grab_set()
    main_window.wait_window()

# Fungsi untuk logout
def logout():
    main_window.destroy()
    root.deiconify()


def barang_masuk(jenisbarang, jumlahyard, jumlahroll, nota):
    try:
        with conn.cursor() as cur:
            # Use CALL statement to execute the stored procedure
            cur.execute(
                "CALL update_stock_and_history(%s, %s, %s, %s, %s, %s, NULL, NULL, NULL)",
                (user_id, jenisbarang, jumlahyard, jumlahroll, 'masuk', nota)
            )
            conn.commit()
            messagebox.showinfo("Success", "Barang berhasil ditambahkan dan dicatat di history")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", str(e))

def barang_keluar(jenisbarang, jumlahyard, jumlahroll, nota):
    try:
        with conn.cursor() as cur:
            # Use CALL statement to execute the stored procedure
            cur.execute(
                "CALL update_stock_and_history(%s, %s, %s, %s, %s, %s, NULL, NULL, NULL)",
                (user_id, jenisbarang, jumlahyard, jumlahroll, 'keluar', nota)
            )
            conn.commit()
            messagebox.showinfo("Success", "Barang berhasil dikurangi dan dicatat di history")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", str(e))

def return_barang(jenisbarang, jumlahyard, jumlahroll, jenisbarang_return, jumlahyard_return, jumlahroll_return, nota):
    try:
        with conn.cursor() as cur:
            # Use CALL statement to execute the stored procedure
            cur.execute(
                "CALL update_stock_and_history(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (user_id, jenisbarang, jumlahyard, jumlahroll, 'return', nota, jenisbarang_return, jumlahyard_return, jumlahroll_return)
            )
            conn.commit()
            messagebox.showinfo("Success", "Return berhasil dan dicatat di history")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", str(e))

# Fungsi untuk menampilkan halaman Barang Masuk
def barang_masuk_action():
    def submit_masuk():
        jenisbarang = jenisbarang_var.get()
        jumlahyard = entry_jumlahyard.get()
        jumlahroll = entry_jumlahroll.get()
        nota = entry_nota.get()
        
        try:
            jumlahyard = int(jumlahyard)
            jumlahroll = int(jumlahroll)
            barang_masuk(jenisbarang, jumlahyard, jumlahroll, nota)
            masuk_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Jumlah Yard dan Roll harus berupa angka.")

    masuk_window = Toplevel(main_window)
    masuk_window.title("Barang Masuk")
    masuk_window.geometry("900x700")

    Label(masuk_window, text="Jenis Barang", font=('Helvetica', 18)).grid(row=0, column=0, padx=10, pady=20, columnspan=3, sticky='w')

    jenisbarang_list = [
        "CEY Kringkel", "Jenis 2", "Jenis 3", "Jenis 4", "Jenis 5", 
        "Jenis 6", "Jenis 7", "Jenis 8", "Jenis 9", "Jenis 10",
        "Jenis 11", "Jenis 12", "Jenis 13", "Jenis 14", "Jenis 15"
    ]
    jenisbarang_var = tk.StringVar(masuk_window, jenisbarang_list[0])  # Default value

    row = 1
    col = 0
    max_columns = 3
    max_rows = 5

    for i, jenis in enumerate(jenisbarang_list):
        tk.Radiobutton(masuk_window, text=jenis, variable=jenisbarang_var, value=jenis, font=('Helvetica', 14)).grid(row=row, column=col, padx=10, pady=5, sticky='w')
        col += 1
        if col >= max_columns:
            col = 0
            row += 1
        if row >= max_rows:
            break

    # Adding spacing between Radiobuttons and Entry boxes
    Label(masuk_window, text="", font=('Helvetica', 18)).grid(row=row, column=0, padx=10, pady=20, columnspan=4, sticky='w')

    Label(masuk_window, text="Jumlah Yard", font=('Helvetica', 18)).grid(row=row + 1, column=0, padx=10, pady=10, sticky='e')
    entry_jumlahyard = Entry(masuk_window, font=('Helvetica', 18))
    entry_jumlahyard.grid(row=row + 1, column=1, padx=10, pady=10, sticky='w')

    Label(masuk_window, text="Jumlah Roll", font=('Helvetica', 18)).grid(row=row + 1, column=2, padx=10, pady=10, sticky='e')
    entry_jumlahroll = Entry(masuk_window, font=('Helvetica', 18))
    entry_jumlahroll.grid(row=row + 1, column=3, padx=10, pady=10, sticky='w')

    Label(masuk_window, text="Nota", font=('Helvetica', 18)).grid(row=row + 2, column=0, padx=10, pady=10, sticky='e')
    entry_nota = Entry(masuk_window, font=('Helvetica', 18))
    entry_nota.grid(row=row + 2, column=1, padx=10, pady=10, columnspan=3, sticky='w')

    Label(masuk_window, text="", font=('Helvetica', 18)).grid(row=row, column=0, padx=10, pady=20, columnspan=4, sticky='w')

    Button(masuk_window, text="Submit", command=submit_masuk, font=('Helvetica', 18)).grid(row=row + 3, column=0, columnspan=4, pady=20)
    Button(masuk_window, text="Back", command=masuk_window.destroy, font=('Helvetica', 18)).grid(row=row + 4, column=0, columnspan=4, pady=10)

    masuk_window.grab_set()
    masuk_window.wait_window()


# Fungsi untuk menampilkan halaman Barang Keluar
def barang_keluar_action():
    def submit_keluar():
        jenisbarang = jenisbarang_var.get()
        jumlahyard = entry_jumlahyard.get()
        jumlahroll = entry_jumlahroll.get()
        nota = entry_nota.get()
        
        try:
            jumlahyard = int(jumlahyard)
            jumlahroll = int(jumlahroll)
            barang_keluar(jenisbarang, jumlahyard, jumlahroll, nota)
            keluar_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Jumlah Yard dan Roll harus berupa angka.")

    keluar_window = Toplevel(main_window)
    keluar_window.title("Barang Keluar")
    keluar_window.geometry("900x700")

    Label(keluar_window, text="Jenis Barang", font=('Helvetica', 18)).grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky='w')

    jenisbarang_list = [
        "CEY Kringkel", "Jenis 2", "Jenis 3", "Jenis 4", "Jenis 5", 
        "Jenis 6", "Jenis 7", "Jenis 8", "Jenis 9", "Jenis 10",
        "Jenis 11", "Jenis 12", "Jenis 13", "Jenis 14", "Jenis 15"
    ]
    jenisbarang_var = tk.StringVar(keluar_window, jenisbarang_list[0])  # Default value

    row = 1
    col = 0
    max_columns = 3
    max_rows = 5

    for i, jenis in enumerate(jenisbarang_list):
        tk.Radiobutton(keluar_window, text=jenis, variable=jenisbarang_var, value=jenis, font=('Helvetica', 14)).grid(row=row, column=col, padx=10, pady=5, sticky='w')
        col += 1
        if col >= max_columns:
            col = 0
            row += 1
        if row >= max_rows:
            break
        
        
    Label(keluar_window, text="", font=('Helvetica', 18)).grid(row=row, column=0, padx=10, pady=20, columnspan=4, sticky='w')

    Label(keluar_window, text="Jumlah Yard", font=('Helvetica', 18)).grid(row=row + 1, column=0, padx=10, pady=10, sticky='e')
    entry_jumlahyard = Entry(keluar_window, font=('Helvetica', 18))
    entry_jumlahyard.grid(row=row + 1, column=1, padx=10, pady=10, sticky='w')

    Label(keluar_window, text="Jumlah Roll", font=('Helvetica', 18)).grid(row=row + 1, column=2, padx=10, pady=10, sticky='e')
    entry_jumlahroll = Entry(keluar_window, font=('Helvetica', 18))
    entry_jumlahroll.grid(row=row + 1, column=3, padx=10, pady=10, sticky='w')

    Label(keluar_window, text="Nota", font=('Helvetica', 18)).grid(row=row + 2, column=0, padx=10, pady=10, sticky='e')
    entry_nota = Entry(keluar_window, font=('Helvetica', 18))
    entry_nota.grid(row=row + 2, column=1, padx=10, pady=10, columnspan=3, sticky='w')

    Label(keluar_window, text="", font=('Helvetica', 18)).grid(row=row, column=0, padx=10, pady=20, columnspan=4, sticky='w')

    Button(keluar_window, text="Submit", command=submit_keluar, font=('Helvetica', 18)).grid(row=row + 3, column=0, columnspan=4, pady=20)
    Button(keluar_window, text="Back", command=keluar_window.destroy, font=('Helvetica', 18)).grid(row=row + 4, column=0, columnspan=4, pady=10)

    keluar_window.grab_set()
    keluar_window.wait_window()



# Fungsi untuk menampilkan halaman Return Barang
def return_barang_action():
    def submit_return():
        jenisbarang = jenisbarang_var.get()
        jumlahyard = entry_jumlahyard.get()
        jumlahroll = entry_jumlahroll.get()
        jenisbarang_return = jenisbarang_return_var.get()
        jumlahyard_return = entry_jumlahyard_return.get()
        jumlahroll_return = entry_jumlahroll_return.get()
        nota = entry_nota.get()
        
        try:
            jumlahyard = int(jumlahyard)
            jumlahroll = int(jumlahroll)
            jumlahyard_return = int(jumlahyard_return)
            jumlahroll_return = int(jumlahroll_return)
            return_barang(jenisbarang, jumlahyard, jumlahroll, jenisbarang_return, jumlahyard_return, jumlahroll_return, nota)
            return_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Jumlah Yard dan Roll harus berupa angka.")

    return_window = Toplevel(main_window)
    return_window.title("Return Barang")
    return_window.geometry("1200x1000")  # Adjust size for better visibility

    Label(return_window, text="Nota", font=('Helvetica', 18)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    entry_nota = Entry(return_window, font=('Helvetica', 18))
    entry_nota.grid(row=0, column=1, padx=10, pady=10, columnspan=3, sticky='w')

    Label(return_window, text="Jenis Barang", font=('Helvetica', 18)).grid(row=1, column=0, padx=10, pady=10, sticky='w')

    # Frame for the first set of RadioButtons (Jenis Barang)
    frame1 = Frame(return_window)
    frame1.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='w')

    jenisbarang_list = [
        "CEY Kringkel", "Jenis 2", "Jenis 3", "Jenis 4", "Jenis 5", 
        "Jenis 6", "Jenis 7", "Jenis 8", "Jenis 9", "Jenis 10",
        "Jenis 11", "Jenis 12", "Jenis 13", "Jenis 14", "Jenis 15"
    ]
    
    jenisbarang_var = tk.StringVar(return_window, jenisbarang_list[0])  # Default value

    row = 0
    col = 0
    max_columns = 3

    for i, jenis in enumerate(jenisbarang_list):
        tk.Radiobutton(frame1, text=jenis, variable=jenisbarang_var, value=jenis, font=('Helvetica', 14)).grid(row=row, column=col, padx=10, pady=5, sticky='w')
        col += 1
        if col >= max_columns:
            col = 0
            row += 1

    # Setelah frame pertama, set row baru
    current_row = row + 3

    Label(return_window, text="Jumlah Yard", font=('Helvetica', 18)).grid(row=current_row, column=0, padx=10, pady=10, sticky='w')
    entry_jumlahyard = Entry(return_window, font=('Helvetica', 18))
    entry_jumlahyard.grid(row=current_row, column=1, padx=10, pady=10, sticky='w')

    Label(return_window, text="Jumlah Roll", font=('Helvetica', 18)).grid(row=current_row, column=2, padx=10, pady=10, sticky='e')
    entry_jumlahroll = Entry(return_window, font=('Helvetica', 18))
    entry_jumlahroll.grid(row=current_row, column=3, padx=10, pady=10, sticky='w')

    # Frame for the second set of RadioButtons (Jenis Barang Return)
    current_row += 1
    Label(return_window, text="Jenis Barang Return", font=('Helvetica', 18)).grid(row=current_row, column=0, padx=10, pady=10, sticky='w')

    frame2 = Frame(return_window)
    frame2.grid(row=current_row + 1, column=0, columnspan=4, padx=10, pady=10, sticky='w')

    jenisbarang_return_var = tk.StringVar(return_window, jenisbarang_list[0])  # Default value

    row = 0
    col = 0

    for i, jenis in enumerate(jenisbarang_list):
        tk.Radiobutton(frame2, text=jenis, variable=jenisbarang_return_var, value=jenis, font=('Helvetica', 14)).grid(row=row, column=col, padx=10, pady=5, sticky='w')
        col += 1
        if col >= max_columns:
            col = 0
            row += 1

    current_row += row + 2

    Label(return_window, text="Jumlah Yard Return", font=('Helvetica', 18)).grid(row=current_row, column=0, padx=10, pady=10, sticky='w')
    entry_jumlahyard_return = Entry(return_window, font=('Helvetica', 18))
    entry_jumlahyard_return.grid(row=current_row, column=1, padx=10, pady=10, sticky='w')

    Label(return_window, text="Jumlah Roll Return", font=('Helvetica', 18)).grid(row=current_row, column=2, padx=10, pady=10, sticky='e')
    entry_jumlahroll_return = Entry(return_window, font=('Helvetica', 18))
    entry_jumlahroll_return.grid(row=current_row, column=3, padx=10, pady=10, sticky='w')

    Button(return_window, text="Submit", command=submit_return, font=('Helvetica', 18)).grid(row=current_row + 1, column=0, columnspan=4, pady=20)
    Button(return_window, text="Back", command=return_window.destroy, font=('Helvetica', 18)).grid(row=current_row + 2, column=0, columnspan=4, pady=10)

    return_window.grab_set()
    return_window.wait_window()



# Fungsi untuk menampilkan cek stok
def show_cek_stok():
    def update_table():
        for i in tree.get_children():
            tree.delete(i)
        
        with conn.cursor() as cur:
            cur.execute("SELECT jenisbarang, jumlahyard, jumlahroll, harga, total FROM barang")
            rows = cur.fetchall()
            
            for row in rows:
                total = row[4]
                formatted_total = f"{total:,}"
                tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], formatted_total))
    
    cek_stok_window = Toplevel(main_window)
    cek_stok_window.title("Cek Stok")
    cek_stok_window.geometry("1000x800")

    columns = ('Jenis Barang', 'Jumlah Yard', 'Jumlah Roll', 'Harga', 'Total')
    tree = ttk.Treeview(cek_stok_window, columns=columns, show='headings')

    # Atur lebar kolom agar pas
    tree.column('Jenis Barang', width=200, anchor='w')
    tree.column('Jumlah Yard', width=100, anchor='center')
    tree.column('Jumlah Roll', width=100, anchor='center')
    tree.column('Harga', width=100, anchor='center')
    tree.column('Total', width=100, anchor='center')

    tree.heading('Jenis Barang', text='Jenis Barang')
    tree.heading('Jumlah Yard', text='Jumlah Yard')
    tree.heading('Jumlah Roll', text='Jumlah Roll')
    tree.heading('Harga', text='Harga')
    tree.heading('Total', text='Total')


    tree.pack(side=LEFT, fill=BOTH, expand=True)

     # Perbesar font untuk isi Treeview
    style = ttk.Style()
    style.configure("Treeview",
                    font=('Helvetica', 18))  # Font untuk isi
    style.configure("Treeview.Heading",
                    font=('Helvetica', 20))  # Font untuk heading
    
    update_table()

    Button(cek_stok_window, text="Back", command=cek_stok_window.destroy, font=('Helvetica', 16)).pack(pady=10)

    cek_stok_window.grab_set()
    cek_stok_window.wait_window()

def hitung_pendapatan_harian():
    try:
        with conn.cursor() as cur:
            # Hitung pendapatan harian
            query = """
            SELECT SUM(CASE WHEN action = 'keluar' THEN total 
                            WHEN action = 'return' THEN -total END) AS total_pendapatan_harian
            FROM history
            WHERE DATE(timestamp) = CURRENT_DATE;
            """
            cur.execute(query)
            result = cur.fetchone()
            pendapatan_harian = result[0] if result[0] is not None else 0
            
            # Simpan pendapatan harian ke tabel pendapatan_harian
            upsert_query = """
            INSERT INTO pendapatan_harian (tanggal, total_pendapatan)
            VALUES (CURRENT_DATE, %s)
            ON CONFLICT (tanggal) DO UPDATE
            SET total_pendapatan = pendapatan_harian.total_pendapatan + EXCLUDED.total_pendapatan;
            """
            cur.execute(upsert_query, (pendapatan_harian,))
            conn.commit()

            # Format pendapatan harian dengan ribuan (misal Rp 1.000)
            formatted_pendapatan = f"Rp {pendapatan_harian:,.0f}"
            return formatted_pendapatan
            
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", str(e))
        return None


# Fungsi untuk mengformat timestamp ke timezone Jakarta
def format_timestamp(timestamp):
    if timestamp.tzinfo is None:
        timestamp = pytz.utc.localize(timestamp)
    
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    timestamp_jakarta = timestamp.astimezone(jakarta_tz)
    return timestamp_jakarta.strftime(" %H:%M:%S  Tanggal : %d-%m-%Y")

def show_history():
    def update_table():
        for i in tree.get_children():
            tree.delete(i)

        with conn.cursor() as cur:
            # Hapus data yang lebih dari 7 hari
            cur.execute("""
               DELETE FROM history
               WHERE timestamp < NOW() - INTERVAL '7 days';
            """)
            conn.commit()  # Pastikan untuk menyimpan perubahan
            
            cur.execute("SELECT nota, action, jenisbarang, jumlahyard, jumlahroll, total, timestamp FROM history ORDER BY timestamp DESC")
            rows = cur.fetchall()

            for row in rows:
                formatted_time = format_timestamp(row[6])
                total = row[5]
                formatted_total = f"{total:,}"  # Format total dengan koma untuk ribuan
                tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], formatted_total, formatted_time))

        # Hitung pendapatan harian setelah semua data history ditampilkan
        daily_revenue = hitung_pendapatan_harian()

        # Cek jika daily_revenue None, set jadi Rp 0
        if daily_revenue is None:
            daily_revenue = "Rp 0"

        # Tampilkan pendapatan harian di Text widget yang lebih besar
        revenue_box.delete(1.0, tk.END)  # Kosongkan dulu box
        revenue_box.insert(tk.END, f"Pendapatan Harian: {daily_revenue}\n")
    
    history_window = Toplevel(main_window)
    history_window.title("History")
    history_window.geometry("1200x800")

    # Tambahkan kolom ke dalam Treeview
    columns = ('Nota', 'Action', 'Jenis Barang', 'Jumlah Yard', 'Jumlah Roll', 'Total', 'Timestamp')
    tree = ttk.Treeview(history_window, columns=columns, show='headings')

    tree.column('Nota', width=150, anchor='w')
    tree.column('Action', width=100, anchor='center')
    tree.column('Jenis Barang', width=150, anchor='w')
    tree.column('Jumlah Yard', width=100, anchor='center')
    tree.column('Jumlah Roll', width=100, anchor='center')
    tree.column('Total', width=80, anchor='center')
    tree.column('Timestamp', width=180, anchor='center')

    tree.heading('Nota', text='Nota', anchor='w')
    tree.heading('Action', text='Action', anchor='center')
    tree.heading('Jenis Barang', text='Jenis Barang', anchor='w')
    tree.heading('Jumlah Yard', text='Jumlah Yard', anchor='center')
    tree.heading('Jumlah Roll', text='Jumlah Roll', anchor='center')
    tree.heading('Total', text='Total', anchor='center')
    tree.heading('Timestamp', text='Timestamp', anchor='center')

    tree.pack(side=LEFT, fill=BOTH, expand=True)

    style = ttk.Style()
    style.configure("Treeview", font=('Helvetica', 15))
    style.configure("Treeview.Heading", font=('Helvetica', 16))

    # Tambahkan Text widget untuk menampilkan pendapatan harian dengan ukuran lebih besar
    revenue_box = Text(history_window, height=5, width=50, font=('Helvetica', 18), bg='lightyellow')
    revenue_box.pack(pady=20)

    # Inisialisasi label kosong
    revenue_box.insert(tk.END, "Pendapatan Harian: Menghitung...\n")

    update_table()

    Button(history_window, text="Back", command=history_window.destroy, font=('Helvetica', 16)).pack(pady=10)

    history_window.grab_set()
    history_window.wait_window()

    

# Fungsi untuk menampilkan halaman Pengaturan (ubah harga barang)
def show_pengaturan():
    def submit_pengaturan():
        jenisbarang = entry_jenisbarang.get()
        harga_baru = entry_harga_baru.get()
        
        try:
            harga_baru = int(harga_baru)
            update_harga_barang(jenisbarang, harga_baru)
            pengaturan_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka.")
    
    pengaturan_window = Toplevel(main_window)
    pengaturan_window.title("Pengaturan - Ubah Harga Barang")
    pengaturan_window.geometry("500x400")
    
    Label(pengaturan_window, text="Jenis Barang", font=('Helvetica', 18)).grid(row=0, column=0, padx=10, pady=20, sticky='e')
    entry_jenisbarang = Entry(pengaturan_window, font=('Helvetica', 18))
    entry_jenisbarang.grid(row=0, column=1, padx=10, pady=20)
    
    Label(pengaturan_window, text="Harga Baru", font=('Helvetica', 18)).grid(row=1, column=0, padx=10, pady=20, sticky='e')
    entry_harga_baru = Entry(pengaturan_window, font=('Helvetica', 18))
    entry_harga_baru.grid(row=1, column=1, padx=10, pady=20)
    
    Button(pengaturan_window, text="Submit", command=submit_pengaturan, font=('Helvetica', 18)).grid(row=2, column=0, columnspan=2, pady=20)
    Button(pengaturan_window, text="Back", command=pengaturan_window.destroy, font=('Helvetica', 18)).grid(row=3, column=0, columnspan=2, pady=10)
    
    pengaturan_window.grab_set()
    pengaturan_window.wait_window()
    
# Fungsi untuk memperbarui harga barang di database
def update_harga_barang(jenisbarang, harga_baru):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE barang SET harga = %s WHERE jenisbarang = %s",
                (harga_baru, jenisbarang)
            )
            conn.commit()
            messagebox.showinfo("Success", "Harga barang berhasil diperbarui")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", str(e))




# Setup Tkinter root window
root = Tk()
root.title("Login")
root.geometry("600x400")

Label(root, text="Username", font=('Helvetica', 16)).pack(pady=10)
entry_username = Entry(root, font=('Helvetica', 16))
entry_username.pack(pady=10, padx=20, fill=X)

Label(root, text="Password", font=('Helvetica', 16)).pack(pady=10)
entry_password = Entry(root, show='*', font=('Helvetica', 16))
entry_password.pack(pady=10, padx=20, fill=X)

Button(root, text="Login", command=login, font=('Helvetica', 16)).pack(pady=20)

root.mainloop()
