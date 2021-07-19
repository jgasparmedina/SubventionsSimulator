"""
SimulatorWeb is based on Flask and provides the web content associated to
the SubventionsSimulator project.

- static folder contains logos, images, css and javascript files.
- templates folder contains html templates based on Flask to serve each different page.
"""
from flask import render_template, request, session
from SubventionsSimulator import Attribute, SubventionsLoader, Simulator, SubventionsDataSample
import configparser
import logging
import flask
import sys

app = flask.Flask(__name__)
# Recommended: in Production define an strong key to encrypt session data.
app.config['SECRET_KEY'] = 'your secret key'

config = configparser.ConfigParser()
config.read("SimulatorWeb.cfg")
if not config.sections():
    print("Fatal error: SimulatorWeb.cfg file is not present or is empty!", file = sys.stderr)

# Define level for the logging.
if config["LOG"]["LEVEL"] == "DEBUG":
    app.logger.setLevel(logging.DEBUG)
elif config["LOG"]["LEVEL"] == "ERROR":
    app.logger.setLevel(logging.ERROR)
elif config["LOG"]["LEVEL"] == "WARNING":
    app.logger.setLevel(logging.WARNING)
else:
    app.logger.setLevel(logging.INFO)

def loadData ():
    global subsSimulator, data
    try:
        # Load Subventions Data and create Subventions Simulator
        filename = config["DATA"]["FILE"]
        app.logger.info("Trying to start SubventionsSimulator from datafile %s" % filename)
        data = SubventionsLoader.SubventionsFileLoader(filename)
        data.load()
        subsSimulator = Simulator.Simulator(data.getSubventions())
        app.logger.info ("SubventionsSimulator succesfully created!")
    except Exception as e:
        app.logger.error("Error creating SubventionsSimulator from file: %s" % e)
        app.logger.info("Creating SubventionsSimulator with sample data")
        from SubventionsSimulator import SubventionsDataSample
        data = SubventionsLoader.SubventionsDictLoader ()
        data.load(SubventionsDataSample.ATRIBUTOS, SubventionsDataSample.AYUDAS)
        subsSimulator = Simulator.Simulator(data.getSubventions())
        app.logger.info("SubventionsSimulator succesfully created!")

loadData()

@app.route("/")
def home():
    """
    Serves the home page and clear the session data.
    :return: the html code for the home page.
    """
    app.logger.info("Serving home.html")
    if 'SIMULATION_IN_PROCESS' in session:
        app.logger.debug("Clearing simulation in process from session data")
        session.pop('SIMULATION_IN_PROCESS')
    if 'NEXT_FIELD' in session:
        app.logger.debug("Clearing next field from session data")
        session.pop('NEXT_FIELD')
    if 'OPTIONS' in session:
        app.logger.debug("Clearing options from session data")
        session.pop('OPTIONS')
    loadData()
    return render_template("home.html")


