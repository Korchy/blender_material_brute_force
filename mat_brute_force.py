# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_material_brute_force

import bpy
import functools
import os


class MaterialBruteForce:

    _mode = 'IDLE'  # current mode (IDLE, RENDER, CANCEL)
    _materials_to_render = []
    _render_object = None

    @classmethod
    def start(cls, context):
        # get scene materials
        cls._get_materials_to_render(context=context)
        # render object
        cls._render_object = context.active_object
        # handlers
        if cls._on_render_complete not in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.append(cls._on_render_complete)
        if cls._on_render_cancel not in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.append(cls._on_render_cancel)
        # start render
        cls._mode = 'IDLE'
        bpy.app.timers.register(
            functools.partial(cls._render_next_material, context),
            first_interval=0.25
        )

    @classmethod
    def stop(cls, context):
        # stop
        # handlers
        if cls._on_render_complete in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.remove(cls._on_render_complete)
        if cls._on_render_cancel in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.remove(cls._on_render_cancel)

    @classmethod
    def _render_next_material(cls, context):
        # render next material
        if cls._mode == 'RENDER':
            # if rendering - retry after interval
            return 0.25
        elif cls._mode == 'IDLE':
            if cls._materials_to_render:
                mat = cls._materials_to_render.pop()
                # set material to object
                cls._render_object.active_material = mat
                # execute render
                cls._mode = 'RENDER'  # current step in progress
                if not bpy.app.timers.is_registered(cls.render):
                    bpy.app.timers.register(
                        functools.partial(cls.render),
                        first_interval=0.25
                    )
                return 0.25
            else:
                # Finish
                print('Finish')
                cls.stop(context=context)
                return None
        elif cls._mode == 'CANCEL':
            cls.stop(context=context)
            return None

    @classmethod
    def render(cls):
        # execute render
        rez = bpy.ops.render.render('INVOKE_DEFAULT', use_viewport=True)
        if rez == {'CANCELLED'}:
            # retry with timer
            return 0.25
        else:
            return None

    @classmethod
    def _get_materials_to_render(cls, context):
        # get materials list from scene
        cls._materials_to_render = [mat for mat in context.blend_data.materials
                                    if mat.name not in ['Dots Stroke']]

    @classmethod
    def _on_render_complete(cls, *args):
        # on render complete
        # save image
        cls._save_render(context=bpy.context)
        # render next
        cls._mode = 'IDLE'

    @classmethod
    def _on_render_cancel(cls, *args):
        # on render complete
        cls._mode = 'CANCEL'

    @classmethod
    def _save_render(cls, context):
        # save render to file
        output_path = cls.abs_path(
            path=context.scene.render.filepath
        )
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # save image
        bpy.data.images['Render Result'].save_render(
            os.path.join(
                output_path,
                cls._render_object.active_material.name + bpy.context.scene.render.file_extension
            )
        )

    @staticmethod
    def abs_path(path):
        # returns absolute file path from path
        if path[:2] == '//':
            return os.path.abspath(
                os.path.join(
                    os.path.dirname(os.path.abspath(bpy.data.filepath)),
                    path[2:]
                )
            )
        else:
            return os.path.abspath(path)
