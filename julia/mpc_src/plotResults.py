import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_measurement(fig, axes, dataFile, measurement):
  data = pd.read_csv(dataFile)
  measInd = np.where(data.columns.values == measurement)
  timeInd = np.where(data.columns.values == 'minute_of_day')
  measValues = data.values[:, measInd[0][0]]
  timeValues = data.values[:, timeInd[0][0]]
  hPlot = axes.plot(timeValues, measValues)
  return hPlot

def main():
  resultsFile_base = './results/run2-base-case/cl_results.csv'
  resultsFile_mpc = './results/run2-mpc-10/cl_results.csv'
  
  '''
  # plot outside temperature
  measurement = 'TOutDryBul_y'
  fig, axes = plt.subplots(3, 1, figsize = (24, 10))
  hPlot1 = plot_measurement(fig, axes[0], resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, axes[0], resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  axes[0].set(title = 'Outside temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  axes[0].legend(('base case', 'mpc case'), loc = 'upper right')
  axes[0].grid()
  #with mpl.rc_context(rc={'interactive': False}):
  #  plt.show()
'''

  # plot air supply temperature
  floor = 2
  zone = 1
  measurement1 = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  measurement2 = 'floor' + str(floor) + '_zon' + str(zone) + '_TRooAir_y'
  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u'
  fig, axes = plt.subplots(2, 1, figsize = (20, 8))
  hPlot1 = plot_measurement(fig, axes[0], resultsFile_base, measurement1)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, axes[0], resultsFile_base, measurement2)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  hPlot3 = plot_measurement(fig, axes[0], resultsFile_mpc, measurement1)
  hPlot3[0].set(color = 'magenta', linewidth = 4, linestyle = '--')
  hPlot4 = plot_measurement(fig, axes[0], resultsFile_mpc, measurement2)
  hPlot4[0].set(color = 'green', linewidth = 2, linestyle = '-.')
  hPlot5 = plot_measurement(fig, axes[0], resultsFile_mpc, setpoint)
  hPlot5[0].set(color = 'black', linewidth = 1, linestyle = '-')
  axes[0].set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  axes[0].legend((measurement1 + ' - base case', measurement2 + ' - base case', measurement1 + ' - mpc case', measurement2 + ' - mpc case', setpoint + ' - mpc case'), loc = 'upper right')
  axes[0].grid()
  '''
  # plot air supply temperature
  floor = 2
  zone = 1
  measurement = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  # fig, axes = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, axes[1], resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, axes[1], resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  axes[1].set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - Air supply temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  axes[1].legend(('base case', 'mpc case'), loc = 'upper right')
  axes[1].grid()
  #with mpl.rc_context(rc={'interactive': False}):
  #  plt.show()


  # plot fan power
  floor = 2
  measurement = 'floor' + str(floor) + '_Pfan_y'
  #fig, axes = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, axes[2], resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, axes[2], resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  axes[2].set(title = 'Floor ' + str(floor) + ' - fan power',
           xlabel = 'minute of day', ylabel = 'power [KW]')
  axes[2].legend(('base case', 'mpc case'), loc = 'upper right')
  axes[2].grid()


  floor = 2
  zone = 1
  measurement = 'floor' + str(floor) + '_zon' + str(zone) + '_TRooAir_y'
  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u'
  #fig, axes = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, axes[2], resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, axes[2], resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  #hPlot3 = plot_measurement(fig, axes[2], resultsFile_mpc, setpoint)
  #hPlot3[0].set(color = 'green', linewidth = 2, linestyle = '-.')
  axes[2].set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  axes[2].legend(('y - base case', 'y - mpc case', 'u - mpc case'), loc = 'upper right')
  axes[2].grid()
  '''
  measurement = 'floor' + str(floor) + '_TSupAir_y'
  setpoint = 'floor' + str(floor) + '_aHU_con_oveTSetSupAir_u'
  hPlot1 = plot_measurement(fig, axes[1], resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, axes[1], resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  hPlot3 = plot_measurement(fig, axes[1], resultsFile_mpc, setpoint)
  hPlot3[0].set(color = 'green', linewidth = 2, linestyle = '-.')
  axes[1].set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  axes[1].legend((measurement + ' - base case', measurement + ' - mpc case', setpoint + ' - mpc case'), loc = 'upper right')
  axes[1].grid()
  with mpl.rc_context(rc={'interactive': False}):
    plt.show()

if __name__ == '__main__':
  main()