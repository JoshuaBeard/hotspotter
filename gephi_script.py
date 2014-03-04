#/usr/local/bin/jython
#from os.path import expanduser; f = open(expanduser('~/code/hotspotter/gephi_script.py')); exec(f.read()); f.close()
#

'''
(<type 'org.gephi.filters.FilterControllerImpl'>, 'FilterController')
(<type 'java.lang.Class'>, 'ClockwiseRotate')
(<type 'java.lang.Class'>, 'Contract')
(<type 'java.lang.Class'>, 'CounterClockwiseRotate')
(<type 'java.lang.Class'>, 'Expand')
(<type 'java.lang.Class'>, 'ForceAtlas')
(<type 'java.lang.Class'>, 'ForceAtlas2')
(<type 'java.lang.Class'>, 'FruchtermanReingold')
(<type 'java.lang.Class'>, 'LabelAdjust')
(<type 'java.lang.Class'>, 'Lookup')
(<type 'java.lang.Class'>, 'RandomLayout')
(<type 'java.lang.Class'>, 'YifanHu')
(<type 'java.lang.Class'>, 'YifanHuMultiLevel')
(<type 'java.lang.Class'>, 'YifanHuProportional')
(<type 'function'>, 'addFilter')
(<type 'function'>, 'add_filter')
(<type 'function'>, 'center')
(<type 'function'>, 'exportGraph')
(<type 'function'>, 'getEdgeAttributes')
(<type 'function'>, 'getLayoutBuilders')
(<type 'function'>, 'getNodeAttributes')
(<type 'function'>, 'get_edge_attributes')
(<type 'function'>, 'get_layout_builders')
(<type 'function'>, 'get_node_attributes')
(<type 'function'>, 'importGraph')
(<type 'function'>, 'resetSelection')
(<type 'function'>, 'runLayout')
(<type 'function'>, 'run_layout')
(<type 'function'>, 'selectEdges')
(<type 'function'>, 'selectNodes')
(<type 'function'>, 'selectSubGraph')
(<type 'function'>, 'selectSubgraph')
(<type 'function'>, 'select_edges')
(<type 'function'>, 'select_nodes')
(<type 'function'>, 'select_sub_graph')
(<type 'function'>, 'select_subgraph')
(<type 'function'>, 'setVisible')
(<type 'function'>, 'set_visible')
(<type 'function'>, 'stopLayout')
(<type 'function'>, 'stop_layout')
(<type 'classobj'>, 'Console')
(<type 'javapackage'>, 'java')
(<type 'javapackage'>, 'org')
(<type 'org.gephi.scripting.wrappers.GyGraph'>, 'g')
(<type 'org.gephi.scripting.wrappers.GyGraph'>, 'graph')
(<type 'instance'>, 'console')
(<type 'org.gephi.io.importer.impl.ImportControllerImpl'>, 'ImportController')
(<type 'org.gephi.layout.LayoutControllerImpl'>, 'LayoutController')
(<type 'org.gephi.project.impl.ProjectControllerImpl'>, 'ProjectController')
(<type 'org.gephi.io.exporter.impl.ExportControllerImpl'>, 'ExportController')
(<type 'org.gephi.visualization.VizController'>, 'VizController')
'''
#from os.path import *; execfile(expanduser('~/code/hotspotter/gephi_script.py'))

'''

jython -Dpython.path=gephi-toolkit.jar

'''

import java
from os.path import *  # NOQA
import sys


def ensure_gephi_toolkit_jar():
    print('[init] ensuring gephi tookit')
    jarname = 'gephi-toolkit.jar'
    if jarname in map(lambda path: split(path)[1], sys.path):
        print(' * gephi toolkit is already in path')
        return
    cwd = os.path.dirname(os.path.realpath(__file__))
    toolkit = os.path.join(cwd, 'gephi-toolkit.jar')
    if not exists(toolkit):
        toolkit = os.path.join(os.getcwd(), jarname)
    sys.path.append(toolkit)
    print(' * found gephi')


import org.openide.util.Lookup as Lookup
Lookup = Lookup.getDefault().lookup


#https://github.com/jsundram/pygephi/blob/master/gephi.py
def lookup(name, namespace='org.gephi.'):
    classname = namespace + name
    print('[init] lookup: %s' % classname)
    javaclass = java.lang.Class.forName(classname)
    return Lookup(javaclass)


try:
    ProjectController
    print('We are running in from gephi')
