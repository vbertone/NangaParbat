import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from PyInquirer import prompt
from examples import custom_style_3
from ruamel import yaml
from collections import OrderedDict

import modules.banner as banner
import modules.writemarkdown as writemarkdown
import modules.roman as roman
import modules.utilities as utilities

import modules.bcolours as bcolours
import modules.fitresults as fitresults

from modules.bcolours import *
from validators import *
from modules.fitresults import *


# Print banner
print(banner.reportbanner())

# Folder containing the utilities
CliFolder = os.path.dirname(os.path.realpath(__file__))

# Prompt for output folder
questions = [
    {
        "type": "input",
        "name": "Output folder",
        "message": "Type the name (path) of the input folder for the report (fit result's folder): ",
        "validate": NotOutputFolderValidator,
        "default": "FitResults/fitresults_ceres_unif"
    }
]
answers = prompt(questions, style = custom_style_3)

# Set folder with the info for the report (output of the fit)
outfolder = CliFolder + "/../" + answers["Output folder"]
print(bcolours.ACTREPORT + "Folder with info for the report '" + outfolder + bcolours.ENDC)

# with open(outfolder + "/fitconfig.yaml", "r") as fc:
#     fitconfig = yaml.load(fc, Loader=yaml.RoundTripLoader)
# # important: yaml.load imports yaml files as OrderedDict(iterable, kwargs)
# print(bcolours.ACTREPORT + "Loading fit configuration file '" + outfolder + "/fitconfig.yaml" + bcolours.ENDC)

with open(outfolder + "/tables/config.yaml", "r") as fc:
    config = yaml.load(fc, Loader=yaml.RoundTripLoader)
print(bcolours.ACTREPORT + "Loading tables configuration file '" + outfolder + "/tables/config.yaml" + '\n' + bcolours.ENDC)

# Prompt for report folder
questions = [
    {
        "type": "input",
        "name": "Final report folder",
        "message": "Type a name for the report folder:",
        "validate": OutputFolderValidator,
        "default": "FinalReport"
    }
]
answers = prompt(questions, style = custom_style_3)

# Create report folder
reportnamefolder = answers["Final report folder"]
reportfolder = outfolder + "/" + answers["Final report folder"]
print(bcolours.ACTREPORT + "Creating folder for the final report '" + reportfolder + "'\n " + bcolours.ENDC)
os.mkdir(reportfolder)

# Prompt for report file
questions = [
    {
        "type": "input",
        "name": "Final report file",
        "message": "Type a name for the markdown report (.md):",
        "validate": OutputFolderValidator,
        "default": "FReport.md"
    }
]
answers = prompt(questions, style=custom_style_3)

# Create report file
reportfile = reportfolder + "/" + answers["Final report file"]
print(bcolours.ACTREPORT + "Creating final report file: '" + reportfile + "'\n " + bcolours.ENDC)

# Prompt for the name of the replicas configurations folder
questions = [
    {
        "type": "input",
        "name": "Replicas fitconfig folder",
        "message": "What is the name of the Replicas Configuration folder in the folder of the output of the fit?:",
        # "validate": NotOutputFolderValidator,
        "default": "RRconfig_ceres"
    }
]
answers = prompt(questions, style=custom_style_3)

# Load the configuration file for the central replica
randomreplicasconfig = answers["Replicas fitconfig folder"]
with open(outfolder + "/" + randomreplicasconfig + "/fitconfig_replica_0.yaml", "r") as fc:
    fitconfig = yaml.load(fc, Loader=yaml.RoundTripLoader)
print(bcolours.ACTREPORT + "Loading configuration file of the central replica: '" + outfolder + "/" + randomreplicasconfig + "/fitconfig_replica_0.yaml" + '\n' + bcolours.ENDC)

# Prompt for the description
questions = [
    {
        "type": "input",
        "name": "Report description",
        "message": "Type a description:"
    }
]
answers = prompt(questions, style=custom_style_3)
rdescription = answers["Report description"]


#### Good replicas and cut on the global function
goodreplicas = []
cutgef = 4
replicasfolders = [dir for dir in os.listdir(outfolder) if os.path.isdir(os.path.join(outfolder,dir)) and dir != 'tables' and dir != 'data' and dir != randomreplicasconfig and dir != reportnamefolder]
# Consider only the ones where the minimizer converged and with the cut on the global function
for rf in replicasfolders:
    with open(outfolder + "/" + rf + "/Report.yaml", "r") as rep:
         replica = yaml.load(rep, Loader=yaml.RoundTripLoader)
         status = int(replica["Status"])
         globef = float(replica["Global error function"])
         if status == 1 and globef < cutgef:
            goodreplicas.append(rf)
# # Consider all replicas - uncomment below
# goodreplicas = replicasfolders

# Print the number of good replicas
print(bcolours.REPORT + "\n" + "The replicas that converged and have Global Error Function < " + str(cutgef) + " are: " + bcolours.BOLD + str(len(goodreplicas)) + bcolours.ENDC + bcolours.REPORT + " out of " + bcolours.BOLD + str(len(replicasfolders)) + bcolours.ENDC)

