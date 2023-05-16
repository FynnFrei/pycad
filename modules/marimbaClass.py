import FreeCAD as App
import importlib
import Part
import ObjectsFem
import Sketcher

import FreeCADGui as Gui
Gui.showMainWindow()    # TODO Gui Window is limited to 62 documents, i need to refresh it or its indices somehow
import FemGui
Gui.getMainWindow().hide()

class Marimba:
    def __init__(self, marimba_length, marimba_width, marimba_height, ground_length, *list_xy):

        # make new doc:
        self.doc = App.newDocument()
        # declare variables
        self.marimba_length, self.marimba_width, self.marimba_height = marimba_length, marimba_width, marimba_height
        self.ground_length = ground_length
        self.list_xy_len = len(list_xy)
        self.list_xy = list_xy

        self.eigenmodesCount = 10  # Number of calculated Eigenmodes
        self.eigenmodeLowLimit = 80

    def recompute(self):
        self.doc.recompute()

    def save(self, path: str):
        self.doc.saveAs(path)

    def marimba_sketch(self):
        sketch = self.doc.addObject("Sketcher::SketchObject", "Sketch")
        sketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000),
                                         App.Rotation(0.707107, 0.000000, 0.000000, 0.707107))

        # -----------------ELEMENTS----------------------------
        # Add LieSegments:
        line0 = sketch.addGeometry(
            Part.LineSegment(App.Vector(1, 0, 0),
                             App.Vector(0, 0, 0)),
            False)
        line1 = sketch.addGeometry(
            Part.LineSegment(App.Vector(0, 1, 0),
                             App.Vector(0, 2, 0)),
            False)
        line2 = sketch.addGeometry(
            Part.LineSegment(App.Vector(1, 2, 0),
                             App.Vector(3, 2, 0)),
            False)
        line3 = sketch.addGeometry(
            Part.LineSegment(App.Vector(4, 2, 0),
                             App.Vector(4, 0, 0)),
            False)
        line4 = sketch.addGeometry(
            Part.LineSegment(App.Vector(3, 0, 0),
                             App.Vector(2, 0, 0)),
            False)

        num_of_circles = int(
            (self.list_xy_len + 4) / 2)  # sets the number of points on B-spline -> number of parameters / 2
        bspline = 5 + num_of_circles  # The index of B-spline for later use (num of lines + num of circles)
        circle_list = []  # List of indices of circles
        point_list = []  # List of all points on B-spline

        for i in range(num_of_circles):
            sketch.addGeometry(Part.Circle(App.Vector(10, 0, 0), App.Vector(0, 0, 1), 10), True)
            circle_list.append(i + 5)  # +5 because of the 5 lines (line0-line4)

        for i in range(num_of_circles):
            point_list.append(App.Vector(0, 0, 0))
        sketch.addGeometry(Part.BSplineCurve(point_list, None, None, False, 3, None, False), False)

        # ----------------CONSTRAINTS----------------

        # DIMENSIONAL CONSTRAINTS:

        # FIX line0 vertex1 TO ORIGIN:
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 0, 2, App.Units.Quantity('0 mm')))
        sketch.addConstraint(Sketcher.Constraint("DistanceY", 0, 2, App.Units.Quantity('0 mm')))

        # dimensions:
        sketch.addConstraint(Sketcher.Constraint('Distance', 1, 1, 1, 2, App.Units.Quantity(self.marimba_height)))
        sketch.addConstraint(Sketcher.Constraint('Distance', 2, 1, 2, 2, App.Units.Quantity(self.marimba_length)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 0, 2, 0, 1, App.Units.Quantity(self.ground_length)))
        sketch.addConstraint(Sketcher.Constraint("DistanceX", 4, 2, 4, 1, App.Units.Quantity(self.ground_length)))

        # GEOMETRIC CONSTRAINTS:
        sketch.addConstraint(Sketcher.Constraint("Horizontal", line0))
        sketch.addConstraint(Sketcher.Constraint("Vertical", line1))
        sketch.addConstraint(Sketcher.Constraint("Horizontal", line2))
        sketch.addConstraint(Sketcher.Constraint('Vertical', line3))
        sketch.addConstraint(Sketcher.Constraint('Horizontal', line4))
        sketch.addConstraint(Sketcher.Constraint('Equal', 3, 1))

        # LINK ALL LINES:
        # Example1: Line 0, Vertex 2 is linked with Line 1, Vertex 1
        sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 2, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 2, 2, 3, 1))
        sketch.addConstraint(Sketcher.Constraint("Coincident", 3, 2, 4, 1))

        # Variable vertices:
        for i in range(num_of_circles - 2):
            sketch.addConstraint(
                Sketcher.Constraint("DistanceX", circle_list[i + 1], 3, App.Units.Quantity(self.list_xy[i * 2])))
            sketch.addConstraint(
                Sketcher.Constraint("DistanceY", circle_list[i + 1], 3, App.Units.Quantity(self.list_xy[(i * 2) + 1])))

        # MAKE CONTROL POINT (Circle5...n) WEIGHT and connect B-Spline to circles:
        for i in range(num_of_circles):
            sketch.addConstraint(Sketcher.Constraint('Weight', circle_list[i], 1.000000))
            sketch.addConstraint(
                Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint', circle_list[i], 3, bspline, i))

        sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 2, bspline, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 1, bspline, 2))

    def marimba_extrude(self):
        self.doc.addObject('Part::Extrusion', 'Bar')
        f = self.doc.getObject('Bar')
        f.Base = self.doc.getObject('Sketch')
        f.DirMode = "Normal"
        f.DirLink = None
        f.LengthFwd = self.marimba_width
        f.LengthRev = 0.000000000000000
        f.Solid = True
        f.Reversed = False
        f.Symmetric = False
        f.TaperAngle = 0.000000000000000
        f.TaperAngleRev = 0.000000000000000

    def marimba_analysis(self):
        # make Analysis
        analysis_object = ObjectsFem.makeAnalysis(self.doc, 'Analysis')
        FemGui.setActiveAnalysis(self.doc.ActiveObject)

        # solver
        solver_object = ObjectsFem.makeSolverCalculixCcxTools(self.doc)
        solver_object.EigenmodesCount = self.eigenmodesCount
        solver_object.EigenmodeLowLimit = self.eigenmodeLowLimit
        solver_object.GeometricalNonlinearity = 'linear'
        solver_object.ThermoMechSteadyState = False
        solver_object.MatrixSolverType = 'default'
        solver_object.IterationsControlParameterTimeUse = False
        analysis_object.addObject(solver_object)

        # material
        FemGui.getActiveAnalysis().addObject(ObjectsFem.makeMaterialSolid(self.doc, 'MaterialSolid'))
        self.doc.Analysis.addObject(self.doc.ActiveObject)
        mat = self.doc.ActiveObject.Material
        mat['Name'] = "Wood-Chestnut"  # TODO fill material properties
        mat['CompressiveStrength'] = "4300 kPa"  # perpendicular to grain
        mat['Density'] = "430 kg/m^3"  # / specific gravity
        mat['FractureToughness'] = ""
        mat['PoissonRatio'] = "0.32"
        mat['ShearModulus'] = "7.4 MPa"
        mat['UltimateStrain'] = ""
        mat['UltimateTensileStrength'] = "59.0 MPa"  # max stress before breaking / modulus of rupture
        # mat['YieldStrength'] = ""                       # Elastic limit -> Deformation (irrelevant)
        mat['YoungsModulus'] = "8500 MPa"  # Modulus of elasticity
        mat['Stiffness'] = ""
        self.doc.ActiveObject.Material = mat
        analysis_object.addObject(self.doc.ActiveObject)

        # Wood Data:
        '''mat['Name'] = "White European Oak"  # TODO fill material properties
        mat['CompressiveStrength'] = "7800 kPa"  # perpendicular to grain
        mat['Density'] = "670 kg/m^3"  # / specific gravity
        mat['FractureToughness'] = ""
        mat['PoissonRatio'] = "0.37"
        mat['ShearModulus'] = "11.6 MPa"
        mat['UltimateStrain'] = ""
        mat['UltimateTensileStrength'] = "97.1 MPa"  # max stress before breaking / modulus of rupture
        # mat['YieldStrength'] = ""                       # Elastic limit -> Deformation (irrelevant)
        mat['YoungsModulus'] = "10600 MPa"  # Modulus of elasticity
        mat['Stiffness'] = ""
        
        mat['Name'] = "Wood-Chestnut"  # TODO fill material properties
        mat['CompressiveStrength'] = "4300 kPa"  # perpendicular to grain
        mat['Density'] = "430 kg/m^3"  # / specific gravity
        mat['FractureToughness'] = ""
        mat['PoissonRatio'] = "0.32"
        mat['ShearModulus'] = "7.4 MPa"
        mat['UltimateStrain'] = ""
        mat['UltimateTensileStrength'] = "59.0 MPa"  # max stress before breaking / modulus of rupture
        # mat['YieldStrength'] = ""                       # Elastic limit -> Deformation (irrelevant?)
        mat['YoungsModulus'] = "8500 MPa"  # Modulus of elasticity
        mat['Stiffness'] = ""
        
        mat['Name'] = "Wood-Cherry"        # TODO fill material properties
        mat['CompressiveStrength'] = "4800 kPa"         # perpendicular to grain
        mat['Density'] = "500 kg/m^3"                   # / specific gravity
        mat['FractureToughness'] = ""
        mat['PoissonRatio'] = "0.39"
        mat['ShearModulus'] = "11.7 MPa"
        mat['UltimateStrain'] = ""
        mat['UltimateTensileStrength'] = "85.0 MPa"     # max stress before breaking / modulus of rupture
        # mat['YieldStrength'] = ""                       # Elastic limit -> Deformation (irrelevant?)
        mat['YoungsModulus'] = "10300 MPa"              # Modulus of elasticity
        mat['Stiffness'] = ""'''

        # fixed_constraint
        displacement_constraint = ObjectsFem.makeConstraintDisplacement(self.doc, "FemConstraintDisplacement")
        displacement_constraint.yFree = False
        displacement_constraint.yFix = True
        displacement_constraint.References = [(self.doc.Bar, "Face1"),
                                              (self.doc.Bar, "Face2"),
                                              (self.doc.Bar, "Face3"),
                                              (self.doc.Bar, "Face4"),
                                              (self.doc.Bar, "Face5"),
                                              (self.doc.Bar, "Face6"),
                                              (self.doc.Bar, "Face7"),
                                              (self.doc.Bar, "Face8")]
        analysis_object.addObject(displacement_constraint)

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
        void = True
        mode_index = 1

        # check what the lowest EigenMode object index in FreeCAD is
        while void:
            if self.doc.getObject(f'CCX_EigenMode_{mode_index}_Results'):
                void = False
            else:
                mode_index += 1

        for i in range(mode_index, self.eigenmodesCount + 1):
            eigenmode_object = self.doc.getObject(f'CCX_EigenMode_{i}_Results')     # TODO error occurred bc. sometimes FreeCAD skips index 1(starts for example with index 4)
            frequency.append(
                eigenmode_object.EigenmodeFrequency)
        return frequency


def marimba_femrun():
    '''# run the analysis all in one
    from femtools import ccxtools
    fea = ccxtools.FemToolsCcx()
    print("Debug marimbaClass 0")
    fea.purge_results()
    print("Debug marimbaClass 1")
    fea.run()
    print("Debug marimbaClass 2")'''
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


def open_freecad():
    Gui.showMainWindow()


def close_doc():
    App.closeDocument("Unnamed")


def close_freecad():
    Gui.getMainWindow().close()
