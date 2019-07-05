# GENERAL PACKAGE IMPORT
# ----------------------
println("Loading packages ......")
using HTTP, JSON, CSV, DataFrames, Dates, Printf, DelimitedFiles, MathOptInterface
const MOI = MathOptInterface
println("Including other functions ....")
# import the Julia script with the optimization model and associated dependencies
include("functions.jl")

# defining the possible optimization solver status, in order to make decissions
# on how to proceed further
status_goodSolution = [MOI.OPTIMAL, MOI.LOCALLY_SOLVED, MOI.ALMOST_OPTIMAL]
status_badSolution = [MOI.ALMOST_LOCALLY_SOLVED, MOI.INFEASIBLE, MOI.DUAL_INFEASIBLE, MOI.LOCALLY_INFEASIBLE, MOI.INFEASIBLE_OR_UNBOUNDED, MOI.ALMOST_INFEASIBLE, MOI.ALMOST_DUAL_INFEASIBLE]
status_userLim = [MOI.ITERATION_LIMIT, MOI.TIME_LIMIT, MOI.NODE_LIMIT, MOI.SOLUTION_LIMIT, MOI.MEMORY_LIMIT, MOI.OBJECTIVE_LIMIT, MOI.NORM_LIMIT, MOI.OTHER_LIMIT]

println("Create output folder ....")
# create directory to store MPC results
dirpath = createdir()
println("Find results in : ", dirpath)
# initialize counters
sample = 1           # counter (index) for the samples (integer)
minute = 1.0          # counter (index)  for time in minute (float)
sampling_timer = 0   # counts time during which setpoints are not updated
# define quantities related to simulation horizon
start_minute = o.cl_startday * 24 * 60.0
end_minute = start_minute + o.cl_numdays * 24 * 60.0
nompc_minute = start_minute + o.cl_nompcdays * 24 * 60.0
# Setup JModelica case
# --------------------
# Set URL for jmodelica model simulation
JModelicaLocation = string("http://", conn.ip, ":", conn.port)
simTimeLength = o.cl_numdays * 3600 # JModelica simulation length in seconds (not used at this time)
simTimeStep = o.cl_minPerSample * 60 # JModelica simulation step in seconds

# Get JModelica simulation model
# ---------------
mutable struct Case
    name::String
    inputs
    measurements
    step_def::Float64
    Case() = new()
end
case = Case()
getCaseInfo(JModelicaLocation, case)
println("JModelica case information from $JModelicaLocation")
println("\tName: $(case.name)")
println("\tNumber of control inputs: $(Int64((length(case.inputs) - 1) / 2))")
println("\tNumber of measurements: $(length(case.measurements))")
# println("\tList of control inputs:\t$(case.inputs)")
writedlm("inputList-20190705.csv", sort!(case.inputs), ", ")
# println("\tList of measurements:\t$(case.measurements)")
writedlm("measurementList-20190705.csv", sort!(case.measurements), ", ")

println("\tDefault simulation step: $(case.step_def)")