# Get chi2 of the central replica
with open(outfolder + "/" + "replica_0" + "/Report.yaml", "r") as rep0:
    singlereportinforep0 = yaml.load(rep0, Loader=yaml.RoundTripLoader)
    rep0chi2 = singlereportinforep0["Global chi2"]

# Print the final chi2 (of replica 0)
print(bcolours.REPORT + "The chi2 of the central replica is: " + bcolours.BOLD + str(rep0chi2) + "\n " + bcolours.ENDC)

# Write final report in Markdown
# Title
with open(reportfile,"w+") as mdout:
    writemarkdown.mdtitle(mdout, 1, "Final report of the fit with NangaParbat")
    mdout.write("__The final $\chi^2$ is:__ " +  "``" + str(rep0chi2) + "``"  + '\n')
    mdout.write('\n')

# General information from tables/config.yaml
with open(reportfile,"a+") as mdout:
    # mdout.write("Description of the fit: " + fitconfig["Description"] + '\n')
    mdout.write("Description of the fit: " + rdescription + ' \n')
    mdout.write( "This report is related to the output of the fit in the folder: \n " + "``" + outfolder + "``"  + '\n')
    mdout.write('\n')

    mdout.write("The collinear __PDF set__ used for the generation of the tables are: " + "``" + config["pdfset"]["name"] + "``"  + '\n')
    mdout.write('\n')
    mdout.write("The __perturbative order__ is: " + "``" + utilities.GetPertOrd(str(config["PerturbativeOrder"])) + "``"  + '\n')
    mdout.write('\n')
    mdout.write("The number of __replicas__ that __converged__ is: " + "``" + str(len(goodreplicas)) + "``" + " out of " + str(len(replicasfolders)) + '\n')
    mdout.write('\n')

# Tables with general information about the fit
with open(reportfile,"a+") as mdout:
    data = [(fitconfig["Minimiser"],fitconfig["Seed"],fitconfig["qToQmax"],fitconfig["t0prescription"],fitconfig["Parameterisation"])]
    headings = [list(fitconfig.keys())[iter] for iter in range(1, len(data[0])+ 1)]
    writemarkdown.table(mdout, data, headings)

# # Parameterisation latex formula
# with open(reportfile,"a+") as mdout:
#     # unpack the OrderedDict given by GetLatexFormula()
#     key, formula = [x for x in zip(*utilities.GetLatexFormula(fitconfig["Parameterisation"]).items())]
#     # Write in the report
#     mdout.write("The formulas for the " + "``" + fitconfig["Parameterisation"] + "``" + " parameterisation are: " + "\n")
#     for f in formula:
#         mdout.write(f + '\n')
#     mdout.write('\n')

# Parameters
with open(reportfile, "a+") as mdout:
    writemarkdown.mdtitle(mdout, 3, "Parameters")
    writemarkdown.mdtitle(mdout, 4, "T0 parameters")

    # Write as table
    headings = [roman.write_roman(n) for n in range(1, len(fitconfig["t0parameters"]) + 1)]
    par = [tuple(fitconfig["t0parameters"])]
    writemarkdown.table(mdout, par, headings)

    # Write as block
    mdout.write("    " + "t0 parameters = " + str(fitconfig["t0parameters"]) + '\n')

# Table of initial Parameters of replica 0
with open(reportfile,"a+") as mdout:
    # Get parameters in the right format
    headers, rows = utilities.TableOfInitialParameters(fitconfig["Parameters"])
    rows = utilities.GetLatexNames(rows)

    # Write the table for initial parameters
    mdout.write("The __initial parameters__ of the fit for the central replica (__replica 0__) are: " + '\n')
    writemarkdown.table(mdout, rows, headers)

# Table of the Final parameters for the central replica (replica_0)
with open(outfolder + "/" + "replica_0" + "/Report.yaml", "r") as rep0:
    singlereportinforep0 = yaml.load(rep0, Loader=yaml.RoundTripLoader)

    rows = [[] for v in range(len(singlereportinforep0["Parameters"].items()))]
    for v, vir in enumerate(singlereportinforep0["Parameters"].items()):
        rows[v] = vir
    headings = ["name", "value"]
    # Write table
    with open(reportfile,"a+") as mdout:
        mdout.write("The __final parameters__ of the fit for the central replica (__replica 0__) are: " + '\n')
        writemarkdown.table(mdout, rows, headings)

# Create folder for plot.pdf and for plot.png
pdffolder = reportfolder + "/plots"
pngfolder = reportfolder + "/pngplots"
print(bcolours.ACTREPORT + "Creating folder for the plots .pdf '" + pdffolder + "'" + bcolours.ENDC)
os.mkdir(pdffolder)
print(bcolours.ACTREPORT + "Creating folder for the plots .png '" + pngfolder + "'\n " + bcolours.ENDC)
os.mkdir(pngfolder)

############################# Analysis #########################################

# Initialisation of results (object of the class fitresults)
results = fitresults(outfolder, goodreplicas, pdffolder, pngfolder)

