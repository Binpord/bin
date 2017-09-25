#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import importlib

def error_print(msg):
    parent_frame = sys._getframe(1)
    sys.stderr.write("error:    in file '{}:{}' in function '{}':    {}\n".format(parent_frame.f_code.co_filename, 
                                        parent_frame.f_lineno, parent_frame.f_code.co_name, msg))

def usage():
    print('Usage:')
    print('%s DATA_FILE [-f FUNCTOIN_FILE] [-x XLABEL] [-y YLABEL] [-o FILENAME] [--linear-fit | --poly-fit NUMBER] [--help]' % sys.argv[0])

def read_data(filename):
    with open(filename, "r") as datafile:
        data = datafile.readlines()
        res = []
        for i in range(len(data)):
            res.append(np.fromstring(data[i], sep= ','))
    return res

def main():
    if len(sys.argv) < 2:
        error_print("inappropriate arguments.")
        usage()
        return 1

    data_filename = sys.argv[1]
    save_to_file = False
    save_filename = ""
    extern_func = False
    extern_func_filepath = ""
    xlabel = ""
    ylabel = ""
    poly_fit = False
    poly_fit_degree = 0

    # Parsing arguments. Checking only from 2nd, because 0 is progname, 1st is data_file.
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "-f":
            extern_func = True
            extern_func_filepath = sys.argv[i + 1]
        elif sys.argv[i] == "-x":
            xlabel = sys.argv[i + 1]
        elif sys.argv[i] == "-y":
            ylabel = sys.argv[i + 1]
        elif sys.argv[i] == "-o":
            save_to_file = True
            save_filename = sys.argv[i + 1]
        elif sys.argv[i] == "--linear-fit":
            poly_fit = True
            poly_fit_degree = 1
        elif sys.argv[i] == "--poly-fit":
            poly_fit = True
            poly_fit_degree = int(sys.argv[i + 1])
        elif sys.argv[i] == "--help":
            usage()
            return 0

    # read data from DATA_FILE
    data = read_data(data_filename)

    # If "-f" specified, importing function calculate from FUNCTION_FILE and calculating data.
    # Else ploting the two data sets.
    if extern_func:
        extern_func_last_sep = extern_func_filepath.rfind('/')
        extern_func_filedir = extern_func_filepath[:extern_func_last_sep]
        extern_func_filename = extern_func_filepath[extern_func_last_sep + 1:]
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
        # plot the result
        plt.rc('text', usetex = True)
        plt.rc('font', family = 'serif')

        plt.figure()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.errorbar(plot_data[0], plot_data[1], xerr = plot_data[2], yerr = plot_data[2], fmt = 'o')
        plt.grid()

        if poly_fit:
            fit_coefs = np.polyfit(plot_data[0], plot_data[1], poly_fit_degree)
            print(fit_coefs)
            fit_fn = np.poly1d(fit_coefs)

            minX = np.amin(plot_data[0])
            maxX = np.amax(plot_data[0])
            stepX = (maxX - minX) / 10
            fitX = np.arange(minX, maxX + stepX, stepX)
            fitY = fit_fn(fitX)

            plt.plot(fitX, fitY)

    if save_to_file:
        if save_filename[-4:] != ".png":
            save_filename += ".png"
        plt.savefig(save_filename, format = 'png')
    else:
        plt.show()

    return 0

if __name__ == "__main__":
    sys.exit(main())