global dfCurrentSetpoints = DataFrames.DataFrame()
global dfCurrentMeasurements = DataFrames.DataFrame()
global dfAllInputs = DataFrames.DataFrame()
# Run Case
#----------
start = Dates.now() # this time type includes date and time
sim_start = Base.Libc.time() # epoch time in seconds
# Reset test case
println("Resetting test case if needed.") # Looks like it gets reset no matter what!!!!!!!
res = HTTP.put("$JModelicaLocation/reset",["Content-Type" => "application/json"], JSON.json(Dict("start" => 0 + 200 * 86400)))
println("Running test case ...")
# Set simulation step
println("Setting simulation step to $simTimeStep")
res = HTTP.put("$JModelicaLocation/step",["Content-Type" => "application/json"], JSON.json(Dict("step" => simTimeStep)))
global originalMaxIter = o.maxiter
# simulation loop
while minute <= end_minute - start_minute
    loopStartTime = Base.Libc.time()
    @printf("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    @printf("Minute %d loop started at %s.\n", minute, Base.Libc.strftime(loopStartTime))
    # initialize dataframe for storing data (measurements + setpoints)
    # df = DataFrames.DataFrame()
    # update counters before next sampling period

    if minute == 1.0
        global u = ctrlInitialize(case.inputs)
        # the following set points are added for data analysis later; their values are not relevant when going with default controller
        for floor = 1 : p.numfloors
            for zone = 1 : p.numzones
                u["floor$(floor)_zon$(zone)_oveTSetDisAir_activate"] = 0
                u["floor$(floor)_zon$(zone)_oveTSetDisAir_u"] = 1e-27
            end
        end
        global dfCurrentSetpoints = dict2df!(dfCurrentSetpoints, u)
        # println(u)
    end
    # println(length(u))
    # println(u)
    tempStartTime = Base.Libc.time()
    res = HTTP.post("$JModelicaLocation/advance", ["Content-Type" => "application/json"], JSON.json(u);retry_non_idempotent=true).body
    currMeasurements = JSON.parse(String(res))
    @printf("Emulator current measurement time, minute: %d\n", values(currMeasurements["time"]) / 60)
    global dfCurrentMeasurements = dict2df!(dfCurrentMeasurements, currMeasurements)
    tempEndTime = Base.Libc.time()
    @printf("Minute %d ADVANCE EMULATOR ended at %s, after %.4f seconds.\n", minute, Base.Libc.strftime(tempEndTime), tempEndTime - tempStartTime)

    # res = HTTP.get("$JModelicaLocation/results", ["Content-Type" => "application/json"]).body
    # allInputs = JSON.parse(String(res))["u"];
    # global dfAllInputs = dict2df!(dfAllInputs, allInputs)
    # extract relevant time information
    current_minute = start_minute + minute      # current clock time (in minute)
    timedata = timeinfo(current_minute)         # dictionary contaning relevant time info
    minute_of_day = timedata["minute_of_day"]   # minute of the day ∈ (1, …, 1440)
    hour_of_day = timedata["hour_of_day"]       # hour of the day ∈ (1, …, 24)
    @printf("\tSimulation minute: %d\n", minute)
    @printf("\tHour of day: %d\n", hour_of_day)
    @printf("\tMinute of the hour: %d\n", minute_of_day%60 != 0 ? minute_of_day%60 : 60)
    # dfCurrentMeasurements stores previous measurements to compute internal loads (using moving average model)
    global dfCurrentMeasurements_history = minute == 1.0 ? dfCurrentMeasurements : updatehistory!(dfCurrentMeasurements_history, dfCurrentMeasurements) # note df_history only requires "updated" measurements, not setpoints

    # obtain heating (lower bound) and cooling (upper bound) setpoints (in Celsius) over prediction horizon (1D array)
    h, c =  comfortbounds(current_minute)
    # obtain predicted outside-air temps in Celsius (1D array)
    @printf("Current measurement for outside temperature : %.2f Kelvin (%.2f Celsius).\n", dfCurrentMeasurements[1, :TOutDryBul_y], dfCurrentMeasurements[1, :TOutDryBul_y] - 273.15)
    tempStartTime = Base.Libc.time()
    pred_oat = predictambient(dfCurrentMeasurements[1, :TOutDryBul_y], minute_of_day)
    tempEndTime = Base.Libc.time()
    @printf("Minute %d PREDICT AMBIENT TEMPERATURE ended at %s, after %.4f seconds.\n", minute, Base.Libc.strftime(tempEndTime), tempEndTime - tempStartTime)
    # obtain internal loads for each zone (3D array)
    tempStartTime = Base.Libc.time()
    pred_load = predictloads(dfCurrentMeasurements_history)
    tempEndTime = Base.Libc.time()
    @printf("Minute %d PREDICT LOAD ended at %s, after %.4f seconds.\n", minute, Base.Libc.strftime(tempEndTime), tempEndTime - tempStartTime)

    # dictionary of computed MPC params
    mpc_params = Dict("heat_sp" => h, "cool_sp" => c, "pred_oat" => pred_oat, "pred_loads" => pred_load)

    # convert temperature measurements from Kelvin to Celsius
    dfCurrentMeasurements = kelvintocelsius!(dfCurrentMeasurements)

    ####################################################################
    # CASE 1: DEFAULT CONTROL (NO OVERRIDE)
    ####################################################################
    if (minute <= nompc_minute - start_minute + 1.0 * o.cl_nosolvewindow)
        # message
        defaultNoOveStartTime = Base.Libc.time()
        printmessage(sample, sampling_timer, data_type = "overrides", control = "DEFAULT")

        # store arbitrary values for overrides (required mainly for data storage later)
        dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, control = "DEFAULT")

        # message
        println("Sending default setpoints for minute = $minute ...")
        # send back data (with no overrides); basically, using the same control input u
        u = df2dict!(u, dfCurrentSetpoints)
        # solution info
        solverinfo = Dict("optcost" => 1e-27, "status" => "N/A", "soltime" => 1e-27)

        # all important info
        global allinfo = Dict("solverinfo" => solverinfo, "timedata" => timedata,
        "mpcparams" => mpc_params, "sample" => sample, "controller" => "DEFAULT", "MPC stage" => "n/a")
        defaultNoOveEndTime = Base.Libc.time()
        @printf("Minute %d DEFAULT/NO OVERRIDE ended at %s, after %.4f seconds.\n", minute, Base.Libc.strftime(defaultNoOveEndTime), defaultNoOveEndTime - defaultNoOveStartTime)

    ####################################################################
    # CASE 2: MPC CONTROL (OVERRIDE ON)
    ####################################################################
    else
        # check if the last computed setpoints can be implemented
        ####################################################################
        # CASE 2a): IMPLEMENT LAST COMPUTED SETPOINTS
        ####################################################################
        if (1 <= sampling_timer <= o.cl_nosolvewindow)
            mpcNoOptStartTime = Base.Libc.time()
            # message
            printmessage(sample, sampling_timer, data_type = "overrides", control = "MPC")

            if in(currMPCStatus, status_goodSolution)
              # store current overrides
              if o.mpcMovingBlockImpl
                global currMPCStage = allinfo["MPC stage"] + 1
                @printf("<<<<< MPC MOVING BLOCK Implementation - Using stage %d of the MPC prediction horizon. >>>>>\n", currMPCStage)
                global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, control = "MPC", stage = currMPCStage)
              else
                global currMPCStage = 1
                @printf("<<<<< MPC NON-MOVING BLOCK Implementation - Using stage %d of the MPC prediction horizon. >>>>>\n", currMPCStage)
                global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, control = "MPC", stage = currMPCStage)
              end
            else
              global currMPCStage = "n/a"
              @printf("<<<<< MPC failed this time, so going with last computed setpoints. >>>>>>>\n")
              # store previously computed MPC overrides
              global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, dfPastSetpoints, minute_of_day, control = "MPC")
            end
            # store previously computed MPC overrides
            # global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, dfPastSetpoints, minute_of_day, control = "MPC")

            # solution info
            solverinfo = Dict("optcost" => 1e-27, 
                              "status" => "no-solve",
                              "soltime" => 1e-27)
            global allinfo["MPC stage"] = currMPCStage
            mpcNoOptEndTime = Base.Libc.time()
            @printf("Minute %d MPC/NO OPTIMIZATION ended at %s, after %.4f seconds.\n", minute, Base.Libc.strftime(mpcNoOptEndTime), mpcNoOptEndTime - mpcNoOptStartTime)

        # else solve MPC
        ####################################################################
        # CASE 2B): SOLVE MPC AND USE NEWLY COMPUTED SETPOINTS
        ####################################################################
        else
            mpcOptStartTime = Base.Libc.time()
            @printf("<<<<< Solve MPC to get new setpoints. >>>>>>>\n")
            # display message
            printmessage(sample, sampling_timer, data_type = "overrides", control = "MPC", optimize = "Yes")

            # update MPC model parameters
            updatemodelparams(dfCurrentMeasurements, mpc_params)

            # solve MPC model
            global solverinfo = solvemodel()
            @printf("================= Quick statistics of optimization algorithms. =============\n")
            @printf("Going for %d max iterations.\n", o.maxiter)
            # println(JuMP.SimplexIterations(m))
            #println(MOI.get(m, MOI.SimplexIterations()))
            @printf("Optimization took %.4f seconds, and ended with status %s.\n", solverinfo["soltime"], solverinfo["status"])
            #@printf("size of ahusupplytemp: %d, %d, %d\n", size(ahusupplytemp, 1), size(ahusupplytemp, 2), size(ahusupplytemp, 3))
            #@printf("size of ahudamper: %d, %d, %d\n", size(ahudamper, 1), size(ahudamper, 2), size(ahudamper, 3))
            #@printf("size of zonedischargetemp: %d, %d, %d\n", size(zonedischargetemp, 1), size(zonedischargetemp, 2), size(zonedischargetemp, 3))
            #@printf("size of zoneflow: %d, %d, %d\n", size(zoneflow, 1), size(zoneflow, 2), size(zoneflow, 3))
            #@printf("size of ahupressures: %d, %d, %d\n", size(ahupressures, 1), size(ahupressures, 2), size(ahupressures, 3))
            #@printf("size of zonetemp: %d, %d, %d\n", size(zonetemp, 1), size(zonetemp, 2), size(zonetemp, 3))
            for f = 1 : p.numfloors
                @printf("floor %d -> ahusupplytemp = %.4f, constrain: [%.2f, %.2f]\n", f, JuMP.value(ahusupplytemp[f, 1]), p.ahusupplytemp_min, p.ahusupplytemp_max)
                @printf("floor %d -> ahudamper = %.4f, constrain: [%.2f, %2f]\n", f, JuMP.value(ahudamper[f, 1]), p.damper_min, p.damper_max)
                for z = 1 : p.numzones
                    @printf("floor %d, zone %d -> zonedischargetemp = %.4f, constrain: [%.2f, %2f]\n", f, z, JuMP.value(zonedischargetemp[f, z, 1]), JuMP.value(ahusupplytemp[f, 1]), p.zonedischargetemp_max)
                    @printf("floor %d, zone %d -> zoneflow = %.4f, constrain: [%.2f, %2f]\n", f, z, JuMP.value(zoneflow[f, z, 1]), p.zoneflow_min[z], p.zoneflow_max[z])
                    @printf("floor %d, zone %d -> reheat valve opening = %.4f, constrain: [%.2f, %2f]\n", f, z, JuMP.value(zoneflow[f, z, 1])/p.zoneflow_max[z], p.zoneflow_min[z]/p.zoneflow_max[z], p.zoneflow_max[z]/p.zoneflow_max[z])
                end
            end
            global currMPCStatus = solverinfo["status"]
            if in(solverinfo["status"], status_goodSolution)
              # store current overrides
              global currMPCStage = 1
              @printf("Using stage %d of the MPC prediction horizon.\n", currMPCStage)
              global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, control = "MPC", stage = currMPCStage)
              @printf("<<<<<<< RE-INITIALIZE THE MODEL WITH THE LAST VALUES OF THE PREVIOUS SOLVER. >>>>>>>\n")
              JuMP.set_start_value.(JuMP.all_variables(m), JuMP.value.(JuMP.all_variables(m)))
              o.maxiter = originalMaxIter
              @printf("New max iteration number: %d.\n", o.maxiter)
            elseif solverinfo["status"] == status_userLim[1] # MOI.ITERATION_LIMIT
              global currMPCStage = "n/a"
              @printf("<<<<< THIS TIME: USER MAXIMUM ITERATION NUMBER REACHED. >>>>>>>\n")
              @printf("<<<<<<< RE-INITIALIZE THE MODEL WITH THE LAST VALUES OF THE PREVIOUS SOLVER. >>>>>>>\n")
              JuMP.set_start_value.(JuMP.all_variables(m), JuMP.value.(JuMP.all_variables(m)))
              # store previously computed MPC overrides
              global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, dfPastSetpoints, minute_of_day, control = "MPC")
              o.maxiter += 100
              @printf("New max iteration number: %d.\n", o.maxiter)
            elseif in(solverinfo["status"], status_badSolution)
              global currMPCStage = "n/a"
              @printf("Optimization algorithm terminated with INFEASIBLE or UNBOUNDED solution.\n")
              @printf("<<<<<<< RE-INITIALIZE THE MODEL WITH THE LAST VALUES OF THE PREVIOUS SOLVER. >>>>>>>\n")
              JuMP.set_start_value.(JuMP.all_variables(m), JuMP.value.(JuMP.all_variables(m)))
              # store previously computed MPC overrides
              global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, dfPastSetpoints, minute_of_day, control = "MPC")
            elseif in(solverinfo["status"], status_userLim[2:end])
              global currMPCStage = "n/a"
              @printf("<<<<<<< SOME OTHER SORT OF LIMIT HAS BEEN REACHED, that is %s. >>>>>>>>>>", string(solverinfo["status"]))
              @printf("<<<<<<< RE-INITIALIZE THE MODEL WITH THE LAST VALUES OF THE PREVIOUS SOLVER. >>>>>>>\n")
              JuMP.set_start_value.(JuMP.all_variables(m), JuMP.value.(JuMP.all_variables(m)))
              # store previously computed MPC overrides
              global dfCurrentSetpoints = setoverrides!(dfCurrentSetpoints, dfPastSetpoints, minute_of_day, control = "MPC")
            end
            mpcOptEndTime = Base.Libc.time()
            @printf("Minute %d MPC/OPTIMIZATION ended at %s, after %.4f seconds.\n", minute, Base.Libc.strftime(mpcOptEndTime), mpcOptEndTime - mpcOptStartTime)
        end

        # all mpc info
        global allinfo = Dict("solverinfo" => solverinfo,
                       "timedata" => timedata,
                       "mpcparams" => mpc_params,
                       "sample" => sample,
                       "controller" => "MPC",
                       "MPC stage" => currMPCStage)

        # send back data (with overrides)
        u = df2dict!(u, dfCurrentSetpoints) # u

        # update sampling timer counter
        global sampling_timer = sampling_timer + 1 > o.cl_nosolvewindow ? 0 : sampling_timer + 1
    end

    # store current setpoints for future use
    global dfPastSetpoints = deepcopy(dfCurrentSetpoints)

    global sample += 1
    global minute += 1.0
    
    loopEndTime = Base.Libc.time()
    @printf("Minute %d loop ended at %s, after %.4f seconds.\n", minute - 1, Base.Libc.strftime(loopEndTime), loopEndTime - loopStartTime)
    global allinfo["loopTime"] = loopEndTime - loopStartTime
    
    # save results for current sampling period
    saveStartTime = Base.Libc.time()
    saveresults(dfCurrentMeasurements, dfCurrentSetpoints, allinfo, dirpath)
    saveEndTime = Base.Libc.time()
    @printf("Minute %d saving ended at %s, after %.4f seconds.\n", minute - 1, Base.Libc.strftime(saveEndTime), saveEndTime - saveStartTime)
    int_sim_end = Base.Libc.time()
    int_sim_time = int_sim_end - sim_start # in seconds
    int_sim_days = div(int_sim_time, 24 * 60 * 60)
    int_sim_hours = div(int_sim_time - int_sim_days * 24 * 60 * 60, 60 * 60)
    int_sim_min = div(int_sim_time - int_sim_days * 24 * 60 * 60 - int_sim_hours * 60 * 60, 60)
    int_sim_sec = rem(int_sim_time - int_sim_days * 24 * 60 * 60 - int_sim_hours * 60 * 60 - int_sim_min * 60, 60)
    @printf("So far, the simulation took %d days, %d hours, %d minutes and %.2f seconds.\n", int_sim_days, int_sim_hours, int_sim_min, int_sim_sec)
end
sim_end = Base.Libc.time()
sim_time = sim_end - sim_start # in seconds
sim_days = div(sim_time, 24 * 60 * 60)
sim_hours = div(sim_time - sim_days * 24 * 60 * 60, 60 * 60)
sim_min = div(sim_time - sim_days * 24 * 60 * 60 - sim_hours * 60 * 60, 60)
sim_sec = rem(sim_time - sim_days * 24 * 60 * 60 - sim_hours * 60 * 60 - sim_min * 60, 60)
@printf("The whole simulation took %d days, %d hours, %d minutes and %.2f seconds.\n", sim_days, sim_hours, sim_min, sim_sec)
#
#################### End of main loop ###########################################################
#################################################################################################

# combine result for each sampling time into one aggregated file
#=
numsamples = sample - 1
combineresults(dirpath, numsamples)
=#