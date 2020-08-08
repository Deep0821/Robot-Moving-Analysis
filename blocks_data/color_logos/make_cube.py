import sys 

HEADER = """mtllib {}.mtl
o Mesh
v -0.025 -0.025 -0.025
v 0.025 -0.025 -0.025
v 0.025 0.025 -0.025
v -0.025 0.025 -0.025
v -0.025 -0.025 0.025
v 0.025 -0.025 0.025
v 0.025 0.025 0.025
v -0.025 0.025 0.025
vn 0 -1 0.5
vn 0 1 0.5
vn -1 0 0.5
vn 1 0 0
vn 0 0 1
vn 0 0 -1
vt 0 0
vt 1 0
vt 0 1
vt 1 1
usemtl CubeTop
f 1/1/1 2/2/1 6/4/1
f 1/1/1 6/4/1 5/3/1
usemtl CubeTop
f 3/1/2 4/2/2 8/4/2
f 3/1/2 8/4/2 7/3/2
usemtl CubeTop
f 4/1/3 1/2/3 5/4/3
f 4/1/3 5/4/3 8/3/3
usemtl CubeTop
f 2/1/4 3/2/4 7/4/4
f 2/1/4 7/4/4 6/3/4
usemtl CubeTop
f 5/1/5 6/2/5 7/4/5
f 5/1/5 7/4/5 8/3/5
usemtl CubeTop
f 4/1/6 3/2/6 2/4/6
f 4/1/6 2/4/6 1/3/6"""

logo_type = sys.argv[1]

with open(f"{logo_type}.obj", "w") as f1:
    head = HEADER.format(logo_type)
    f1.write(head) 


