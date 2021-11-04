# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_material_brute_force

if "bpy" in locals():
    import importlib
    importlib.reload(mat_brute_force_ops)
    importlib.reload(mat_brute_force_panel)
else:
    from . import mat_brute_force_ops
    from . import mat_brute_force_panel


bl_info = {
    'name': 'Material Brute Force',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 93, 0),
    'location': '3D ViewPort - N panel',
    'description': 'Change material and make render'
}


def register():
    mat_brute_force_ops.register()
    mat_brute_force_panel.register()


def unregister():
    mat_brute_force_panel.unregister()
    mat_brute_force_ops.unregister()


if __name__ == '__main__':
    register()
