import PySimpleGUI as sg
from PIL import Image, ImageTk
import numpy as np
import cv2
import imageio
import csv


def arr_to_img(arr):
    img = Image.fromarray(arr)
    img = img.resize((600,400))
    return ImageTk.PhotoImage(image=img)


class Visrl:
    def __init__(self, env, agent=None):
        self.env = env
        self.agent = agent
        self.state = np.around(self.env.reset(), 2)
        layout = [
            [sg.Button("Set Action Keys", key='set_keys')] + \
            [sg.Text(f"{i}: None", key=f'action{i}') for i in range(self.env.action_space.n)],
            [sg.Image(key='screen')],
            [sg.Slider(range=(0, 0), size=(66,10), orientation='h', key='slider')],
            [sg.Text("ms/frame: 0", key='mpf'),
             sg.Text("Time: 0", key='time'),
             sg.Text("Total Reward: 0", key='total_reward'),],
            [sg.Text("State: ", key='state')],
            [sg.Text("Action: ", key='action'),
             sg.Text("Reward: 0", key='reward'),
             sg.Text("Done: False", key='done')],
            [sg.Button("New", key='new'),
             sg.Button("Play", key='play'),
             sg.Button("Stop", key='stop'),
             sg.Button("Speed Up", key="speedup"),
             sg.Button("Slow down", key="slowdown")],
            [sg.Input("self.state[0] < -0.1", size=(30, 10), key='condition'),
             sg.Button("Add Breakpoint", key='breakpoint')],
            [sg.Text("Start frame:"),
             sg.Input("0", size=(5, 10), key='start'),
             sg.Text("End frame:"),
             sg.Input("100", size=(5, 10), key='end'),
             sg.Button("mp4", key='mp4'),
             sg.Button("gif", key='gif'),
             sg.Button("history", key='history')],
        ]
        self.window = sg.Window("Visrl", layout,
                   return_keyboard_events=True,
                   use_default_focus=False,
                    element_justification='c')
        self.event, self.values = self.window.read(timeout=0)
        self.play = False
        self.mode = "agent"
        self.ms = 0
        self.time = 0
        self.total_reward = 0
        self.done = False
        self.images = []
        self.video = []
        self.values = []
        self.conditions = []
        self.keys = {}
        self.rkeys = {}
        self.update()

    def set_keys(self):
        keys_set = True
        for i in range(self.env.action_space.n):
            self.window[f'action{i}'].update('0: -')
        i = 0
        while i < self.env.action_space.n:
            event, values = self.window.read()
            if len(event) == 1:
                self.window[f'action{i}'].update(value=f'{i}: {event}')
                self.keys[event] = i
                self.rkeys[i] = event
                i += 1
            elif event is not None:
                e = event[:-3] if event in ("Left:37", "Up:38", "Right:39", "Down:40") else event
                self.window[f'action{i}'].update(value=f'{i}: {e}')
                self.keys[event] = i
                self.rkeys[i] = event[:-3] if event in ("Left:37", "Up:38", "Right:39", "Down:40") else event
                i += 1

    def update(self):
        if self.ms == 0:
            self.fps = 'Fastest'
        else:
            self.fps = round(1000 / self.ms, 2)
        self.window['mpf'].update(value="ms/frame: " + str(self.ms))
        screen = self.env.render(mode='rgb_array')
        img = arr_to_img(screen)
        self.window['screen'].update(data=img)
        self.window['state'].update(value="State: " + str(self.state))

    def step(self, action):
        self.action = action
        obs, self.reward, done, _ = self.env.step(action)
        self.total_reward += self.reward
        self.time += 1
        self.state = np.around(obs, 2)
        self.done = done
        self.values.append(dict(state=np.around(obs, 2),
                                reward=self.reward,
                                done=done,
                                total_reward=self.total_reward,
                                time=self.time,
                                action=self.action))
        if done:
            self.play = False
        screen = self.env.render(mode='rgb_array')
        img = arr_to_img(screen)
        self.video.append(screen)
        self.images.append(img)
        self.window['screen'].update(data=img)
        self.window['time'].update(value="Time: " + str(self.time))
        self.window['reward'].update(value="Reward: " + str(np.around(self.reward, 2)))
        self.window['total_reward'].update(value="Total Reward: " + str(np.around(self.total_reward, 2)))
        self.window['state'].update(value="State: " + str(self.state))
        self.window['done'].update(value="Done: " + str(self.done))
        if self.rkeys != {}:
            self.window['action'].update(value="Action: " + str(self.rkeys[self.action]))
        else:
            self.window['action'].update(value="Action: " + str(self.action))
        self.window['slider'].update(range=(0, self.time), value=self.time)

    def reset(self):
        if self.time == 0:
            return
        obs = self.env.reset()
        self.images = []
        self.values = []
        self.total_reward = 0
        self.reward = 0
        self.state = np.around(obs, 2)
        self.time = 0
        self.done = False
        screen = self.env.render(mode='rgb_array')
        im = Image.fromarray(screen)
        imtk = ImageTk.PhotoImage(image=im)
        self.video.append(screen)
        self.images.append(imtk)
        self.window['screen'].update(data=imtk)
        self.window['time'].update(value="Time: " + str(self.time))
        self.window['total_reward'].update(value="Total Reward: 0" + str(np.around(self.total_reward, 2)))
        self.window['reward'].update(value="Reward: 0" + str(np.around(self.reward, 2)))
        self.window['state'].update(value="State: " + str(self.state))
        self.window['done'].update(value="Done: " + str(self.done))
        if self.rkeys != {}:
            self.window['action'].update(value="Action: " + str(self.rkeys[self.action]))
        else:
            self.window['action'].update(value="Action: " + str(self.action))
        self.window['slider'].update(range=(0, self.time), value=self.time)

    def update_slider(self):
        t = int(self.window_values['slider'])
        self.window['slider'].update(self.window_values['slider'])
        if t < len(self.images):
            self.window['screen'].update(data=self.images[t])
            self.window['time'].update(value="Time: " + str(self.values[t]['time']))
            self.window['total_reward'].update(value="Total Reward: " + str(np.around(self.values[t]['total_reward'], 2)))
            self.window['reward'].update(value="Reward: " + str(np.around(self.values[t]['reward'], 2)))
            self.window['state'].update(value="State: " + str(self.values[t]['state']))
            self.window['done'].update(value="Done: " + str(self.values[t]['done']))
            if self.rkeys != {}:
                self.window['action'].update(value="Action: " + str(self.rkeys[self.values[t]['action']]))
            else:
                self.window['action'].update(value="Action: " + str(self.action))

    def run(self):
        while True:
            event, self.window_values = self.window.read(timeout=self.ms)
            if event is None:
                break
            if event == "set_keys":
                self.set_keys()
            if event == "new":
                self.reset()
            if event == "play":
                self.play = True
                self.mode = "agent"
            if event == "stop":
                self.play = False
            if event in self.keys:
                self.mode = "human"
                self.step(self.keys[event])
            elif self.play and self.mode == "agent":
                if self.agent is not None:
                    action, _ = self.agent.predict(self.state)
                else:
                    action = self.env.action_space.sample()
                self.step(action)

            if event == "slowdown":
                self.ms += 10
            if event == "speedup":
                self.ms -= 10 if self.ms > 0 else 0
            if event == "breakpoint":
                self.conditions.append(self.window_values['condition'])
            if event == "mp4":
                start, end = int(self.window_values['start']), int(self.window_values['end'])
                shape = self.video[0].shape[:2]
                fps = self.fps if type(self.fps) != str else 30
                out = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (shape[1], shape[0]))
                for frame in self.video[start:end+1]:
                    out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                out.release()
            if event == "gif":
                start, end = int(self.window_values['start']), int(self.window_values['end'])
                imageio.mimsave('video.gif', self.video[start:end+1])
            if event == "history":
                keys = self.values[0].keys()
                with open('history.csv', 'w', newline='') as f:
                    w = csv.DictWriter(f, keys)
                    w.writeheader()
                    w.writerows(self.values)

            self.update()

            if all(list(map(eval, self.conditions))) and self.conditions != []:
                self.play = False
                self.conditions = []

            if not self.play and self.mode != "human" and self.window_values['slider'] != self.time:
                self.update_slider()

        self.window.close()
        self.env.close()


