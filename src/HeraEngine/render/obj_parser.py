def parse_obj(file_path):
    vertices = []
    textures = []
    faces = []
    
    with open(file_path, 'r') as obj_file:
        for line in obj_file:
            if line.startswith('v '):  # Vertex
                vertices.append([float(x) for x in line.strip().split()[1:]])
            elif line.startswith('vt '):  # Texture coordinate
                textures.append([float(x) for x in line.strip().split()[1:]])
            elif line.startswith('f '):  # Face
                face = [
                    tuple(int(idx) if idx else None for idx in vertex.split('/')) 
                    for vertex in line.strip().split()[1:]
                ]
                faces.append(face)

    return {
        'vertices': vertices,
        'textures': textures,
        'faces': faces
    }

