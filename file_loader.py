import ifcopenshell
import ifcopenshell.geom

def load_ifc_file(filename):
    shapes = []
    ifc_file = ifcopenshell.open(filename)
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    for product in ifc_file.by_type("IfcProduct"):
        if product.Representation:
            try:
                shape = ifcopenshell.geom.create_shape(settings, product)
                if shape.geometry:
                    shapes.append(shape)
                else:
                    print(f"No geometry for {product.GlobalId}")
            except Exception as e:
                print(f"Error creating shape for {product.GlobalId}: {e}")

    return shapes