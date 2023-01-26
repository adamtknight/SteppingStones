import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
global input_boxes

class InputBox:

    def __init__(self, name, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.name = name

    def handle_event(self, event):
        global done
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    submit()
                    done = True
                    
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

def submit():
    global input_boxes, ts, sl, sw, bw, bh
    for ib in input_boxes:
        if ib.name == "ts":
            ts = ib.text
        elif ib.name == "sl":
            sl = ib.text
        elif ib.name == "sw":
            sw = ib.text
        elif ib.name == "bw":
            bw = ib.text
        elif ib.name == "bh":
            bh = ib.text

def main():
    global input_boxes, done
    clock = pg.time.Clock()
    treadmill_speed = InputBox("ts", 100, 50, 140, 32)
    step_length = InputBox("sl", 100, 125, 140, 32)
    step_width = InputBox("sw", 100, 200, 140, 32)
    box_width = InputBox("bw", 100, 275, 140, 32)
    box_height = InputBox("bh",100, 350, 140, 32)
    input_boxes = [treadmill_speed, step_length,step_width,box_width,box_height]
    done = False

    # Create text boxes above each input box
    treadmill_speed_text = FONT.render("Treadmill Speed (m/s):", True, (255, 255, 255))
    step_length_text = FONT.render("Step Length (m):", True, (255, 255, 255))
    step_width_text = FONT.render("Step Width (m):", True, (255, 255, 255))
    box_width_text = FONT.render("Box Width (m):", True, (255, 255, 255))
    box_height_text = FONT.render("Box Height (m):", True, (255, 255, 255))


    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)
            # Blit the text boxes to the screen
        screen.blit(treadmill_speed_text, (25, 20))
        screen.blit(step_length_text, (25, 95))
        screen.blit(step_width_text, (25, 170))
        screen.blit(box_width_text, (25, 245))
        screen.blit(box_height_text, (25, 320))
        pg.display.flip()
        clock.tick(30)
    return ts, sl, sw, bw, bh

if __name__ == '__main__':
    main()
    pg.quit()