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
  hPlot = Axis.step(timeValues, measValues)
  return hPlot

def plot_status(fig, Axis, dataFile, measurement, statusType, mark):
  data = pd.read_csv(dataFile)
  measInd = np.where(data.columns.values == measurement)
  statusInd = np.where(data.columns.values == 'status')
  timeInd = np.where(data.columns.values == 'minute_of_day')
  measValues = data.values[:, measInd[0][0]]
  statusValues = data.values[:, statusInd[0][0]]
  desiredStatusInd = np.where(statusValues == statusType)
  timeValues = data.values[:, timeInd[0][0]]
  hPlot = Axis.plot(timeValues[desiredStatusInd], measValues[desiredStatusInd])
  hPlot[0].set(marker = mark, markersize = 6, linestyle = 'None')
  return hPlot

def main():
  figWidth = 10
  figHeight = 8

  resultsFile_base = './results/run2-base-case/cl_results.csv'
  resultsFile_mpc = './results/run10-mpc-10/cl_results.csv'

  # comfort_params
  zonetemp_min_occ = 21.11   # (float) lower comfort bound in occupied periods
  zonetemp_max_occ = 23.89   # (float) upper comfort bound in occupied periods
  zonetemp_min_uocc = 15.56  # (float) lower comfort bound in unoccupied periods
  zonetemp_max_uocc = 26.67  # (float) upper comfort bound in unoccupied periods
  startOccTime = 60 * 6 # minute of day occupancy starts, that is 6:00 AM
  endOccTime = 60 * 20 - 1 # minute of day occupancy ends, that is 19:59 
  
  
  # plot outside temperature
  measurementOutside = 'TOutDryBul_y'
  '''
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

  # =========== Figure 1 ============
  # plot air supply temperature
  floor = 1
  zone = 1
  measurement1 = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  measurement2 = 'floor' + str(floor) + '_zon' + str(zone) + '_TRooAir_y'
  measurement3 = 'heatsp'
  measurement4 = 'coolsp'
  
  fig, (h1Axis, h2Axis) = plt.subplots(2, 1, figsize = (figWidth, figHeight))
  hPlot2 = plot_measurement(fig, h1Axis, resultsFile_base, measurement2)
  hPlot2[0].set(color = 'blue', linewidth = 2, linestyle = '-')
  
  hPlot7 = plot_measurement(fig, h1Axis, resultsFile_base, measurementOutside)
  hPlot7[0].set(color = 'magenta', linewidth = 2, linestyle = '-')

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
  #for tick in h1Axis.get_xticks():
  #  xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  #h1Axis.set_xticklabels(xticklabels)
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
  #for tick in h2Axis.get_xticks():
  #  xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  #h2Axis.set_xticklabels(xticklabels)
  h2Axis.grid()

  # =============================================
  setpointAHU = 'floor' + str(floor) + '_aHU_con_oveTSetSupAir_u'
  setpointZone = []
  for zone in range(1, 6):
    setpointZone.append('floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u')
  hFig, hAxis = plt.subplots(1, 1, figsize = (figWidth, figHeight))
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
  #for tick in hAxis.get_xticks():
  #  xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  #hAxis.set_xticklabels(xticklabels)
  hAxis.grid()
  
  # ===================================================================
  measurement5 = 'floor' + str(floor) + '_TSupAir_y'
  fig, h1Axis = plt.subplots(1, 1, figsize = (figWidth, figHeight))
  hPlot2 = plot_measurement(fig, h1Axis, resultsFile_mpc, measurement5)
  hPlot2[0].set(color = 'blue', linewidth = 2, linestyle = '-')
  hPlot4 = plot_measurement(fig, h1Axis, resultsFile_mpc, setpointAHU)
  hPlot4[0].set(color = 'red', linewidth = 2, linestyle = '-')
  hPlot5 = plot_status(fig, h1Axis, resultsFile_mpc, setpointAHU, 'LOCALLY_SOLVED', 'o')
  hPlot6 = plot_status(fig, h1Axis, resultsFile_mpc, setpointAHU, 'ITERATION_LIMIT', 'd')
  hPlot7 = plot_status(fig, h1Axis, resultsFile_mpc, setpointAHU, 'ALMOST_LOCALLY_SOLVED', '*')
  left, right = h1Axis.get_xlim()
  bottom, top = h1Axis.get_ylim()
  h1Axis.set(title = 'Floor ' + str(floor) + ' - AHU supply temperature',
           ylabel = 'temperature [deg C]')
  h1Axis.legend((measurement5 + ' - mpc', setpointAHU + ' - mpc', 'LOCALLY_SOLVED', 'ITERATION_LIMIT', 'ALMOST_LOCALLY_SOLVED'), loc = 'upper left')
  h1Axis.set_xlim(22, right)
  h1Axis.set_ylim(10, top)
  xticklabels = []
  #for tick in h1Axis.get_xticks():
  #  xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  #h1Axis.set_xticklabels(xticklabels)
  h1Axis.grid()

  #hPlot5 = plot_measurement(fig, h1Axis, resultsFile_mpc, setpoint)
  #Plot5[0].set(color = 'black', linewidth = 1, linestyle = '-')

  # =========================================================================
  # plot air supply temperature
  zone = 1
  hFig = []
  hPlot = []
  hAxis = []
  legendText = []
  measurement = 'floor' + str(floor) + '_zon' + str(zone) + '_TSupAir_y'
  setpoint = 'floor' + str(floor) + '_zon' + str(zone) + '_oveTSetDisAir_u'
  hFig, hAxis = plt.subplots(1, 1, figsize = (figWidth, figHeight))
  hPlot1 = plot_measurement(hFig, hAxis, resultsFile_mpc, measurement)
  hPlot1[0].set(color = 'blue', linewidth = 2, linestyle = '-')
  legendText.append(measurement + ' - mpc')
  hPlot2 = plot_measurement(hFig, hAxis, resultsFile_mpc, setpoint)
  hPlot2[0].set(color = 'red', linewidth = 2, linestyle = '-')
  legendText.append(setpoint + ' - mpc')
  hPlot3 = plot_measurement(hFig, hAxis, resultsFile_mpc, measurement3)
  hPlot3[0].set(color = 'black', linewidth = 2, linestyle = '--')
  legendText.append(measurement3)
  hPlot4 = plot_measurement(hFig, hAxis, resultsFile_mpc, measurement4)
  hPlot4[0].set(color = 'black', linewidth = 2, linestyle = '--')
  legendText.append(measurement4)
  hAxis.set(title = 'Floor ' + str(floor) + ' / Zone ' + str(zone) + ' - Air supply temperature',
           xlabel = 'minute of day', ylabel = 'temperature [deg C]')
  left, right = hAxis.get_xlim()
  bottom, top = hAxis.get_ylim()
  hAxis.legend((measurement + ' - mpc', setpoint + ' - mpc'), loc = 'upper right')
  hAxis.set_xlim(24, right)
  hAxis.set_ylim(min(np.minimum(hPlot1[0].get_ydata()[24:], hPlot3[0].get_ydata()[24:])) - 1, max(np.maximum(hPlot1[0].get_ydata()[24:], hPlot4[0].get_ydata()[24:])) + 1)
  hAxis.grid()
  
  # =========================================================================
  setpointZone = []
  hPlot=[]
  hFig = []
  hAxis = []
  legendText = []
  for zone in range(1, 6):
    setpointZone.append('floor' + str(floor) + '_zon' + str(zone) + '_oveHeaOut_u')
  hFig, hAxis = plt.subplots(1, 1, figsize = (figWidth, figHeight))
  for setpoint in setpointZone:
    h = plot_measurement(hFig, hAxis, resultsFile_mpc, setpoint)
    hPlot.append(h)
    hPlot[setpointZone.index(setpoint)][0].set(linewidth = 2, linestyle = '-')
    legendText.append(setpoint)
  left, right = hAxis.get_xlim()
  bottom, top = hAxis.get_ylim()
  hAxis.legend((legendText), loc = 'upper right')
  hAxis.set_xlim(24, right)
  hAxis.set_ylim(min(hPlot[0][0].get_ydata()[24:]) - 1, max(hPlot[0][0].get_ydata()) + 1)
  xticklabels = []
  #for tick in hAxis.get_xticks():
  #  xticklabels.append(str(int(divmod(tick, 60)[0])) + ':' + str(int(divmod(tick, 60)[1])))
  #hAxis.set_xticklabels(xticklabels)
  hAxis.grid()

  # ======= energy consumption ======
  measurementPChiller = 'PChi_y'
  measurementPPump = 'PPum_y'
  measurementPFan = []
  hPlot=[]
  hFig = []
  hAxis = []
  legendText = []
  for floor in range (1, 4):
    measurementPFan.append('floor' + str(floor) + '_Pfan_y')
  hFig, hAxis = plt.subplots(1, 1, figsize = (figWidth, figHeight))
  hPlot1 = plot_measurement(hFig, hAxis, resultsFile_mpc, measurementPChiller)
  hPlot1[0].set(color = 'red', linewidth = 2, linestyle = '-')
  legendText.append(measurementPChiller)
  hPlot2 = plot_measurement(hFig, hAxis, resultsFile_mpc, measurementPPump)
  hPlot2[0].set(color = 'blue', linewidth = 2, linestyle = '-')
  legendText.append(measurementPPump)
  left, right = hAxis.get_xlim()
  bottom, top = hAxis.get_ylim()
  hAxis.legend((legendText), loc = 'upper left')
  hAxis.set_xlim(24, right)
  hAxis.grid()

  hAxis = []
  hPlot = []
  legendText = []
  hFig, hAxis = plt.subplots(1, 1, figsize = (figWidth, figHeight))
  for meas in measurementPFan:
    h = plot_measurement(hFig, hAxis, resultsFile_mpc, meas)
    hPlot.append(h)
    hPlot[measurementPFan.index(meas)][0].set(linewidth = 2, lineStyle = '-')
    legendText.append(meas)
  left, right = hAxis.get_xlim()
  bottom, top = hAxis.get_ylim()
  hAxis.legend((legendText), loc = 'upper left')
  hAxis.set_xlim(24, right)
  # hAxis.set_ylim(min(hPlot[0][0].get_ydata()[24:]) - 1, max(hPlot[0][0].get_ydata()) + 1)
  hAxis.grid()

  plt.subplots_adjust(hspace = 0.35)
  with mpl.rc_context(rc={'interactive': False}):
    plt.show()

if __name__ == '__main__':
  main()