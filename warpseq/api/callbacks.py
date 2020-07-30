from classforge import Class, Field


class DefaultCallback(Class):

    def on_init(self):
        pass

    def on_scene_start(self, scene):
        print("> starting scene: %s (%s)" % (scene.name, scene.obj_id))
        pass

    def on_clip_start(self, clip):
        print("> starting clip: %s (%s)" % (clip.name, clip.obj_id))

    def on_clip_stop(self, clip):
        print("> stopping clip: %s (%s)" % (clip.name, clip.obj_id))

    def on_clip_restart(self, clip):
        print("> restarting clip: %s (%s)" % (clip.name, clip.obj_id))

    def on_pattern_start(self, clip, pattern):
        print("> starting pattern: %s (%s)/%s (%s)" % (clip.name, clip.obj_id, pattern.name, pattern.obj_id))

    def on_note_on(self, event):
        #print("> play: %s" % event)
        pass

    def on_note_off(self, event):
        pass

class WebCallback(Class):
    pass




class Callbacks(object):

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
    def on_note_on(cls, event):
        for cb in Callbacks.CALLBACKS:
            cb.on_note_on(event)

    @classmethod
    def on_note_off(cls, event):
        for cb in Callbacks.CALLBACKS:
            cb.on_note_off(event)

