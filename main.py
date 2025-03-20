
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random

STRONG_NUMBER_RANGE = range(1, 8)

def load_lotto_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if not file_path:
        messagebox.showwarning('שגיאה', 'לא נבחר קובץ.')
        return None
    try:
        df = pd.read_csv(file_path, encoding='cp1255')
        if 'המספר החזק/נוסף' in df.columns:
            df.rename(columns={'המספר החזק/נוסף': 'חזק'}, inplace=True)
        required_columns = ['תאריך'] + [str(i) for i in range(1, 7)] + ['הגרלה', 'חזק']
        for col in required_columns:
            if col not in df.columns:
                messagebox.showerror('שגיאה', f'עמודה חסרה בקובץ: {col}')
                return None
        df['Date'] = pd.to_datetime(df['תאריך'], format='%d/%m/%Y')
        df['Day'] = df['Date'].dt.strftime('%A')
        df = df.dropna()
        return df
    except Exception as e:
        messagebox.showerror('שגיאה', f'אירעה תקלה בטעינת הקובץ:\n{e}')
        return None

def generate_random_predictions_by_day(day):
    predictions = ''
    for i in range(14):
        numbers = sorted(random.sample(range(1, 38), 6))
        strong_number = random.randint(1, 7)
        predictions += f'יום {day} - טור {i+1}: {numbers} | חזק: {strong_number}\n'
    return predictions

def build_new_ui():
    root = tk.Tk()
    root.title('מחולל לוטו לפי ימים - Liviu Holivia')
    root.configure(bg='black')

    tk.Label(root, text='בחר יום הגרלה:', fg='lime', bg='black', font=('Courier', 12)).pack(pady=10)
    day_var = tk.StringVar()
    ttk.Combobox(root, textvariable=day_var, values=['Tuesday', 'Thursday', 'Saturday']).pack(pady=5)

    def predict():
        df = load_lotto_file()
        if df is None:
            return
        day = day_var.get()
        results = generate_random_predictions_by_day(day)
        messagebox.showinfo('14 תחזיות ליום נבחר', results)

    tk.Button(root, text='טען קובץ וחזה תחזיות ליום', command=predict, bg='black', fg='lime', font=('Courier', 12)).pack(pady=40)

    tk.Label(root, text='נבנה מחדש לפי בקשתך | Liviu Holivia', fg='lime', bg='black', font=('Courier', 10)).pack(side=tk.BOTTOM, pady=20)

    root.geometry('700x450')
    root.mainloop()

if __name__ == '__main__':
    build_new_ui()
