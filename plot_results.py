#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import importlib
import scipy.interpolate
import argparse

def error_print(msg):
    parent_frame = sys._getframe(1)
    sys.stderr.write("error:    in file '{}:{}' in function '{}':    {}\n".format(parent_frame.f_code.co_filename, 
                                        parent_frame.f_lineno, parent_frame.f_code.co_name, msg))

def read_data(filename):
    with open(filename, "r") as datafile:
        data = datafile.readlines()
        res = []
        for i in range(len(data)):
            res.append(np.fromstring(data[i], sep= ','))
    return res

def main():
    parser = argparse.ArgumentParser(description="Plot results from csv-like formated files.")
    parser.add_argument("data_filename", metavar="DATA_FILE", type=str,
                        help="path to the data file")
    parser.add_argument("-f", "--func", dest="extern_func_filepath", type=str,
                        help="file, containing extern calculate(...) function")
    parser.add_argument("-t", "--title", dest="title", type=str,
                        help="title for the plot")
    parser.add_argument("-x", "--xlabel", dest="xlabel", type=str, default="",
                        help="xlabel for the plot")
    parser.add_argument("-y", "--ylabel", dest="ylabel", type=str, default="",
                        help="ylabel for the plot")
    parser.add_argument("-o", dest="save_filepath", type=str,
                        help="path to the .png file to save resulting plot")
    parser.add_argument("--linear-fit", dest="poly_fit_degree", action="store_const", const=1,
                        help="linear fit; is equal to '--poly-fit 1'")
    parser.add_argument("--poly-fit", dest="poly_fit_degree", type=int,
                        help="polynomial fit")
    parser.add_argument("--cubic-approx", dest="cubic_approx", action="store_const", const=True,
                        help="cubic approximation")
    parser.add_argument("-s", "--steps", dest="num_of_steps", type=int, default=10,
                        help="custom number of steps in subplot")

    args = parser.parse_args()

    if (args.cubic_approx == True | (args.poly_fit_degree is not None)) & args.num_of_steps < 100:
        args.num_of_steps = 100

    # plot the result
    plt.rc('text', usetex = True)
    plt.rc('font', family = 'serif')

    plt.figure()
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)

    if args.title is not None:
        plt.title(args.title)

    # read data from DATA_FILE
    data = read_data(args.data_filename)

    # If "-f" specified, importing function calculate from FUNCTION_FILE and calculating data.
    # Else ploting the two data sets.
    if args.extern_func_filepath is not None:
        extern_func_last_sep = args.extern_func_filepath.rfind('/')
        extern_func_filedir = args.extern_func_filepath[:extern_func_last_sep]
        extern_func_filename = args.extern_func_filepath[extern_func_last_sep + 1:]
        sys.path.append(extern_func_filedir)
        if extern_func_filename[-3:] == ".py":
            extern_module = importlib.import_module(extern_func_filename[:-3])
        else:
            extern_module = importlib.import_module(extern_func_filename)

        all_plot_data = extern_module.calculate(data)
    else:
        all_plot_data = []
        all_plot_data.append([data[0], data[1], 0, 0])

    for plot_data in all_plot_data:
        if len(plot_data) != 4:
            error_print("inappropriate result from calculate")
            return 1

        plt.errorbar(plot_data[0], plot_data[1], xerr = plot_data[2], yerr = plot_data[2], fmt = 'o')
        plt.grid()

        if args.poly_fit_degree is not None:
            fit_coefs = np.polyfit(plot_data[0], plot_data[1], args.poly_fit_degree)
            print(fit_coefs)
            fit_fn = np.poly1d(fit_coefs)

            minX = np.amin(plot_data[0])
            maxX = np.amax(plot_data[0])
            stepX = (maxX - minX) / args.num_of_steps
            fitX = np.arange(minX, maxX + stepX, stepX)
            fitY = fit_fn(fitX)

            plt.plot(fitX, fitY)
        elif args.cubic_approx:
            fit_fn = scipy.interpolate.interp1d(plot_data[0], plot_data[1], kind = 'cubic')

            minX = np.amin(plot_data[0])
            maxX = np.amax(plot_data[0])
            stepX = (maxX - minX) / args.num_of_steps
            fitX = np.arange(minX, maxX + stepX, stepX)
            fitY = fit_fn(fitX)

            plt.plot(fitX, fitY)

    if args.save_filepath is not None:
        if args.save_filepath[-4:] != ".png":
            args.save_filepath += ".png"
        plt.savefig(args.save_filepath, format = 'png')
    else:
        plt.show()

    return 0

if __name__ == "__main__":
    sys.exit(main())
