# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_material_brute_force

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class MAT_BRUTE_FORCE_PT_panel(Panel):
    bl_idname = 'MAT_BRUTE_FORCE_PT_panel'
    bl_label = 'Material Brute Force'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MBF'

    def draw(self, context):
        operator = self.layout.operator(
            'mat_brute_force.main',
            icon='SHADING_TEXTURE'
        )


def register():
    register_class(MAT_BRUTE_FORCE_PT_panel)


def unregister():
    unregister_class(MAT_BRUTE_FORCE_PT_panel)
