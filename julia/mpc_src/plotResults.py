import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_measurement(fig, Axis, dataFile, measurement):
  data = pd.read_csv(dataFile)
  measInd = np.where(data.columns.values == measurement)
  timeInd = np.where(data.columns.values == 'minute_of_day')
  measValues = data.values[:, measInd[0][0]]
  timeValues = data.values[:, timeInd[0][0]]
  hPlot = Axis.plot(timeValues, measValues)
  return hPlot

def main():
  resultsFile_base = './results/run2-base-case/cl_results.csv'
  resultsFile_mpc = './results/run3-mpc/cl_results.csv'

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
  fig, Axis = plt.subplots(3, 1, figsize = (24, 10))
  hPlot1 = plot_measurement(fig, h1Axis, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h1Axis, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  h1Axis.set(title = 'Outside temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  h1Axis.legend(('base', 'mpc'), loc = 'upper right')
  h1Axis.grid()
  #with mpl.rc_context(rc={'interactive': False}):
  #  plt.show()
'''

  # plot air supply temperature
  floor = 1
  zone = 1
  measurement1 = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  measurement2 = 'floor' + str(floor) + '_zon' + str(zone) + '_TRooAir_y'
  measurement3 = 'heatsp'
  measurement4 = 'coolsp'
  
  fig, (h1Axis, h2Axis) = plt.subplots(2, 1, figsize = (20, 8))
  hPlot2 = plot_measurement(fig, h1Axis, resultsFile_base, measurement2)
  hPlot2[0].set(color = 'blue', linewidth = 2, linestyle = '-')
  
  hPlot4 = plot_measurement(fig, h1Axis, resultsFile_mpc, measurement2)
  hPlot4[0].set(color = 'red', linewidth = 2, linestyle = '-')
  left, right = h1Axis.get_xlim()
  bottom, top = h1Axis.get_ylim()
  
  hPlot5 = plot_measurement(fig, h1Axis, resultsFile_mpc, measurement3)
  #h1Axis.plot(hPlot2[0].get_xdata(), np.concatenate((zonetemp_min_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() <= 60 * 6])), \
  #        zonetemp_min_occ * np.ones(len(hPlot2[0].get_xdata()[(hPlot2[0].get_xdata() > 60 * 6) * (hPlot2[0].get_xdata() < 60 * 20)])), \
  #        zonetemp_min_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() >= 60 * 20])))))
  hPlot5[0].set(color = 'black', linewidth = 2, linestyle = '-.')
  hPlot6 = plot_measurement(fig, h1Axis, resultsFile_mpc, measurement4)
  #h1Axis.plot(hPlot2[0].get_xdata(), np.concatenate((zonetemp_max_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() <= 60 * 6])), \
  #        zonetemp_max_occ * np.ones(len(hPlot2[0].get_xdata()[(hPlot2[0].get_xdata() > 60 * 6) * (hPlot2[0].get_xdata() < 60 * 20)])), \
  #        zonetemp_max_uocc * np.ones(len(hPlot2[0].get_xdata()[hPlot2[0].get_xdata() >= 60 * 20])))))
  hPlot6[0].set(color = 'black', linewidth = 2, linestyle = '-.')
  h1Axis.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - room temperature',
           ylabel = 'temperature [deg C]')
  h1Axis.legend((measurement2 + ' - base', measurement2 + ' - mpc'), loc = 'upper left')
  h1Axis.set_xlim(22, right)
  #h1Axis.set_ylim(bottom, top)
  xticklabels = []
  for tick in h1Axis.get_xticks():
    xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  h1Axis.set_xticklabels(xticklabels)
  h1Axis.grid()
  
  hPlot1 = plot_measurement(fig, h2Axis, resultsFile_base, measurement1)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot3 = plot_measurement(fig, h2Axis, resultsFile_mpc, measurement1)
  hPlot3[0].set(color = 'red', linewidth = 4, linestyle = '-')
  h2Axis.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - supply temperature',
           ylabel = 'temperature [deg C]')
  left, right = h2Axis.get_xlim()
  bottom, top = h2Axis.get_ylim()
  h2Axis.legend((measurement1 + ' - base', measurement1 + ' - mpc'), loc = 'upper left')
  h2Axis.set_xlim(22, right)
  #h1Axis.set_ylim(bottom, top)
  xticklabels = []
  for tick in h2Axis.get_xticks():
    xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  h2Axis.set_xticklabels(xticklabels)
  h2Axis.grid()

  # =============================================
  setpointAHU = 'floor' + str(floor) + '_aHU_con_oveTSetSupAir_u'
  setpointZone = []
  for zone in range(1, 6):
    setpointZone.append('floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u')
  hFig, hAxis = plt.subplots(1, 1, figsize = (20, 8))
  h1Plot = plot_measurement(hFig, hAxis, resultsFile_mpc, setpointAHU)
  h1Plot[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hAxis.set(title = 'Floor ' + str(floor) + ' - AHU and zone supply setpoints',
           ylabel = 'temperature [deg C]')
  legendText = []
  legendText.append(setpointAHU)
  hPlot = []
  for setpoint in setpointZone:
    h = plot_measurement(hFig, hAxis, resultsFile_mpc, setpoint)
    hPlot.append(h)
    hPlot[setpointZone.index(setpoint)][0].set(linewidth = 2, linestyle = '-.')
    legendText.append(setpoint)
  left, right = hAxis.get_xlim()
  bottom, top = hAxis.get_ylim()
  hAxis.legend((legendText), loc = 'upper right')
  hAxis.set_xlim(24, right)
  hAxis.set_ylim(min(hPlot[0][0].get_ydata()[24:]) - 1, max(hPlot[0][0].get_ydata()) + 1)
  xticklabels = []
  for tick in hAxis.get_xticks():
    xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  hAxis.set_xticklabels(xticklabels)
  hAxis.grid()
  
  # ===================================================================
  measurement5 = 'floor' + str(floor) + '_TSupAir_y'
  fig, h1Axis = plt.subplots(1, 1, figsize = (20, 8))
  hPlot2 = plot_measurement(fig, h1Axis, resultsFile_mpc, measurement5)
  hPlot2[0].set(color = 'blue', linewidth = 2, linestyle = '-')
  hPlot4 = plot_measurement(fig, h1Axis, resultsFile_mpc, setpointAHU)
  hPlot4[0].set(color = 'red', linewidth = 2, linestyle = '-')
  left, right = h1Axis.get_xlim()
  bottom, top = h1Axis.get_ylim()
  h1Axis.set(title = 'Floor ' + str(floor) + ' - AHU supply temperature',
           ylabel = 'temperature [deg C]')
  h1Axis.legend((measurement5 + ' - mpc', setpointAHU + ' - mpc'), loc = 'upper left')
  h1Axis.set_xlim(22, right)
  h1Axis.set_ylim(10, top)
  xticklabels = []
  for tick in h1Axis.get_xticks():
    xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  h1Axis.set_xticklabels(xticklabels)
  h1Axis.grid()

  #hPlot5 = plot_measurement(fig, h1Axis, resultsFile_mpc, setpoint)
  #Plot5[0].set(color = 'black', linewidth = 1, linestyle = '-')

  '''
  # plot air supply temperature
  floor = 2
  zone = 1
  measurement = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  # fig, Axis = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, h2Axis, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h2Axis, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  h2Axis.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - Air supply temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  h2Axis.legend(('base', 'mpc'), loc = 'upper right')
  h2Axis.grid()
  #with mpl.rc_context(rc={'interactive': False}):
  #  plt.show()


  # plot fan power
  floor = 2
  measurement = 'floor' + str(floor) + '_Pfan_y'
  #fig, Axis = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, h3Axis, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h3Axis, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '--')
  h3Axis.set(title = 'Floor ' + str(floor) + ' - fan power',
           xlabel = 'minute of day', ylabel = 'power [KW]')
  h3Axis.legend(('base', 'mpc'), loc = 'upper right')
  h3Axis.grid()


  floor = 2
  zone = 1
  measurement = 'floor' + str(floor) + '_zon' + str(zone) + '_TRooAir_y'
  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u'
  #fig, Axis = plt.subplots(1, 1, figsize = (12, 5))
  hPlot1 = plot_measurement(fig, h3Axis, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h3Axis, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  #hPlot3 = plot_measurement(fig, h3Axis, resultsFile_mpc, setpoint)
  #hPlot3[0].set(color = 'green', linewidth = 2, linestyle = '-.')
  h3Axis.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  h3Axis.legend(('y - base', 'y - mpc', 'u - mpc'), loc = 'upper right')
  h3Axis.grid()
  '''

  '''
  measurement = 'floor' + str(floor) + '_TSupAir_y'
  setpoint = 'floor' + str(floor) + '_aHU_con_oveTSetSupAir_u'
  hPlot1 = plot_measurement(fig, h2Axis, resultsFile_base, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  hPlot2 = plot_measurement(fig, h2Axis, resultsFile_mpc, measurement)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  hPlot3 = plot_measurement(fig, h2Axis, resultsFile_mpc, setpoint)
  hPlot3[0].set(color = 'green', linewidth = 2, linestyle = '-.')
  h2Axis.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - temperature',
           ylabel = 'temperature [deg C]')
  h2Axis.legend((measurement + ' - base', measurement + ' - mpc', setpoint + ' - mpc'), loc = 'upper left')
  left, right = h2Axis.get_xlim()
  bottom, top = h2Axis.get_ylim()
  h2Axis.set_xlim(22, right)
  h2Axis.set_ylim(10, 30)
  h2Axis.set_xticklabels(xticklabels)
  h2Axis.grid()

  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveHeaOut_u'
  hPlot1 = plot_measurement(fig, h3Axis, resultsFile_mpc, setpoint)
  hPlot1[0].set(color = 'blue', linewidth = 4, linestyle = '-')
  h3Axis.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - VAV valve',
           xlabel = 'time of day', ylabel = 'fraction')
  h3Axis.legend((setpoint + ' - mpc',), loc = 'upper left') #, bbox_to_anchor=(0, 0))
  left, right = h3Axis.get_xlim()
  bottom, top = h3Axis.get_ylim()
  h3Axis.set_xlim(22, right)
  #h3Axis.set_ylim(0, top)
  h3Axis.set_xticklabels(xticklabels)
  h3Axis.grid()
  '''
  plt.subplots_adjust(hspace = 0.35)
  with mpl.rc_context(rc={'interactive': False}):
    plt.show()

if __name__ == '__main__':
  main()