# -*- coding: utf-8 -*-

def update(self, current_time, rate=0):
    if current_time > self.last_time + rate:
        self.frame += 1
        if self.frame >self.last_frame:
            self.frame = self.first_frame
        self.last_time = current_time