except NameError:
    print('We are running in from command line')
    import org.gephi.project.api as project
    import org.gephi.data.attributes.api as attributes
    import org.gephi.filters.api as filters
    import org.gephi.graph.api as graph
    import org.gephi.io.exporter.api as exporter
    import org.gephi.io.generator.api as generator
    import org.gephi.io.importer.api as importer
    import org.gephi.layout.api as layout
    import org.gephi.partition.api as partition
    import org.gephi.preview as preview
    import org.gephi.project.api as project
    import org.gephi.ranking.api as ranking
    import org.gephi.statistics as statistics
    import org.gephi.utils as utils
    ensure_gephi_toolkit_jar()
    ProjectController = lookup('project.api.ProjectController')
    ExportController  = lookup('io.exporter.api.ExportController')
    ImportController  = lookup('io.importer.api.ImportController')
    GraphController   = lookup('graph.api.GraphController')
    PreviewController = lookup('preview.api.PreviewController')
    #from org.openide.util import Lookup
    #import java.lang.Class
    #import org.gephi.project.api.ProjectController as ProjectController
    #pc = Lookup.getDefault().lookup(java.lang.Class.forName("org.gephi.project.api.ProjectController"))


def rrr():
    execfile(expanduser('~/code/hotspotter/gephi_script.py'))

if not 'DEVLOCALS' in vars():
    DEVLOCALS = {}
    DEVLOCALS['ISINIT'] = False
    DEVLOCALS['DB'] = ''


def print_available():
    local_items = locals().items()
    item_tuples = []
    for key, val in local_items:
        if not isinstance(val, java.awt.Color):
            item_tuples += [(type(val), key)]
    sorted_items = sorted(item_tuples)
    print('\n'.join(map(str, sorted_items)))

# Useful variables
#ProjectController.newProject()

# pc = Lookup.getDefault().lookup(ProjectController.class)
pc = ProjectController
viz = VizController
lc = LayoutController

proj = pc.getCurrentProject()
wspace = pc.getCurrentWorkspace()
#wspace.init(proj)

#pc.cleanWorkspace(wspace)
cfg = viz.getVizConfig()
vizmodel = viz.getVizModel()
text_model = vizmodel.getTextModel()
graphio = viz.getGraphIO()
modelClassLib = viz.getModelClassLibrary()


def get_gml_fpath():
    gml_fname = 'GZ_ALL_cgraph_netx.gml'
    #gml_fname = 'HSDB_zebra_with_mothers_cgraph_netx.gml'
    DEVLOCALS['DB'] = gml_fname
    gml_dir = expanduser('~/code/hotspotter/graphs/')
    gml_fpath = join(gml_dir, gml_fname)
    return gml_fpath


def ImportCustomGML():
    global DEVLOCALS
    if DEVLOCALS['ISINIT'] is False:
        print('ImportCustomGML() ... opening')
        importGraph(get_gml_fpath())
        DEVLOCALS['ISINIT'] = True
        return True
    else:
        print('ImportCustomGML() ... already open')
        return False
    #gml_file = java.io.File(get_gml_fpath())
    #containter = ImportController.importFile(gml_file)
    #ImportController.process(containter)  # returns void


def centerOnGraph():
    import org.gephi.visualization.VizController as VIZ
    viz = VIZ.getInstance()
    #import org.gephi.project.api.ProjectController as pc
    viz.getGraphIO().centerOnGraph()
    viz.getEngine().getScheduler().requireUpdateVisible()


def SetCustomVizParams():
    print('SetCustomVizParams()')
    # No Hulls
    viz.vizModel.setShowHulls(False)
    # Smaller edges
    #vizmodel.setEdgeScale(.878)
    vizmodel.setEdgeScale(1.3)
    # Dark background
    vizmodel.setBackgroundColor(black)
    # View the name of the animal nodes
    node_attrs = getNodeAttributes()
    if 'name' in node_attrs:
        name_attr = node_attrs['name']
        name_col = name_attr.underlyingAttributeColumn
        viz.textManager.model.nodeTextColumns[0] = name_col
    # Show animal names
    text_model.setShowNodeLabels(True)
    # Smaller font
    fontsize = 32
    try:
        smallfont = java.awt.Font('Mono Dyslexic', 0, fontsize)
        text_model.setNodeFont(smallfont)
    except Exception:
        print(ex)
        smallfont = java.awt.Font('Arial', 0, fontsize)
        text_model.setNodeFont(smallfont)
    #text_model.setNodeColor(orange)


#def CustomForceParamsBAD(layout):
    #layout.maxDisplacement = 1e2
    #layout.repulsionStrength = 1e3
    #layout.attractionStrength = 1e-2
    #layout.gravity = 1e4
    #layout.freezeStrength = 1e2  # autostab strength
    #layout.freezeInertia = 1e2  # Autostab sensitivity
    #layout.cooling = 1e0
    #layout.inertia = 1e0
    #layout.speed = 1e2


