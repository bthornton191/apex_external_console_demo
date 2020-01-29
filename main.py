# pylint:disable=no-name-in-module, no-member, invalid-name, wrong-import-order
import os
import launch_apex as _la       #pylint:disable=unused-import  
import apex
from library import truss_sketch, find_constraint_nodes, find_load_nodes, get_unused_name

# Define a directory for saving models
SAVE_DIRECTORY = os.path.join(os.getcwd(), 'model')

# Create the save directory if it doesn't exist
if os.path.exists(SAVE_DIRECTORY) is False:
    os.mkdir(SAVE_DIRECTORY)

# Define the endpoints of the truss
TRUSS_ENDPOINTS = [(0, 0), (0, 100), (100, 0), (100, 100)]


def build_truss_model():
    # Get the current model
    model = apex.currentModel()

    # Create a sketch of the truss
    truss_sketch(model, TRUSS_ENDPOINTS)

    # Get the part object and part collection
    part = apex.getPart('{}/Part 1'.format(model.getName()))
    part_collection = apex.EntityCollection()
    part_collection.append(part)

    # Mesh the truss curves
    curve = part.getCurves()[0]
    collection = apex.EntityCollection()
    collection.append(curve)
    mesh = apex.mesh.createCurveMesh(name='', target=collection, meshSize=10.0, elementOrder=apex.mesh.ElementOrder.Linear).curveMeshes[0]

    # Apply Constraints
    constraint_nodes = find_constraint_nodes(mesh.getNodes())    
    _constraints = [apex.environment.createDisplacementConstraint(name=f'Constraint {idx+1}', constraintType=apex.attribute.ConstraintType.Clamped, applicationMethod=apex.attribute.ApplicationMethod.Direct, target=node) for idx, node in enumerate(constraint_nodes)]

    # Apply Loads
    load_nodes = find_load_nodes(mesh.getNodes())
    _loads = [apex.environment.createForceMoment(name=f'Load{idx+1}', forceMomentRep=apex.environment.createForceMomentStaticRepByComponent(name='load', description='', forceY=-100.0), applicationMethod=apex.attribute.ApplicationMethod.Direct, target=node, orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)) for idx, node in enumerate(load_nodes)]

    # Apply Gravity Load
    orientation = apex.construct.createOptionOrientation()
    orientation.GlobalNY = True
    _gravity_1 = apex.environment.createGravityByG(name='Gravity', gravConstant=386.08858268, orientation=orientation, gravConstantMultiplier=1.0)

    # Create and assign material
    material_1 = apex.catalog.createMaterial(name='steel', color=[64,254,250])
    material_1.update(elasticModulus=30000000.0)
    material_1.update(poissonRatio=0.3)
    material_1.update(density=0.000725222171)
    apex.attribute.assignMaterial(material=material_1, target=part_collection)

    # Create and apply beam sections
    beamshape_1 = apex.attribute.createBeamShapeHollowRoundByThickness(name='Beam Shape', outerRadius=2.0, thickness=0.25)
    _beamspan_1 = apex.attribute.createBeamSpanFree(name='Span', beamTarget=curve.getEdges(), shapeEndA=beamshape_1, shapeEndB=beamshape_1, shapeEndA_orientation=0.0, shapeEndB_orientation=0.0, shapeEndA_offset1=0.0, shapeEndA_offset2=0.0, shapeEndB_offset1=0.0, shapeEndB_offset2=0.0)

    # Create analysis
    study = apex.getPrimaryStudy()
    scenario = study.createScenarioByModelRep(context=part, simulationType=apex.studies.SimulationType.Static)
    
    # TODO: Figure out why the following line throws an error
    # scenario.execute()

    model_save_name = get_unused_name(model.name, SAVE_DIRECTORY)
    model.saveAs(model_save_name, SAVE_DIRECTORY)

if __name__ == '__main__':
    build_truss_model()