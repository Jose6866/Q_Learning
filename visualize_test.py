import tkinter as tk
from tkinter import Button
import time
import numpy as np
from PIL import ImageTk, Image
PhotoImage = ImageTk.PhotoImage

UNIT = 100  # Number of pixels for each grid

# TRANSITION_PROB = 1
# POSSIBLE_ACTIONS = [0, 1, 2, 3]  # 좌, 우, 상, 하
# ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 좌표로 나타낸 행동
# REWARDS = []


class GraphicDisplay(tk.Tk):
    def __init__(self, Env, agent):
        super(GraphicDisplay, self).__init__()
        self.env = Env
        self.HEIGHT, self.WIDTH = self.env.size()
        self.title('Policy Iteration')
        self.geometry('{0}x{1}'.format(self.WIDTH * UNIT, self.HEIGHT * UNIT + 50))
        self.texts = []
        self.arrows = []

        self.agent = agent
        # self.evaluation_count = 0
        # self.improvement_count = 0
        self.is_moving = 0
        (self.up, self.down, self.left, self.right), self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        # self.text_reward(2, 2, "R : 1.0")
        # self.text_reward(1, 2, "R : -1.0")
        # self.text_reward(2, 1, "R : -1.0")

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height= self.HEIGHT * UNIT+50,
                           width= self.WIDTH * UNIT)
        # # 버튼 초기화
        # iteration_button = Button(self, text="Evaluate",
        #                           command=self.evaluate_policy)
        # iteration_button.configure(width=10, activebackground="#33B5E5")
        # canvas.create_window(self.WIDTH * UNIT * 0.13, self.HEIGHT * UNIT + 10,
        #                      window=iteration_button)
        # policy_button = Button(self, text="Improve",
        #                        command=self.improve_policy)
        # policy_button.configure(width=10, activebackground="#33B5E5")
        # canvas.create_window(self.WIDTH * UNIT * 0.37, self.HEIGHT * UNIT + 10,
        #                      window=policy_button)
        policy_button = Button(self, text="move", command=self.move_by_policy)
        policy_button.configure(width=10, activebackground="#33B5E5")
        canvas.create_window(self.WIDTH * UNIT * 0.62, self.HEIGHT * UNIT + 30,
                                window=policy_button)
        # policy_button = Button(self, text="reset", command=self.reset)
        # policy_button.configure(width=10, activebackground="#33B5E5")
        # canvas.create_window(self.WIDTH * UNIT * 0.87, self.HEIGHT * UNIT + 10,
        #                       window=policy_button)

        # 그리드 생성
        for col in range(0, self.WIDTH * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = col, 0, col, self.HEIGHT * UNIT
            canvas.create_line(x0, y0, x1, y1)
        for row in range(0, self.HEIGHT * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = 0, row, self.WIDTH * UNIT, row
            canvas.create_line(x0, y0, x1, y1)

        # 캔버스에 이미지 추가
        # srow = np.random.randint(self.HEIGHT)
        # scol = np.random.randint(self.WIDTH)
        # self.rectangle = canvas.create_image(self.matrix2image_index(srow, scol), image=self.shapes[0])
        # self.goal_rectangle1 = canvas.create_image(self.matrix2image_index(0,0), image=self.shapes[3])
        # self.goal_rectangle2 = canvas.create_image(self.matrix2image_index(self.HEIGHT-1, self.WIDTH-1),
        #                                            image=self.shapes[3])

        self.goal = []
        for k in range(len(self.env.goal)):
            i,j = self.env.goal[k]
            self.goal.append(canvas.create_image(self.matrix2image_index(i,j), image=self.shapes[3]))


        self.obstacles = []
        for k in range(len(self.env.obstacles)):
            i,j = self.env.obstacles[k]
            self.obstacles.append(canvas.create_image(self.matrix2image_index(i,j), image=self.shapes[1]))


        # canvas.create_image(250, 150, image=self.shapes[1])
        # canvas.create_image(150, 250, image=self.shapes[1])
        # canvas.create_image(250, 250, image=self.shapes[2])
        canvas.pack()
        return canvas

    def matrix2image_index(self,i,j):
        return (j*UNIT+UNIT/2, i*UNIT+UNIT/2)


    def load_images(self):
        up = PhotoImage(Image.open("./img/up.png").resize((13, 13)))
        right = PhotoImage(Image.open("./img/right.png").resize((13, 13)))
        left = PhotoImage(Image.open("./img/left.png").resize((13, 13)))
        down = PhotoImage(Image.open("./img/down.png").resize((13, 13)))
        rectangle = PhotoImage(Image.open("./img/rectangle.png").resize((65, 65)))
        triangle = PhotoImage(Image.open("./img/triangle.png").resize((65, 65)))
        circle = PhotoImage(Image.open("./img/circle.png").resize((65, 65)))
        goal_grid = PhotoImage(Image.open("./img/goal.png").resize((100, 100)))
        return (up, down, left, right), (rectangle, triangle, circle, goal_grid)

    # def reset(self):
    #     if self.is_moving == 0:
    #         self.evaluation_count = 0
    #         self.improvement_count = 0
    #         for i in self.texts:
    #             self.canvas.delete(i)
    #
    #         for i in self.arrows:
    #             self.canvas.delete(i)
    #         self.agent.value_table = [[0.0] * self.WIDTH for _ in range(self.HEIGHT)]
    #         self.agent.policy_table = ([[[0.25, 0.25, 0.25, 0.25]] * self.WIDTH
    #                                     for _ in range(self.HEIGHT)])
    #         self.agent.policy_table[2][2] = []
    #         x, y = self.canvas.coords(self.rectangle)
    #         self.canvas.move(self.rectangle, UNIT / 2 - x, UNIT / 2 - y)

    def text_value(self, row, col, contents, font='Helvetica', size=10,
                   style='normal', anchor="nw"):
        origin_x, origin_y = 40, 40       #85, 70
        x, y = origin_x + (UNIT * col), origin_y + (UNIT * row)
        font = (font, str(size), style)
        text = self.canvas.create_text(x, y, fill="black", text=format(contents, '.2f'),
                                       font=font, anchor=anchor)
        return self.texts.append(text)


    def print_value_table(self):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                self.text_value(i, j, self.agent.V_values[i][j])


    # def text_reward(self, row, col, contents, font='Helvetica', size=10,
    #                 style='normal', anchor="nw"):
    #     origin_x, origin_y = 5, 5
    #     x, y = origin_y + (UNIT * col), origin_x + (UNIT * row)
    #     font = (font, str(size), style)
    #     text = self.canvas.create_text(x, y, fill="black", text=contents,
    #                                    font=font, anchor=anchor)
    #     return self.texts.append(text)
    #
    def rectangle_move(self, state, motion):
        # base_action = np.array([0, 0])
        next_state, r = self.env.interaction(state,motion)
        movement = (np.array(next_state)-np.array(state)).tolist()
        self.render()
        # location = self.find_rectangle()
        # if action == 0 and location[1] > 0:  # 좌
        #     base_action[0] -= UNIT
        # elif action == 1 and location[1] < self.WIDTH - 1:  # 우
        #     base_action[0] += UNIT
        # elif action == 2 and location[0] > 0:  # 상
        #     base_action[1] -= UNIT
        # elif action == 3 and location[0] < self.HEIGHT - 1:  # 하
        #     base_action[1] += UNIT
        # move agent
        self.canvas.move(self.rectangle, movement[1]*UNIT, movement[0]*UNIT)
        print(movement)


    def find_rectangle(self):
        temp = self.canvas.coords(self.rectangle)
        x = (temp[0] / 100) - 0.5
        y = (temp[1] / 100) - 0.5
        return int(y), int(x)


    def move_by_policy(self):
        print("move_by_policy")
        self.is_moving = 1

        #
        # start_row = np.random.randint(self.HEIGHT)
        # start_col = np.random.randint(self.WIDTH)
        # self.agent.state = [start_row, start_col]
        # self.rectangle = self.canvas.create_image(self.matrix2image_index(start_row, start_col), image=self.shapes[0])
        [start_row, start_col] = self.agent.initialize_episode()
        self.agent.state = [start_row, start_col]
        self.rectangle = self.canvas.create_image(self.matrix2image_index(start_row, start_col), image=self.shapes[0])

        # x, y = self.canvas.coords(self.rectangle)
        i,j = self.agent.state
        while [i,j] not in self.env.goal:
            self.after(100,self.rectangle_move(self.agent.state,
                                self.agent.ACTIONS[self.agent.get_action([i, j], epsilon=0)]))
            i, j = self.agent.state = self.find_rectangle()


        # while True:
        #     self.after(100, self.rectangle_move(self.agent.get_action([x, y])))
        #     x, y = self.find_rectangle()
        self.is_moving = 0

    # def draw_one_arrow(self, col, row, policy):
    #     if col == 2 and row == 2:
    #         return
    #
    #     if policy[0] > 0:  # up
    #         origin_x, origin_y = 50 + (UNIT * row), 10 + (UNIT * col)
    #         self.arrows.append(self.canvas.create_image(origin_x, origin_y,
    #                                                     image=self.up))
    #     if policy[1] > 0:  # down
    #         origin_x, origin_y = 50 + (UNIT * row), 90 + (UNIT * col)
    #         self.arrows.append(self.canvas.create_image(origin_x, origin_y,
    #                                                     image=self.down))
    #     if policy[2] > 0:  # left
    #         origin_x, origin_y = 10 + (UNIT * row), 50 + (UNIT * col)
    #         self.arrows.append(self.canvas.create_image(origin_x, origin_y,
    #                                                     image=self.left))
    #     if policy[3] > 0:  # right
    #         origin_x, origin_y = 90 + (UNIT * row), 50 + (UNIT * col)
    #         self.arrows.append(self.canvas.create_image(origin_x, origin_y,
    #                                                     image=self.right))
    #
    # def draw_from_policy(self, policy_table):
    #     for i in range(self.HEIGHT):
    #         for j in range(self.WIDTH):
    #             self.draw_one_arrow(i, j, policy_table[i][j])


    #
    def render(self):
        time.sleep(0.35)
        self.canvas.tag_raise(self.rectangle)
        self.update()
    #
    # def evaluate_policy(self):
    #     self.evaluation_count += 1
    #     for i in self.texts:
    #         self.canvas.delete(i)
    #     self.agent.policy_evaluation()
    #     self.print_value_table(self.agent.value_table)
    #
    # def improve_policy(self):
    #     self.improvement_count += 1
    #     for i in self.arrows:
    #         self.canvas.delete(i)
    #     self.agent.policy_improvement()
    #     self.draw_from_policy(self.agent.policy_table)

