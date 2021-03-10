import tkinter as tk
from tkinter.constants import E
import tkinter.messagebox as tkm
import tkinter.font as tkf
import tkinter.ttk as ttk

from anilist_api.anilist import get_users_scores_ani
from myanimelist_api.myanimelist import get_users_scores_mal
from stats_engine.stats import calculate_affinity


VERSION_NUMBER = 'pre-alpha'


class MainWindow(tk.Frame):
    def __init__(self, parent):
        # Set TK attributes
        self.parent = parent
        self.root = tk.Toplevel(self.parent)
        self.root.protocol('WM_DELETE_WINDOW', self.close)

        # Build Window
        self.build_window()

    def build_window(self):
        self.root.title('Anime Affinity (GoodAffinity) version {0}'.format(VERSION_NUMBER))
        self.root.resizable(1, 1)

        # Font Settings
        self.window_font = tkf.Font(None, size=18)

        # Account Selection
        accounts_header = tk.Label(self.root, font=self.window_font, text='Username')
        accounts_header.grid(row=0, column=0, columnspan=2, sticky='NESW')

        service_options = ['AniList', 'MAL']

        self.service_one = tk.StringVar()
        service_one_dropdown = tk.OptionMenu(self.root, self.service_one, *service_options)
        service_one_dropdown.config(width=10)
        service_one_dropdown.grid(row=1, column=0, sticky='EW')

        self.username_one_textbox = tk.Entry(self.root, font=self.window_font, borderwidth=2, relief='groove')
        self.username_one_textbox.grid(row=1, column=1, sticky='NESW')

        self.service_two = tk.StringVar()
        service_two_dropdown = tk.OptionMenu(self.root, self.service_two, *service_options)
        service_two_dropdown.config(width=10)
        service_two_dropdown.grid(row=2, column=0, sticky='EW')

        self.username_two_textbox = tk.Entry(self.root, font=self.window_font, borderwidth=2, relief='groove')
        self.username_two_textbox.grid(row=2, column=1, sticky='NESW')

        # Calculate Button
        calculate_button = tk.Button(self.root, font=self.window_font, text='Calculate', command=self.calculate_affinity)
        calculate_button.grid(row=3, column=0, columnspan=2, sticky='NESW')

    def calculate_affinity(self):
        # Check if Anilist to MAL ID conversion is needed
        mal_conversion = self.service_one.get() != self.service_two.get()


        # Fetch data for user one
        try:
            if self.service_one.get() == 'AniList':
                user_one_data = get_users_scores_ani(self.username_one_textbox.get(), mal_conversion)
            else:
                user_one_data = get_users_scores_mal(self.username_one_textbox.get())
        except Exception as e:
            tkm.showerror('Error', 'The first username is causing an error!')
            raise e

        # Fetch data for user two
        try:
            if self.service_two.get() == 'AniList':
                user_two_data = get_users_scores_ani(self.username_two_textbox.get(), mal_conversion)
            else:
                user_two_data = get_users_scores_mal(self.username_two_textbox.get())
        except Exception as e:
            tkm.showerror('Error', 'The second username is causing an error!')
            raise e

        # Calculate affinity
        affinity_results = calculate_affinity(user_one_data, user_two_data)

        row = 5
        for result in affinity_results:
            result_header = tk.Label(self.root, font=self.window_font, text=result[0])
            result_header.grid(row=row, column=0, columnspan=2, sticky='NESW')

            result = tk.Label(self.root, font=self.window_font, text=str(result[1]))
            result.grid(row=row + 1, column=0, columnspan=2, sticky='NESW')

            row += 2

    def close(self):
        self.root.destroy()
        self.parent.destroy()

def main():
    root = tk.Tk()
    root.withdraw()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
