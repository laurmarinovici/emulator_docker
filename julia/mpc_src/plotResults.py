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
  resultsFile_mpc = './results/run2-mpc/cl_results.csv'

  # comfort_params
  zonetemp_min_occ = 21.11   # (float) lower comfort bound in occupied periods
  zonetemp_max_occ = 23.89   # (float) upper comfort bound in occupied periods
  zonetemp_min_uocc = 15.56  # (float) lower comfort bound in unoccupied periods
  zonetemp_max_uocc = 26.67  # (float) upper comfort bound in unoccupied periods
  startOccTime = 60 * 6 # minute of day occupancy starts, that is 6:00 AM
  endOccTime = 60 * 20 - 1 # minute of day occupancy ends, that is 19:59 
  
  '''
  # plot outside temperature
  measurement = 'TOutDryBul_y'
  fig, axes = plt.subplots(3, 1, figsize = (24, 10))
  hPlot1 = plot_measurement(fig, h1Axes, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h1Axes, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  h1Axes.set(title = 'Outside temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  h1Axes.legend(('base', 'mpc'), loc = 'upper right')
  h1Axes.grid()
  #with mpl.rc_context(rc={'interactive': False}):
  #  plt.show()
'''

  # plot air supply temperature
  floor = 1
  zone = 1
  measurement1 = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  measurement2 = 'floor' + str(floor) + '_zon' + str(zone) + '_TRooAir_y'
  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u'
  fig, (h1Axes, h2Axes) = plt.subplots(2, 1, figsize = (20, 8))
  hPlot2 = plot_measurement(fig, h1Axes, resultsFile_base, measurement1)
  hPlot2[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  #hPlot2 = plot_measurement(fig, h1Axes, resultsFile_base, measurement2)
  #hPlot2[0].set(color = 'blue', linewidth = 2, linestyle = '-')
  hPlot3 = plot_measurement(fig, h1Axes, resultsFile_mpc, measurement1)
  hPlot3[0].set(color = 'magenta', linewidth = 4, linestyle = '--')
  #hPlot4 = plot_measurement(fig, h1Axes, resultsFile_mpc, measurement2)
  #hPlot4[0].set(color = 'red', linewidth = 2, linestyle = '-')
  #hPlot5 = plot_measurement(fig, h1Axes, resultsFile_mpc, setpoint)
  #Plot5[0].set(color = 'black', linewidth = 1, linestyle = '-')
  left, right = h1Axes.get_xlim()
  bottom, top = h1Axes.get_ylim()
  
  hPlot5 = h1Axes.plot(hPlot2[0].get_xdata(), np.concatenate((zonetemp_min_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() <= 60 * 6])), \
          zonetemp_min_occ * np.ones(len(hPlot2[0].get_xdata()[(hPlot2[0].get_xdata() > 60 * 6) * (hPlot2[0].get_xdata() < 60 * 20)])), \
          zonetemp_min_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() >= 60 * 20])))))
  hPlot5[0].set(color = 'black', linewidth = 2, linestyle = '-.')
  hPlot6 = h1Axes.plot(hPlot2[0].get_xdata(), np.concatenate((zonetemp_max_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() <= 60 * 6])), \
          zonetemp_max_occ * np.ones(len(hPlot2[0].get_xdata()[(hPlot2[0].get_xdata() > 60 * 6) * (hPlot2[0].get_xdata() < 60 * 20)])), \
          zonetemp_max_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() >= 60 * 20])))))
  hPlot6[0].set(color = 'black', linewidth = 2, linestyle = '-.')
  h1Axes.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           ylabel = 'temperature [deg C]')
  h1Axes.legend((measurement2 + ' - base', measurement2 + ' - mpc'), loc = 'upper left')
  
  h1Axes.set_xlim(22, right)
  h1Axes.set_ylim(bottom, top)
  xticklabels = []
  for tick in h1Axes.get_xticks():
    xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  h1Axes.set_xticklabels(xticklabels)
  h1Axes.grid()
  
  '''
  # plot air supply temperature
  floor = 2
  zone = 1
  measurement = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  # fig, axes = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, h2Axes, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h2Axes, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  h2Axes.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - Air supply temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  h2Axes.legend(('base', 'mpc'), loc = 'upper right')
  h2Axes.grid()
  #with mpl.rc_context(rc={'interactive': False}):
  #  plt.show()


  # plot fan power
  floor = 2
  measurement = 'floor' + str(floor) + '_Pfan_y'
  #fig, axes = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, h3Axes, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h3Axes, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  h3Axes.set(title = 'Floor ' + str(floor) + ' - fan power',
           xlabel = 'minute of day', ylabel = 'power [KW]')
  h3Axes.legend(('base', 'mpc'), loc = 'upper right')
  h3Axes.grid()


  floor = 2
  zone = 1
  measurement = 'floor' + str(floor) + '_zon' + str(zone) + '_TRooAir_y'
  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u'
  #fig, axes = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, h3Axes, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h3Axes, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  #hPlot3 = plot_measurement(fig, h3Axes, resultsFile_mpc, setpoint)
  #hPlot3[0].set(color = 'green', linewidth = 2, linestyle = '-.')
  h3Axes.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  h3Axes.legend(('y - base', 'y - mpc', 'u - mpc'), loc = 'upper right')
  h3Axes.grid()
  '''

  '''
  measurement = 'floor' + str(floor) + '_TSupAir_y'
  setpoint = 'floor' + str(floor) + '_aHU_con_oveTSetSupAir_u'
  hPlot1 = plot_measurement(fig, h2Axes, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h2Axes, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  hPlot3 = plot_measurement(fig, h2Axes, resultsFile_mpc, setpoint)
  hPlot3[0].set(color = 'green', linewidth = 2, linestyle = '-.')
  h2Axes.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           ylabel = 'temperature [deg C]')
  h2Axes.legend((measurement + ' - base', measurement + ' - mpc', setpoint + ' - mpc'), loc = 'upper left')
  left, right = h2Axes.get_xlim()
  bottom, top = h2Axes.get_ylim()
  h2Axes.set_xlim(22, right)
  h2Axes.set_ylim(10, 30)
  h2Axes.set_xticklabels(xticklabels)
  h2Axes.grid()

  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveHeaOut_u'
  hPlot1 = plot_measurement(fig, h3Axes, resultsFile_mpc, setpoint)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  h3Axes.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - VAV valve',
           xlabel = 'time of day', ylabel = 'fraction')
  h3Axes.legend((setpoint + ' - mpc',), loc = 'upper left') #, bbox_to_anchor=(0, 0))
  left, right = h3Axes.get_xlim()
  bottom, top = h3Axes.get_ylim()
  h3Axes.set_xlim(22, right)
  #h3Axes.set_ylim(0, top)
  h3Axes.set_xticklabels(xticklabels)
  h3Axes.grid()
  '''
  plt.subplots_adjust(hspace = 0.35)
  with mpl.rc_context(rc={'interactive': False}):
    plt.show()

if __name__ == '__main__':
  main()