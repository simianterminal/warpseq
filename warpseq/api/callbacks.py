# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# allows an application to hook certain events in the code without
# subclassing


class DefaultCallback(object):

    __slots__ = ()


    def on_init(self):
        pass

    def on_scene_start(self, scene):
        print("> starting scene: %s (%s)" % (scene.name, scene.obj_id))

    def on_clip_start(self, clip):
        print("> starting clip: %s (%s)" % (clip.name, clip.obj_id))

    def on_clip_stop(self, clip):
        print("> stopping clip: %s (%s)" % (clip.name, clip.obj_id))
        pass

    def on_clip_restart(self, clip):
        print("> restarting clip: %s (%s)" % (clip.name, clip.obj_id))
        pass

    def on_pattern_start(self, clip, pattern):
        print("> starting pattern: %s (%s)/%s (%s)" % (clip.name, clip.obj_id, pattern.name, pattern.obj_id))
        pass

    def all_clips_done(self):
        print("> all clips done")
        pass

    def keyboard_interrupt(self):
        print("> keyboard interrupt")
        pass

class WebCallback(object):
    pass

class Callbacks(object):

    __slots__ = ()

    CALLBACKS = []

    @classmethod
    def clear(cls):
        Callbacks.CALLBACKS = []

    @classmethod
    def register(cls, cb):
        Callbacks.CALLBACKS.append(cb)

    @classmethod
    def on_scene_start(cls, scene):
        for cb in Callbacks.CALLBACKS:
            cb.on_scene_start(scene)

    @classmethod
    def on_clip_start(cls, clip):
        for cb in Callbacks.CALLBACKS:
            cb.on_clip_start(clip)

    @classmethod
    def on_clip_stop(cls, clip):
        for cb in Callbacks.CALLBACKS:
            cb.on_clip_stop(clip)

    @classmethod
    def on_clip_restart(cls, clip):
        for cb in Callbacks.CALLBACKS:
            cb.on_clip_restart(clip)

    @classmethod
    def on_pattern_start(cls, clip, pattern):
        for cb in Callbacks.CALLBACKS:
            cb.on_pattern_start(clip, pattern)

    @classmethod
    def all_clips_done(cls):
        for cb in Callbacks.CALLBACKS:
            cb.all_clips_done()

    @classmethod
    def keyboard_interrupt(cls):
        for cb in Callbacks.CALLBACKS:
            cb.keyboard_interrupt()