# Print on terminal and on the report the minimum chi2
# ! The replicas are not in numerical order !
chi2min = min(results.GlobalChi2())
indexchi2min = results.GlobalChi2().index(min(results.GlobalChi2()))
replicamin = goodreplicas[indexchi2min]

print(bcolours.REPORT + "The minimum global chi2 is: " + bcolours.BOLD + str(chi2min) + bcolours.ENDC + bcolours.REPORT + " and is the one of " + bcolours.BOLD + replicamin + ". \n " + bcolours.ENDC)
with open(reportfile,"a+") as mdout:
    mdout.write("The minimum global chi2 is: " + "``" + str(chi2min) + "``" + "\n ")
    mdout.write( "\n ")

# Write tables of initial and final parameters for replicamin
if replicamin != "replica_0":
    # Table of initial Parameters of replicamin
    with open(reportfile,"a+") as mdout:
        with open(outfolder + "/" + randomreplicasconfig + "/" + "fitconfig_" + replicamin + ".yaml", "r") as repmin_in:
            repminfitconfig = yaml.load(repmin_in, Loader=yaml.RoundTripLoader)

            headers, rows = utilities.TableOfInitialParameters(repminfitconfig["Parameters"])
            # Put the name of the parameters in Latex form
            rows = utilities.GetLatexNames(rows)

            # Write the table for initial parameters
            mdout.write("The __initial parameters__ of the fit for the replica with the __minimum__ chisquare are: " + '\n')
            writemarkdown.table(mdout, rows, headers)

    # Table of the Final parameters for the replica min
    with open(outfolder + "/" + replicamin + "/Report.yaml", "r") as repmin_fin:
        reportreplmin = yaml.load(repmin_fin, Loader=yaml.RoundTripLoader)

        rows = [[] for v in range(len(reportreplmin["Parameters"].items()))]
        for v, vir in enumerate(reportreplmin["Parameters"].items()):
            rows[v] = vir
        headings = ["name", "value"]
        # Write table
        with open(reportfile,"a+") as mdout:
            mdout.write("The __final parameters__ of the fit for the replica with the __minimum__ chisquare are: " + '\n')
            writemarkdown.table(mdout, rows, headings)

#### Global Plots
# Create histograms for global error function and global chi2
results.PlotGlobalErrFunc()
results.PlotGlobalChi2()
results.PlotCutGlobalChi2(1.5, replicamin)

# Include the three histograms in the Markdown report
with open(reportfile,"a+") as mdout:
    writemarkdown.mdincludefig(mdout, "pngplots/GlobalErrorFunction.png", "Global Error functions")
    writemarkdown.mdincludefig(mdout, "pngplots/Globalchi2.png", "Global chi2 ")
    writemarkdown.mdincludefig(mdout, "pngplots/CutGlobalchi2.png", "Cut Global chi2 ")

#### Analysis of the parameters
# Get name of parameteres from the Report.yaml of replica 0
# (any replica does the job, replica 0 is a choice of convenience, could also be replicamin)
with open(outfolder + "/" + "replica_0" + "/Report.yaml", "r") as rep0:
    singlereportinforep0 = yaml.load(rep0, Loader=yaml.RoundTripLoader)

    parameternames = [[] for p in range(len(singlereportinforep0["Parameters"].items()))]
    for p, pns in enumerate(singlereportinforep0["Parameters"].keys()):
        parameternames[p] = pns

with open(reportfile,"a+") as mdout:
    writemarkdown.mdtitle(mdout, 3, "Histograms of the final values of the parameters")

# Creating histograms for the parameters of the fit
for pname in parameternames:
    results.HistoParameter(pname, replicamin)
    if pname == "$N_1$" or pname == "$\sigma$":
        results.LogHistoParameter(pname, replicamin)

    # Remove "\" from the name of the parameter
    parstring = pname.translate({ord('\\'): None})

    # Including the histograms in the report
    with open(reportfile,"a+") as mdout:
        writemarkdown.mdincludefig(mdout, "pngplots/" + parstring + ".png", pname)
        if pname == "$N_1$" or pname == "$\sigma$":
            writemarkdown.mdincludefig(mdout, "pngplots/Log_" + parstring + ".png", pname)

#### Plots for each experiment
with open(reportfile,"a+") as mdout:
    writemarkdown.mdtitle(mdout, 3, "Plots of the experiments")
# Create one set of plots for each experiment
results.PlotExpsResults(replicamin)

# Create list of file names and sort them --- !! requires some time !!
pngfiles = [pngf for pngf in os.listdir(pngfolder) if os.path.isfile(os.path.join(pngfolder + "/", pngf)) and pngf != 'Globalchi2.png' and pngf != 'GlobalErrorFunction.png' and pngf != 'CutGlobalchi2.png' and pngf[0:1] != "$" and pngf[0:3] != "Log"]
pngfiles = sorted(pngfiles)

# Include plots in Markdown report
with open(reportfile,"a+") as mdout:
    for expname in pngfiles:
        writemarkdown.mdincludefig(mdout, "pngplots/" + expname , expname)