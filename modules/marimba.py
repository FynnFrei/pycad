import FreeCAD as App
import Part
import ObjectsFem
import Sketcher
import FreeCADGui


FreeCADGui.showMainWindow()

'''
class Marimba:
    def __init__(self, x, y, z):
        self._doc = App.newDocument()

    def save(self, path: str):
        self._doc.saveAs(path)
'''

# make new doc:
doc = App.newDocument()

# declare variables
x1, x2, x3, x4, x5, x6, x7 = 0, 0, 0, 0, 0, 0, 0
yFirst, y2, y3, y4, y5, y6, yLast = 0, 0, 0, 0, 0, 0, 0
yFirstNum = 3   # Line number of the first bottom line
yLastNum = 10    # Line number of the last bottom Line
marimbaWidth, marimbaLength, marimbaHeight = 0, 0, 0

def marimba_sketch():
    sketch = doc.addObject("Sketcher::SketchObject", "Sketch")

    # Add LieSegments:
    line0 = sketch.addGeometry(
        Part.LineSegment(App.Vector(0, 0, 0),
                         App.Vector(1, 1, 0)),
        False)
    line1 = sketch.addGeometry(
        Part.LineSegment(App.Vector(1, 1, 0),
                         App.Vector(2, 2, 0)),
        False)
    line2 = sketch.addGeometry(
        Part.LineSegment(App.Vector(2, 2, 0),
                         App.Vector(3, 3, 0)),
        False)
    line3 = sketch.addGeometry(
        Part.LineSegment(App.Vector(3, 3, 0),
                         App.Vector(4, 4, 0)),
        False)
    line4 = sketch.addGeometry(
        Part.LineSegment(App.Vector(4, 4, 0),
                         App.Vector(5, 5, 0)),
        False)
    line5 = sketch.addGeometry(
        Part.LineSegment(App.Vector(5, 5, 0),
                         App.Vector(6, 6, 0)),
        False)
    line6 = sketch.addGeometry(
        Part.LineSegment(App.Vector(6, 6, 0),
                         App.Vector(7, 7, 0)),
        False)
    line7 = sketch.addGeometry(
        Part.LineSegment(App.Vector(7, 7, 0),
                         App.Vector(8, 8, 0)),
        False)
    line8 = sketch.addGeometry(
        Part.LineSegment(App.Vector(8, 8, 0),
                         App.Vector(9, 9, 0)),
        False)
    line9 = sketch.addGeometry(
        Part.LineSegment(App.Vector(9, 9, 0),
                         App.Vector(10, 10, 0)),
        False)
    line10 = sketch.addGeometry(
        Part.LineSegment(App.Vector(10, 10, 0),
                         App.Vector(11, 11, 0)),
        False)
    # All the LineSegmets are linked:
    sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1)) # Example: Line 0, Vertex 2 is linked with Line 1, Vertex 1
    sketch.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 2, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 2, 2, 3, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 3, 2, 4, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 4, 2, 5, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 5, 2, 6, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 6, 2, 7, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 7, 2, 8, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 8, 2, 9, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 9, 2, 10, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 10, 2, 0, 1))
    # Fix Line0, Vertex1 to origin:
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 0, 1, App.Units.Quantity('0 mm')))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", 0, 1, App.Units.Quantity('0 mm')))
    # Geometric constraints:
    sketch.addConstraint(Sketcher.Constraint("Vertical", line0))
    sketch.addConstraint(Sketcher.Constraint("Perpendicular", line0, line1))
    sketch.addConstraint(Sketcher.Constraint("Vertical", line2))
    sketch.addConstraint(Sketcher.Constraint('Horizontal', line3))
    # Dimensional constraints:
    # fixed:
    sketch.addConstraint(Sketcher.Constraint('Distance', 0, 1, 0, 2, App.Units.Quantity(marimbaHeight)))
    sketch.addConstraint(Sketcher.Constraint('Distance', 1, 1, 1, 2, App.Units.Quantity(marimbaLength)))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", yFirstNum, 1, App.Units.Quantity(yFirst)))  # yFirst should not be changed but is defined to keep order
    sketch.addConstraint(Sketcher.Constraint("DistanceY", yLastNum, 1, App.Units.Quantity(yLast)))  # yLast should not be changed but is defined to keep order
    # Variable vertices:
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 4, 1, App.Units.Quantity(x1)))
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 5, 1, App.Units.Quantity(x2)))
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 6, 1, App.Units.Quantity(x3)))
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 7, 1, App.Units.Quantity(x4)))
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 8, 1, App.Units.Quantity(x5)))
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 9, 1, App.Units.Quantity(x6)))
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 10, 1, App.Units.Quantity(x7)))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", 5, 1, App.Units.Quantity(y2)))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", 6, 1, App.Units.Quantity(y3)))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", 7, 1, App.Units.Quantity(y4)))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", 8, 1, App.Units.Quantity(y5)))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", 9, 1, App.Units.Quantity(y6)))


