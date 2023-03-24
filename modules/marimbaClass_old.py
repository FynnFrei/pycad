import os
import random
import FreeCAD as App
import Part
import ObjectsFem
import Sketcher
import FreeCADGui
FreeCADGui.showMainWindow()
import FemGui


class Marimba:
    def __init__(self, marimbaLength, marimbaWidth, marimbaHeight, groundLength, x2, x3, x4, x5, x6, x7, x8, x9, y2, y3,
                 y4, y5, y6, y7, y8, y9):
        # make new doc:
        self.doc = App.newDocument()

        # declare variables
        self.marimbaLength, self.marimbaWidth, self.marimbaHeight = marimbaLength, marimbaWidth, marimbaHeight
        self.x2, self.x3, self.x4, self.x5, self.x6, self.x7, self.x8, self.x9 = x2, x3, x4, x5, x6, x7, x8, x9
        self.groundLength = groundLength
        self.xFirst = self.marimbaLength - self.groundLength
        self.xLast = self.groundLength
        self.xFirstNum = 4
        self.xLastNum = 13
        self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9 = y2, y3, y4, y5, y6, y7, y8, y9
        self.yFirst, self.yLast = 0, 0  # Should be 0
        self.yFirstNum = 3  # Line number of the first bottom line
        self.yLastNum = 13  # Line number of the last bottom Line

        self.eigenmodesCount = 10    # Number of calculated Eigenmodes

    def recompute(self):
        self.doc.recompute()

    def save(self, path: str):
        self.doc.saveAs(path)

    def marimba_sketch(self):
        sketch = self.doc.addObject("Sketcher::SketchObject", "Sketch")
        sketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000),
                                         App.Rotation(0.707107, 0.000000, 0.000000, 0.707107))

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
        line11 = sketch.addGeometry(
            Part.LineSegment(App.Vector(11, 11, 0),
                             App.Vector(12, 12, 0)),
            False)
        line12 = sketch.addGeometry(
            Part.LineSegment(App.Vector(12, 12, 0),
                             App.Vector(13, 13, 0)),
            False)
        line13 = sketch.addGeometry(
            Part.LineSegment(App.Vector(13, 13, 0),
                             App.Vector(14, 14, 0)),
            False)

        # All the LineSegmets are linked:
        # Example1: Line 0, Vertex 2 is linked with Line 1, Vertex 1
        sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 2, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 2, 2, 3, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 3, 2, 4, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 4, 2, 5, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 5, 2, 6, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 6, 2, 7, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 7, 2, 8, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 8, 2, 9, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 9, 2, 10, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 10, 2, 11, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 11, 2, 12, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 12, 2, 13, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 13, 2, 0, 1))
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
        sketch.addConstraint(Sketcher.Constraint('Distance', 0, 1, 0, 2, App.Units.Quantity(self.marimbaHeight)))
        sketch.addConstraint(Sketcher.Constraint('Distance', 1, 1, 1, 2, App.Units.Quantity(self.marimbaLength)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", self.xFirstNum, 1, App.Units.Quantity(self.xFirst)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", self.xLastNum, 1, App.Units.Quantity(self.xLast)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", self.yFirstNum, 1, App.Units.Quantity(self.yFirst)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", self.yLastNum, 1, App.Units.Quantity(self.yLast)))
        # Variable vertices:
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 5, 1, App.Units.Quantity(self.x2)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 6, 1, App.Units.Quantity(self.x3)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 7, 1, App.Units.Quantity(self.x4)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 8, 1, App.Units.Quantity(self.x5)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 9, 1, App.Units.Quantity(self.x6)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 10, 1, App.Units.Quantity(self.x7)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 11, 1, App.Units.Quantity(self.x8)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 12, 1, App.Units.Quantity(self.x9)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 5, 1, App.Units.Quantity(self.y2)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 6, 1, App.Units.Quantity(self.y3)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 7, 1, App.Units.Quantity(self.y4)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 8, 1, App.Units.Quantity(self.y5)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 9, 1, App.Units.Quantity(self.y6)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 10, 1, App.Units.Quantity(self.y7)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 11, 1, App.Units.Quantity(self.y8)))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 12, 1, App.Units.Quantity(self.y9)))

    def marimba_extrude(self):
        self.doc.addObject('Part::Extrusion', 'Bar')
        f = self.doc.getObject('Bar')
        f.Base = self.doc.getObject('Sketch')
        f.DirMode = "Normal"
        f.DirLink = None
        f.LengthFwd = self.marimbaWidth
        f.LengthRev = 0.000000000000000
        f.Solid = True
        f.Reversed = False
        f.Symmetric = False
        f.TaperAngle = 0.000000000000000
        f.TaperAngleRev = 0.000000000000000

    def box_part(self):
        self.doc.addObject("Part::Box", "Box1")
        self.doc.addObject("Part::Box", "Box2")
        box1 = self.doc.getObject('Box1')
        box2 = self.doc.getObject('Box2')
        box1.Height = 1
        box1.Length = 10
        box1.Width = 170
        box1.Placement = App.Placement(App.Vector(0, -100, -1), App.Rotation(App.Vector(0, 0, 1), 0),
                                       App.Vector(0, 0, 0))
        box2.Height = 1
        box2.Length = 10
        box2.Width = 170
        box2.Placement = App.Placement(App.Vector(self.marimbaLength - 10, -100, -1),
                                       App.Rotation(App.Vector(0, 0, 1), 0), App.Vector(0, 0, 0))

    def marimba_analysis(self):
        # make Analysis
        analysis_object = ObjectsFem.makeAnalysis(self.doc, 'Analysis')
        FemGui.setActiveAnalysis(self.doc.ActiveObject)

        # solver
        solver_object = ObjectsFem.makeSolverCalculixCcxTools(self.doc)
        solver_object.EigenmodesCount = self.eigenmodesCount
        solver_object.GeometricalNonlinearity = 'linear'
        solver_object.ThermoMechSteadyState = False
        solver_object.MatrixSolverType = 'default'
        solver_object.IterationsControlParameterTimeUse = False
        analysis_object.addObject(solver_object)

        # material
        FemGui.getActiveAnalysis().addObject(ObjectsFem.makeMaterialSolid(self.doc, 'MaterialSolid'))
        self.doc.Analysis.addObject(self.doc.ActiveObject)
        mat = self.doc.ActiveObject.Material
        mat['Name'] = "Wood-Palissander"
        mat['YoungsModulus'] = "15500 MPa"
        mat['PoissonRatio'] = ".030"
        mat['Density'] = "730 kg/m^3"
        mat['UltimateTensileStrength'] = "5.90 MPa"
        mat['ShearModulus'] = "8.3 MPa"
        self.doc.ActiveObject.Material = mat
        analysis_object.addObject(self.doc.ActiveObject)

        # fixed_constraint
        weight_constraint = ObjectsFem.makeConstraintSelfWeight(self.doc)
        fixed_constraint = ObjectsFem.makeConstraintFixed(self.doc, "FemConstraintFixed")
        fixed_constraint.References = [(self.doc.Bar, "Face4"),
                                       (self.doc.Bar, "Face14")]
        '''(self.doc.Box1, "Face3"), (self.doc.Box1, "Face4"), (self.doc.Box2, "Face3"), (self.doc.Box2, "Face4"),'''
        analysis_object.addObject(weight_constraint)
        analysis_object.addObject(fixed_constraint)

        # netgen
        mesh_object = self.doc.addObject('Fem::FemMeshShapeNetgenObject', 'FEMMeshNetgen')
        mesh_object.Shape = self.doc.Bar
        mesh_object.MaxSize = 10
        mesh_object.Fineness = "VeryFine"
        mesh_object.Optimize = True
        mesh_object.SecondOrder = True
        self.doc.recompute()
        analysis_object.addObject(mesh_object)

    def read_eigenmodes(self):
        frequency = []
        for i in range(1, self.eigenmodesCount + 1):
            eigenmode_object = self.doc.getObject(f'CCX_EigenMode_{i}_Results')
            frequency.append(eigenmode_object.EigenmodeFrequency)   # TODO fix "AttributeError: 'NoneType' object has no attribute 'EigenmodeFrequency'" that occurs on very few marimbas (technically solved, the error probability is now like 0.00000000000001%)
        return frequency        # TODO Error came up before 1st generation finished. So the problem might be in FreeCAD and not in genetic.crossover


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