@app.route("/simulador", methods = ['GET', 'POST'])
def simulator():
    """
    Builds and serves questions or results pages.

    This method manages the simulation process providing html pages
    that request data for each attribute and, when no more attributes
    are pending to ask values, the result page is shown.

    :return: the html code for the next question page or the page with
     the subvention results.
    """
    app.logger.debug("Simulador called!")
    # If no simulation in process we start a new one
    if 'SIMULATION_IN_PROCESS' not in session:
        session['SIMULATION_IN_PROCESS'] = True
        # Simulation for one specific subvention
        if request.args.get('idSubvention', None):
            app.logger.info("Starting new simulation for idSubvention --> %s", request.args.get('idSubvention', None))
            subsSimulator.startSimulation([int(request.args.get('idSubvention', None))])
        # Simulation for all available subventions
        else:
            app.logger.info("Starting new simulation for all subventions")
            subsSimulator.startSimulation()
        # Getting next attribute and serving it
        attribute = subsSimulator.getNextAttribute()
        session['NEXT_FIELD'] = attribute.getName()
        session['OPTIONS'] = attribute.getValues()
        app.logger.debug("Serving questions.html with field %s and options %s" % (attribute.getName(), attribute.getValues()))
        # Serving questions.html page with data associated to the requested attribute
        return render_template("questions.html", fieldName = attribute.getName(), question = attribute.getQuestion(), options = attribute.getValues(), helpers = attribute.getHelpers(),
                               fieldType = attribute.getType(), help = attribute.getHelp(), remainingFields = subsSimulator.getPendingAttributes())

    # If the last attribute is numerical, we've to process it getting the information from the form
    if request.method == 'POST':
        app.logger.debug("Get float value %s for field %s" % (int(request.form['float_field']), session['NEXT_FIELD']))
        subsSimulator.setAttributeData(session['NEXT_FIELD'], int(request.form['float_field']))
    # In other case we get the info from the arguments of the url
    else:
        if request.args.get('idAttribute') and request.args.get('idOption'):
            app.logger.debug("Get value %s for field %s" % (session['OPTIONS'][int(request.args.get('idOption'))], session['NEXT_FIELD']))
            subsSimulator.setAttributeData(session['NEXT_FIELD'], session['OPTIONS'][int(request.args.get('idOption'))])
        else:
            app.logger.debug("Nothing to do in simulador!")
            app.logger.info("Simulation has been restarted")
            session.pop('SIMULATION_IN_PROCESS')
            session.pop('NEXT_FIELD')
            session.pop('OPTIONS')
            return simulator ()
    # If there is no additional attributes to asking for, we clear the session data and serve the result page.
    if subsSimulator.isFinished():
        app.logger.info("Simulation finished!")
        session.pop('SIMULATION_IN_PROCESS')
        session.pop('NEXT_FIELD')
        session.pop('OPTIONS')
        subventionsOk = []
        for subventionId in subsSimulator.getSubventionsOk():
            subventionsOk.append({'ID': subventionId,
                                  'TITLE': data.getSubvention(subventionId).getTitle(),
                                  'DESCRIPTION': data.getSubvention(subventionId).getDescription(),
                                  'LAW': data.getSubvention(subventionId).getLaw(),
                                  'LAW_URL': data.getSubvention(subventionId).getLawURL(),
                                  'REQUEST': data.getSubvention(subventionId).getRequestURL(),
                                  'INCOMPATIBILITIES': data.getSubvention(subventionId).getIncompatibilities()})
        app.logger.info("Serving simulation_results.html with results: %s" % subsSimulator.getSubventionsOk())
        return render_template("simulation_results.html", subventions = subventionsOk)
    # In other case, we continue with the simulation serving the next attribute to ask for.
    else:
        attribute = subsSimulator.getNextAttribute()
        session['NEXT_FIELD'] = attribute.getName()
        session['OPTIONS'] = attribute.getValues()
        app.logger.debug("Serving questions.html with field %s and options %s" % (attribute.getName(), attribute.getValues()))
        return render_template("questions.html", fieldName = attribute.getName(), question = attribute.getQuestion(), options = attribute.getValues(), helpers = attribute.getHelpers(),
                               fieldType = attribute.getType(), help = attribute.getHelp(), remainingFields = subsSimulator.getPendingAttributes())


@app.route("/catalogo")
def browseSubventions():
    """
    Builds and serves the page with all the available subventions.

    This method builds one web page that includes all configured subventions
    with its different associated links.

    :return: the html code for the full catalogue of configured
     subventions.
    """
    subventions = []
    for subventionId in data.getSubventions():
        if data.getSubvention(subventionId).getActive():
            subventions.append({'ID': subventionId,
                                'TITLE': data.getSubvention(subventionId).getTitle(),
                                'DESCRIPTION': data.getSubvention(subventionId).getDescription(),
                                'LAW': data.getSubvention(subventionId).getLaw(),
                                'LAW_URL': data.getSubvention(subventionId).getLawURL(),
                                'REQUEST': data.getSubvention(subventionId).getRequestURL(),
                                'INCOMPATIBILITIES': data.getSubvention(subventionId).getIncompatibilities()})
    app.logger.info("Serving subventions.html")
    return render_template("subventions.html", subventions = subventions)


if __name__ == '__main__':
    """
    Main function which launches the Flask Server 
    """
    app.run()
