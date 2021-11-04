# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_material_brute_force

from bpy.props import IntProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .mat_brute_force import MaterialBruteForce


class MAT_BRUTE_FORCE_OT_main(Operator):
    bl_idname = 'mat_brute_force.main'
    bl_label = 'Brute Force Materials'
    bl_description = 'mat_brute_force - main operator'
    bl_options = {'REGISTER', 'UNDO'}

    param1: IntProperty(
        name='param1',
        default=0,
        subtype='UNSIGNED',
        min=0,
        max=1
    )

    def execute(self, context):
        MaterialBruteForce.start(
            context=context
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object)


def register():
    register_class(MAT_BRUTE_FORCE_OT_main)


def unregister():
    unregister_class(MAT_BRUTE_FORCE_OT_main)
