from . exceptions import *

# code supporting public API boilerplate reduction - a bit too much meta-programming but ah well

class BaseApi(object):

    def __init__(self, public_api, song):
        self.api  = public_api
        self.song = song

        if self.__class__.add_method:
            self.fn_add         = getattr(self.song, self.__class__.add_method)
        self.add_required   = self.__class__.add_required
        self.edit_required  = self.__class__.edit_required
        if self.__class__.remove_method:
            self.fn_remove      = getattr(self.song, self.__class__.remove_method)

        self.public_fields = self.__class__.public_fields

    def lookup(self, name, require=False):
        coll = self._get_collection()
        if type(coll) == dict:
            for (k,v) in coll.items():
                if v.name == name:
                    return v
        else:
            for k in coll:
                if k.name == name:
                    return k
        if require:
            raise NotFound("\"%s\" not found" % name)
        return None

    def list(self):
        coll = self._get_collection()
        data = []
        if type(coll) == dict:
            for (k,v) in coll.items():
                data.append(self._short_details(v))
        else:
            return [ self._short_details(x) for x in coll ]
        return data

    def _short_details(self, obj):
        return obj.name

    def details(self, name):
        obj = self.lookup(name)
        if obj is None:
            raise NotFound("\"%s\" not found" % name)
        data = obj.to_dict()
        new_data = dict()
        for (k,v) in data.items():
            if k in self.public_fields:
                value = getattr(obj, k)
                if type(value) == list:
                    if len(value) > 0 and hasattr(value[0], 'obj_id'):
                        value = [ x.name for x in value]
                elif hasattr(value, 'obj_id'):
                    value = value.name
                new_data[k] = value
        self._update_details(new_data, obj)
        return new_data

    def _update_details(self, details, obj):
        pass

    def _get_collection(self):
        return getattr(self.song, self.__class__.song_collection)

    def _require_input(self, what, params):
        for k in what:
            if params[k] is None:
                raise RequiredInput("%s is required" % k)

    def _ok(self):
        return True

    def _generic_add(self, name, params):
        obj = self.lookup(name)
        del params['self']
        del params['name']
        self._require_input(self.add_required, params)
        if not obj:
            obj = self.__class__.object_class(name=name, **params)
            self.fn_add([obj])
            return self._ok()
        else:
            raise AlreadyExists()

    def _generic_edit(self, name, params):
        obj = self.lookup(name)
        if not obj:
            raise NotFound("%s not found" % name)
        del params["name"]
        del params["self"]

        self._require_input(self.edit_required, params)
        if "new_name" in params:
            value = params["new_name"]
            if value:
                obj.name = value
            del params["new_name"]


        for (k,v) in params.items():
            value = v
            if v is not None or k in self.__class__.nullable_edits:
                value = v
                setattr(obj, k, value)
        return self._ok()

    def _generic_remove(self, name):
        obj = self.lookup(name, require=True)
        self.fn_remove(obj)
        return self._ok()