# extrude sketch to 3D Part:
def marimba_extrude():
    doc.addObject('Part::Extrusion', 'Bar')
    f = doc.getObject('Bar')
    f.Base = doc.getObject('Sketch')
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = marimbaWidth
    f.LengthRev = 0.000000000000000
    f.Solid = True
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle = 0.000000000000000
    f.TaperAngleRev = 0.000000000000000


def marimba_femgui():
    import FemGui
    # make Analysis
    analysis_object = ObjectsFem.makeAnalysis(doc, 'Analysis')
    FemGui.setActiveAnalysis(doc.ActiveObject)

    # solver
    solver_object = ObjectsFem.makeSolverCalculixCcxTools(doc)
    solver_object.EigenmodesCount = 6
    solver_object.GeometricalNonlinearity = 'linear'
    solver_object.ThermoMechSteadyState = False
    solver_object.MatrixSolverType = 'default'
    solver_object.IterationsControlParameterTimeUse = False
    analysis_object.addObject(solver_object)

    # material
    FemGui.getActiveAnalysis().addObject(ObjectsFem.makeMaterialSolid(doc, 'MaterialSolid'))
    doc.Analysis.addObject(doc.ActiveObject)
    mat = doc.ActiveObject.Material
    mat['Name'] = "Wood-Palissander"
    mat['YoungsModulus'] = "15500 MPa"
    mat['PoissonRatio'] = ".030"
    mat['Density'] = "730 kg/m^3"
    mat['UltimateTensileStrength'] = "5.90 MPa"
    mat['ShearModulus'] = "8.3 MPa"
    doc.ActiveObject.Material = mat
    analysis_object.addObject(doc.ActiveObject)

    # fixed_constraint
    fixed_constraint = ObjectsFem.makeConstraintFixed(doc, "FemConstraintFixed")
    fixed_constraint.References = [(doc.Bar, ("Face4", "Face11"))]
    analysis_object.addObject(fixed_constraint)

    # netgen
    mesh_object = doc.addObject('Fem::FemMeshShapeNetgenObject', 'FEMMeshNetgen')
    mesh_object.Shape = doc.Bar
    mesh_object.MaxSize = 10
    mesh_object.Fineness = "VeryFine"
    mesh_object.Optimize = True
    mesh_object.SecondOrder = True
    doc.recompute()
    analysis_object.addObject(mesh_object)


def marimba_femrun():
    # run the analysis all in one
    from femtools import ccxtools
    fea = ccxtools.FemToolsCcx()
    fea.update_objects()
    fea.setup_working_dir()
    fea.setup_ccx()
    message = fea.check_prerequisites()
    if not message:
        fea.purge_results()
        fea.write_inp_file()
        # on error at inp file writing, the inp file path "" was returned (even if the file was written)
        # if we would write the inp file anyway, we need to again set it manually
        # fea.inp_file_name = '/tmp/FEMWB/FEMMeshGmsh.inp'
        fea.ccx_run()
        fea.load_results()
    else:
        print("Houston, we have a problem! {}\n".format(message))  # in Python console


if __name__ == "__main__":
    print('hi')
