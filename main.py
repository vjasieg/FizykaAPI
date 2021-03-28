import concurrent.futures
import math

import flask
import imageio
import matplotlib as mpl
import matplotlib.pyplot as plot
import numpy as np
from flask import send_file, request
import random
import threading
import os


app = flask.Flask(__name__)
app.config["DEBUG"] = True
mpl.use("Agg")


class WykresXT:
    def make(self, amp, okres):
        name = random.randint(0, 1000000)
        time = np.arange(0, 60, 0.1)
        fig, ax = plot.subplots()  # <-- here is the start of the different part
        ax.plot(time, calc_xt(amp=float(amp), czas=time, okres_d=float(okres)))
        ax.set_title('Wykres x(t)')
        ax.set_xlabel('t (czas)')
        ax.set_ylabel('x (wychylenie)')
        ax.grid(True, which='both')
        ax.axhline(y=0, color='k')
        fig.savefig(str(name) + '.png') # <-- end of the modified part
        plot.close()
        plot.figure().clear()
        return str(name) + '.png'


class WykresAT:
    def make(self, amp, faza, okres):
        name = random.randint(0, 1000000)
        time = np.arange(0, 60, 0.1)
        fig, ax = plot.subplots()  # <-- here is the start of the different part
        ax.plot(time, calc_at(amp=float(amp), czas=time, faza_poczatkowa=float(faza), okres_d=float(okres)))
        ax.set_title('Wykres a(t)')
        ax.set_xlabel('t (czas)')
        ax.set_ylabel('a (przyśpieszenie)')
        ax.grid(True, which='both')
        ax.axhline(y=0, color='k')
        fig.savefig(str(name) + '.png')  # <-- end of the modified part
        plot.close()
        plot.figure().clear()
        return str(name) + '.png'


class WykresVT:
    def make(self, amp, faza, okres):
        name = random.randint(0, 1000000)
        time = np.arange(0, 60, 0.1)
        fig, ax = plot.subplots()  # <-- here is the start of the different part
        ax.plot(time, calc_vt(amp=float(amp), czas=time, faza_poczatkowa=float(faza), okres_d=float(okres)))
        ax.set_title('Wykres a(t)')
        ax.set_xlabel('t (czas)')
        ax.set_ylabel('v (prędkość)')
        ax.grid(True, which='both')
        ax.axhline(y=0, color='k')
        fig.savefig(str(name) + '.png')  # <-- end of the modified part
        plot.close()
        plot.figure().clear()
        return str(name) + '.png'


class Wahadlo:
    def draw_point(self, x, y, i, okres, folder, amp):
        fig, ax = plot.subplots()
        # Draw a point at the location (3, 9) with size 1000
        ax.scatter(x, y, s=60)
        # Set chart title.
        ax.set_title("Wahadło", fontsize=19)
        # Set x axis label.
        ax.set_xlabel("Wychylenie", fontsize=10)
        # Set y axis label.
        # Set size of tick labels.
        ax.tick_params(axis='both', which='major', labelsize=9)
        # Display the plot in the matplotlib's viewer.

        # List to hold x values.
        x_number_values = [0, x]
        # List to hold y values.
        y_number_values = [25, y]
        # Plot the number in the list and set the line thickness.
        ax.plot(x_number_values, y_number_values, linewidth=3)
        # Set the x, y axis tick marks text size.
        ax.tick_params(axis='both', labelsize=9)

        ax.set_xlim([-2 * amp, 2 * amp])
        ax.set_ylim([-40, 40])

        fig.savefig(folder + "\\" + str(i) + '.png')
        plot.close()
        plot.figure().clear()
    def make(self, args):
        name = ".\\frames" + str(random.randint(0, 10000000))
        os.mkdir(name)

        x = 0
        time = np.arange(0, float(args["okres"]), 1 / 20)
        for i in time:
            calc = calc_xt(float(args["amp"]), i, float(args["okres"]))
            y = 25 * calc_a(calc, 25)
            self.draw_point(
                calc,
                y,
                x,
                int(args["okres"]),
                name,
                float(args["amp"]),
            )
            x += 1
        return name


def calc_vt(amp, czas, faza_poczatkowa, okres_d):
    y = []
    omega = (2 * math.pi) / okres_d
    if not isinstance(czas, int) and not isinstance(czas, float):
        for val in czas:
            y.append(amp * omega * math.cos((omega * val) + faza_poczatkowa))
        return y
    else:
        return round(amp * omega * math.cos((omega * czas) + faza_poczatkowa), 5)