def CustomForceParams(layout):
    layout.maxDisplacement = 1e2
    layout.repulsionStrength = 5e4
    layout.attractionStrength = .8e-3
    layout.gravity = -1e4
    layout.freezeStrength = 1e2  # autostab strength
    layout.freezeInertia = 1e0  # Autostab sensitivity
    layout.cooling = 1e0
    layout.inertia = 1e0
    layout.speed = 5.5e-4
    if DEVLOCALS['DB'] == 'HSDB_zebra_with_mothers_cgraph_netx.gml':
        layout.speed = 5.5e-6
        layout.repulsionStrength = 5e6
        layout.attractionStrength = .8e-2
        layout.gravity = -1e3



if ImportCustomGML():
    SetCustomVizParams()
else:
    print('stopping layout')
    stopLayout()

#stopLayout()
#lc.model.loadProperties(layout)
#centerOnGraph()
#stopLayout()

#text_model.setTextColumns()
#ImportController.getFileImporter(gml_fpath)
# Viz Config


def interpolateColor(alpha, color2, color1):
    red   = (alpha * float(color1.red))   + ((1.0 - alpha) * float(color2.red))
    green = (alpha * float(color1.green)) + ((1.0 - alpha) * float(color2.green))
    blue  = (alpha * float(color1.blue))  + ((1.0 - alpha) * float(color2.blue))
    color3 = java.awt.Color(int(red), int(green), int(blue))
    return color3


scale = 'linear'
if scale == 'log10':
    from math import log10
    scalefn = lambda num: log10(num)
if scale == 'log':
    from math import log
    scalefn = lambda num: log(num)
elif scale == 'linear':
    scalefn = lambda num: num


def CustomEdgeColors():
    print('Getting min max weight')
    minWeight = 1e29
    maxWeight = -1e29

    meansum = 0.0
    for edge in graph.edges:
        meansum += edge.weight
        if edge.weight < minWeight:
            minWeight = edge.weight
        if edge.weight > maxWeight:
            maxWeight = edge.weight
    stddevsum = 0.0
    mean = meansum / float(len(graph.edges))
    for edge in graph.edges:
        stddevsum += (mean - edge.weight) ** 2
    stddevsum = stddevsum / float(len(graph.edges))
    from math import sqrt
    std = sqrt(stddevsum)
    print('std = %r, mean = %r' % (std, mean))
    # Remove outliers
    MAXTHRESH = mean + 5.5 * std
    maxWeight = min(MAXTHRESH, maxWeight)
    for edge in graph.edges:
        edge.weight = min(MAXTHRESH, edge.weight)
    #maxWeight = min(1e4, maxWeight)
    minWeight = float(minWeight)
    maxWeight = float(maxWeight)
    print('minWeight, maxWeight = %r, %r' % (minWeight, maxWeight))
    #shift2 = .01
    shift2 = 1
    min_ = scalefn(minWeight)
    max_ = scalefn(maxWeight)
    max_ = (shift2 * (max_ - min_)) + min_
    range_ = max_ - min_
    #print('range_ = %r' % range_)
    edge_list = graph.edges
    def interpolateEdge(edge):
        #alpha = min(1, max(0, alpha))
        weight = scalefn(edge.weight)
        alpha = (weight - min_) / (max_ - min_)
        alpha = max(0.0, min(1.0, alpha))
        #if alpha < 0 or alpha > 1:
            #raise AssertionError('alpha not in range')
        color = interpolateColor(alpha, blue, orange)
        edge.color = color
        return alpha, color, weight
    alpha_list = []
    weight_list = []
    color_list = []
    for edge in edge_list:
        alpha, color, weight = interpolateEdge(edge)
        color_list.append(color)
        weight_list.append(weight)
        alpha_list.append(alpha)

    print('alpha_list %r' % alpha_list[1:100:5])
    #print('weight_list %r' % weight_list[1:100:10])
    #print('color_list %r' % color_list[1:100:10])
    print('Setting Edge Colors')
    print('Set Colors: %r' % shift2)


CustomEdgeColors()
try:
    layout
except Exception:
    forces_ = ForceAtlas()
    layout  = forces_.buildLayout()

selected_layout = lc.model.getSelectedLayout()
print('selected_layout: %r' % selected_layout)
print('  custom_layout: %r' % layout)
if not selected_layout is None:
    layout = selected_layout
CustomForceParams(layout)
lc.setLayout(layout)
print('Running Layout')
#run_layout(layout.getBuilder, iters=100)
#run_layout(layout.getBuilder)
print('Done')


def doForce():
    #org.gephi.layout.plugin.forceAtlas.
    import org.gephi.layout.plugin.forceAtlas2.ForceAtlas2Builder
    runLayout(org.gephi.layout.plugin.forceAtlas2.ForceAtlas2Builder)
    stopLayout()