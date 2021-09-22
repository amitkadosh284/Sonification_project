import xlrd
import sys
import random
import pygame
import time
import tkinter as tk


def get_num_interrupt(value):
    """
    this function decide the number of interrupt in rhythm in the sound of journalist
    :param value: the value the country have in free journalist
    :return: the number of interrupt ( pause) in rythm of journalist sound
    """
    return int(value / 10)


def get_volume(value):
    """
    get the volume of the corrupt sound
    :param value: the country value in corrupt
    :return: the volume of the corrupt sound
    """
    if value > 50:
        return 0.01
    elif 50 <= value <= 75:
        return 0.1
    elif 25 <= value < 50:
        return 1
    else:
        return 3


def get_locations_interrupt(num_interrupt):
    """

    :param num_interrupt: the number of interrupts in rhythm we want
    :return: array of location to make the interrupt (pause)
    """
    random_locations = []
    for i in range(num_interrupt):
        n = random.randint(0, 10)
        while n in random_locations:
            n = random.randint(0, 10)
        random_locations.append(n)
    return random_locations


def pause(sec):
    """
    function the make pause in playing the sound and create control on the rhythm
    :param sec: the number of second to pause
    :return:
    """
    end = time.time() + sec
    while (end - time.time()) > 0:
        continue


class DemocraticSymphonic:
    DATA = {}

    def __init__(self):
        self._mixer = pygame.mixer
        self._mixer.init()
        self._pig_sound = self._mixer.Sound("C:/Users/USER/PycharmProjects/Senofication/snore.wav")
        self._type_sound = self._mixer.Sound("C:/Users/USER/PycharmProjects/Senofication/singel_type.wav")
        self._channel_1 = self._mixer.Channel(1)
        self._channel_2 = self._mixer.Channel(2)
        self.create_map()
        self._root = tk.Tk()
        self._root.geometry("1000x600")
        self._bg = tk.PhotoImage(file=r"map.png")
        self._map_label = tk.Label(self._root, image=self._bg)
        self._map_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._root.bind("<Motion>", self.motion)
        tk.mainloop()

    def create_map(self):
        """
        this method insert to the DATA dictionary all the data of location of the country on the map and the values
        of the corruption and journalism
        :return:
        """
        wb = xlrd.open_workbook("C:/Users/USER/PycharmProjects/Senofication/data.xls")
        sheet = wb.sheet_by_index(0)
        for i in range(1, 38):
            self.DATA[sheet.cell_value(i, 0)] = [float(sheet.cell_value(i, 1)), float(sheet.cell_value(i, 2)),
                                                 float(sheet.cell_value(i, 3)), float(sheet.cell_value(i, 4)),
                                                 float(sheet.cell_value(i, 5)), float(sheet.cell_value(i, 6))]

    def motion(self, event):
        """
        this function bind between the motion of the mouse to the sound it play
        :param event: the motion of the mouse
        :return:
        """
        self._channel_1.stop()
        self._channel_2.stop()
        x, y = event.x, event.y
        for country in self.DATA.keys():
            x1 = self.DATA[country][2]
            y1 = self.DATA[country][3]
            x2 = self.DATA[country][4]
            y2 = self.DATA[country][5]
            if (x1 <= x <= x2) & (y1 <= y <= y2):
                self.main(country)

    def main(self, country_name):
        """
        this function by the country name play the sound it fit
        :param country_name: the name of the country
        :return:
        """
        print(country_name)
        corrupt_volume = get_volume(self.DATA[country_name][1])
        journalist_interrupt = get_locations_interrupt(get_num_interrupt(self.DATA[country_name][0]))
        self._channel_1.play(self._pig_sound)
        self._channel_1.set_volume(corrupt_volume)
        for i in range(10):
            sec = 0.5
            self._channel_2.play(self._type_sound)
            if i in journalist_interrupt:
                sec = random.uniform(0, 2)
            pause(sec)
        self._channel_1.stop()
        self._channel_2.stop()


if __name__ == "__main__":
    DemocraticSymphonic()