def calc_xt(amp, czas, okres_d):
    y = []
    omega = (2 * math.pi) / okres_d
    if not isinstance(czas, int) and not isinstance(czas, float):
        for val in czas:
            y.append(amp * math.cos(omega * val))
        return y
    else:
        return round(amp * math.cos(omega * czas), 5)


def calc_at(amp, czas, faza_poczatkowa, okres_d):
    y = []
    omega = (2 * math.pi) / okres_d
    if not isinstance(czas, int) and not isinstance(czas, float):
        for val in czas:
            y.append(-amp * (omega ** 2) * math.sin(omega * val + faza_poczatkowa))
        return y
    else:
        return round(-amp * (omega ** 2) * math.sin(omega * czas + faza_poczatkowa), 5)


def calc_a(x, length):
    if length > x:
        z = (length ** 2) - (x ** 2)
    else:
        z = (x ** 2) - (length ** 2)
    return length - math.sqrt(z)


@app.route('/wartosci_t', methods=['GET'])
def wartosci_t():
    args = {"amp": float(request.args.get('amp')), "okres": float(request.args.get('okres')), "czas": float(request.args.get('czas')), "faza": float(request.args.get('faza'))}
    if args["amp"] is not None and args["okres"] is not None and args["faza"] is not None and args["czas"] is not None:
        json = {
            "v(t)": calc_vt(args["amp"], args["czas"], args["faza"], args["okres"]),
            "x(t)": calc_xt(args["amp"], args["czas"], args["okres"]),
            "a(t)": calc_at(args["amp"], args["czas"], args["faza"], args["okres"])
        }
        return json
    else:
        return "podaj wartosci amp okres faza i czas"


@app.route('/wykres_v', methods=['GET'])
def wykres_v():
    args = {"amp": request.args.get('amp'), "okres": request.args.get('okres'), "faza": request.args.get('faza')}
    if args["amp"] is not None and args["okres"] is not None and args["faza"] is not None:
        wykres = WykresVT()
        return send_file(wykres.make(args["amp"], args["faza"], args["okres"]))
    else:
        return "podaj: '?amp=' '&okres=' '&faza='"


@app.route('/wykres_x', methods=['GET'])
def wykres_x():
    time = []
    args = {"amp": request.args.get('amp'), "okres": request.args.get('okres')}
    if args["amp"] is not None and args["okres"] is not None:
        wykres = WykresXT()
        # x = threading.Thread(target=wykres.make(args["amp"], args["okres"]), args=(1,), daemon=True)
        # x.start()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(wykres.make, args["amp"], args["okres"])
            return_value = future.result()
            return send_file(return_value)
    else:
        return "podaj: '?amp=' '&okres='"


@app.route('/wykres_a', methods=['GET'])
def wykres_a():
    args = {"amp": request.args.get('amp'), "okres": request.args.get('okres'), "faza": request.args.get("faza")}
    if args["amp"] is not None and args["okres"] is not None and args["faza"] is not None:
        wykres = WykresAT()
        return send_file(wykres.make(args["amp"], args["faza"], args["okres"]))
    else:
        return "podaj: '?amp=' '&okres=' '&faza='"


@app.route('/wahadlo', methods=['GET'])
def wahadlo():
    print("zaczynam robic zdjecie")
    args = {"amp": request.args.get('amp'), "okres": request.args.get('okres')}
    x = 0
    y = 0
    old_calc = 0
    time = np.arange(0, 20, 0.1)
    for i in time:
        calc = calc_xt(float(args["amp"]), i, float(args["okres"]))
        draw_point(
            calc,
            y,
            x
        )
        if x < 0:
            y += 0.1
        else:
            y -= 0.1

        print(round(y, 1))
        print("x= " + str(calc))
        x += 1
        old_calc = calc

    imageNames = []
    for i in range(int(args["okres"]) * 20):
        imageNames.append(folder_name + "\\" + str(i) + '.png')
    images = list(imageNames)
    image_list = []
    for file_name in images:
        image_list.append(imageio.imread(file_name))
    imageio.mimwrite('result.gif', image_list, fps=20)
    return send_file('result.gif')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=25565, threaded=True)